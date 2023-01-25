import pymysql
import tarfile
import time
import glob
import os, sys, shutil, subprocess, psutil
from lxml import etree

__NBNODES__ = os.cpu_count()

def mariadbconnection():
    try:
        conn = pymysql.connect(
            user="triannot2022",
            password="Tr14nn0t2022!",
            host="127.0.0.1",
            port=3306,
            database="triannot2022"
        )
        return conn

    except mariadb.Error as e:
        print("Error connecting to MariaDB Platform: "+str(e))
        sys.exit(1)

def updatestepdb(cur):
    stepfiles = glob.glob('/home/users/triannot/steps/*.xml')
    cur.execute("select ana_libelle from tr_analyse_ana")
    anafiles = [item[0] for item in list(cur)]
    cur.execute("select ana_id from tr_analyse_ana")
    anaids = [item[0] for item in list(cur) ]
    anaidmax = max(anaids)
    stepfilenames = []
    for stepfile in stepfiles:
        stepfilename = stepfile.split('/')[-1][:-4]
        stepfilenames.append(stepfilename)
        if stepfilename not in anafiles:
            anaidmax += 1
            cur.execute("INSERT INTO `tr_analyse_ana` (ana_id,ana_libelle) VALUES (%s,%s)", (str(anaidmax), stepfilename))
    for anafile in anafiles:
        if anafile not in stepfilenames:
            cur.execute("DELETE FROM `tr_analyse_ana` WHERE ana_libelle=%s", anafile)

def getprocess_by_statut(cur, statut = 0):
    cur.execute("SELECT * FROM t_request_req WHERE req_statut=%s", statut)
    process = list(cur)
    return process

def gettypemol(cur, id_):
    cur.execute("SELECT tmo_libelle FROM tr_typemol_tmo WHERE tmo_id=%s", id_)
    for libelle in cur:
        return libelle[0]

def getanalyse(cur, id_):
    cur.execute("SELECT ana_libelle FROM tr_analyse_ana WHERE ana_id=%s", id_)
    for libelle in cur:
        return libelle[0]

def getlogin(cur, id_):
    cur.execute("SELECT ana_libelle FROM tr_analyse_ana WHERE ana_id=%s", id_)
    for libelle in cur:
        return libelle[0]

def startprocess(req_code, req_sequences, req_ana, req_tmo, req_min_size, req_max_size, req_overlap, req_splitseq, src):
    os.makedirs(f'/home/users/triannot/run/{req_code}/Anno', exist_ok=True)
    shutil.copy(f'{src}/{req_sequences}', f'/home/users/triannot/run/{req_code}/')
    shutil.copy(f'/home/users/triannot/steps/{req_ana}.xml', f'/home/users/triannot/run/{req_code}/')
    if req_splitseq == 1:
        cmd = f"TriAnnotPipeline.py -w /home/users/triannot/run/{req_code}/Anno --debug --logtofile run -s /home/users/triannot/run/{req_code}/{req_sequences} -t  /home/users/triannot/run/{req_code}/{req_ana}.xml --type {req_tmo} -ir Local -tr SLURM --maxinstance {__NBNODES__*8} --clean loetcsp --minlength {req_min_size} --splitseq --maxlength {req_max_size} --overlap {req_overlap} >& /home/users/triannot/run/{req_code}/runTAP.log"
    else:
        cmd = f"TriAnnotPipeline.py -w /home/users/triannot/run/{req_code}/Anno --debug --logtofile run -s /home/users/triannot/run/{req_code}/{req_sequences} -t  /home/users/triannot/run/{req_code}/{req_ana}.xml --type {req_tmo} -ir Local -tr SLURM --maxinstance {__NBNODES__*8} --clean loetcsp --minlength {req_min_size} --maxlength {req_max_size} --overlap {req_overlap} >& /home/users/triannot/run/{req_code}/runTAP.log"
    triannotProcess = subprocess.Popen(cmd, shell = True)
    return triannotProcess
        
def change_job_statut(cur, statut, job_id):
    return cur.execute("UPDATE t_request_req SET req_statut=%s WHERE req_id=%s", (statut,job_id))

def setprogress(cur, req_code):
    pwd = f"/home/users/triannot/run/{req_code}/Anno/"
    progressfiles = glob.glob(f"{pwd}/**/*_progress", recursive = True)
    completion = 0
    i = 0
    for progressfile in progressfiles:
        try:
            tree = etree.parse(progressfile)
            completion += int(tree.xpath("/unit_progression/percentage_of_completion")[0].text)
            i += 1
        except:
            continue

    completion = (completion/(100*i))*100 if i > 0 else 0
    cur.execute("UPDATE t_request_req SET req_progress=%s WHERE req_code=%s", (int(completion), req_code))

def archive(req_code, phpWorkDir):
    source_dir = f"/home/users/triannot/run/{req_code}/"
    tarFile = f"/home/users/triannot/run/{req_code}.tar.gz"
    with tarfile.open(tarFile, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    shutil.copy(tarFile, phpWorkDir)

def geterrfilesize(req_code):
    pwd = f"/home/users/triannot/run/{req_code}/Anno/"
    errFiles = glob.glob(f"{pwd}*.err", recursive = False)
    for errFile in errFiles:
        errFileSize = os.path.getsize(errFile)
        return errFileSize if errFileSize != None else 0
    return 0


pending, running, finished, failed =  range(0,4)
# Get pending job
conn = mariadbconnection()
cur = conn.cursor()
pending_jobs = getprocess_by_statut(cur,pending)
if len(pending_jobs) == 0:
    sys.exit(0)

# Load job description
job = pending_jobs[0]

req_id, req_sequences, req_code, req_statut, req_login, req_date, req_tmo_id, req_min_size, req_max_size, req_splitseq, req_overlap, req_ana_id = range(0,12)
req_tmo = gettypemol(cur, job[req_tmo_id])
req_ana = getanalyse(cur, job[req_ana_id])

# Change job statut, runnning
change_job_statut(cur, running, job[req_id])
conn.commit()

# Start triannot process
phpWorkDir = f"/var/www/html/Upload/{job[req_date].replace('-','/')}/{job[req_login]}/{job[req_code]}/"
triannotProcess = startprocess(job[req_code], job[req_sequences], req_ana, req_tmo, job[req_min_size], job[req_max_size], job[req_overlap], job[req_splitseq], phpWorkDir)

# Process progress
pid = triannotProcess.pid
running = True
while running: #not triannotProcess.poll() :
    setprogress(cur, job[req_code])
    conn.commit()
    time.sleep(10)
    if psutil.pid_exists(pid):
        running = not psutil.Process(pid).status() == 'zombie'
    else:
        running = False
try:
    triannotProcess.terminate()
except:
    pass

# Process ended:
pwd = f"/home/users/triannot/run/{job[req_code]}/Anno/"
file_size = geterrfilesize(job[req_code])
if file_size > 0: # Failed
    change_job_statut(cur,failed,job[req_id])
else: # Success
    change_job_statut(cur,finished,job[req_id])
conn.commit()

archive(job[req_code], phpWorkDir)
