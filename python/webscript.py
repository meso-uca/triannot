import mariadb
import tarfile
import os, sys, shutil, subprocess
from lxml import etree

__NBNODES__ = 8

def mariadbconnection():
    try:
        conn = mariadb.connect(
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

def getprocess_by_statut(cur, statut = 0):
    cur.execute("SELECT * FROM t_request_req WHERE req_statut=?", (statut,))
    process = list(cur)
    return process

def gettypemol(cur, id_):
    cur.execute("SELECT tmo_libelle FROM tr_typemol_tmo WHERE tmo_id=?", (id_,))
    for libelle in cur:
        return libelle[0]

def getanalyse(cur, id_):
    cur.execute("SELECT ana_libelle FROM tr_analyse_ana WHERE ana_id=?", (id_,))
    for libelle in cur:
        return libelle[0]

def startprocess(req_code, req_sequences, req_ana, req_tmo, req_min_size, req_max_size, req_overlap, req_splitseq, src):
    os.makedirs(f'/home/users/triannot/run/{req_code}/Anno', exist_ok=True)
    shutil.copy(f'{src}/{req_sequences}', f'/home/users/triannot/run/{req_code}')
    shutil.copy(f'/home/users/triannot/steps/{req_ana}', f'/home/users/triannot/run/{req_code}')
    if req_splitseq == 1:
        cmd = f"TriAnnotPipeline.py -w /home/users/triannot/run/{req_code}/Anno --debug --logtofile run -s /home/users/triannot/run/{req_code}/{req_sequences} -t  /home/users/triannot/run/{req_code}/{req_ana} --type {req_tmo} -ir Local -tr SLURM --maxinstance {__NBNODES__*8} --clean loetcsp --minlength {req_min_size} --splitseq --maxlength {req_max_size} --overlap {req_overlap}".split()
    else:
        cmd = f"TriAnnotPipeline.py -w /home/users/triannot/run/{req_code}/Anno --debug --logtofile run -s /home/users/triannot/run/{req_code}/{req_sequences} -t  /home/users/triannot/run/{req_code}/{req_ana} --type {req_tmo} -ir Local -tr SLURM --maxinstance {__NBNODES__*8} --clean loetcsp --minlength {req_min_size} --maxlength {req_max_size} --overlap {req_overlap}".split()
    triannotProcess = subprocess.Popen(cmd)
    return triannotProcess
        
def change_job_statut(cur, statut, job_id):
    return cur.execute("UPDATE t_request_req SET req_statut=? WHERE req_id=?", (statut,job_id))

def setprogress(req_code):
    pwd = f"/home/users/triannot/run/{req_code}/Anno/"
    chunks = os.listdir(pwd)
    for chunk in chunks:
        if not os.path.isdir(os.path.join(pwd,chunk)):
            continue
        tree = etree.parse(os.path.join(pwd, chunk, "TriAnnot_progress"))
        completion += int(tree.xpath("/unit_progression/percentage_of_completion").text)
        i += 1
    completion = (completion/(100*i))*100
    cur.execute("UPDATE t_request_req SET req_progress = ? WHERE ", (completion))

# Get pending job
conn = mariadbconnection()
cur = conn.cursor()
pending_jobs = getprocess_by_statut(cur,0)
if len(pending_jobs) == 0:
    sys.exit(0)

# Load job description
job = pending_jobs[0]

req_id = job[0]
req_sequences = job[1]
req_code = job[2]
req_login = job[3]
req_ = job[4]
req_date = job[5]
req_tmo = gettypemol(cur, job[6])
req_min_size = job[7]
req_max_size = job[8]
req_splitseq = job[9]
req_overlap = job[10]
req_ana = getanalyse(cur, job[11])

# Change job statut, runnning
change_job_statut(cur, 1, job[0])
conn.commit()

# Start triannot process
phpWorkDir = f"/var/www/html/Upload/{req_date.replace('-','/')}/{req_login}/{req_code}"
triannotProcess = startprocess(req_code, req_sequences, req_ana, req_tmo, req_min_size, req_max_size, req_overlap, req_splitseq, phpWorkDir)

# Process progress
while triannotProcess.poll():
    setprogress(req_code)

# Process ended:
pwd = f"/home/users/triannot/run/{req_code}/Anno/"
errFile = geterrfile()
file_size = os.path.getsize(os.path.join(pwd,errFile)) # with errors ?
if file_size > 0: # Failed
    change_job_statut(cur,2,req_id)
else: # Success
    change_job_statut(cur,3,req_id)
conn.commit()




