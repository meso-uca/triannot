from datetime import timedelta
#from dateutil import parser
import sys
import os
import re
import math

def get_timedelta(date_str):
    # Returns timedelta object from string in [DD-[hh:]]mm:ss format
    days = 0
    hours = 0
    minutes = 0
    seconds = 0

    if date_str.count('-') == 1:
        days = int(date_str.split('-')[0])
        date_str = date_str.partition('-')[2]
    if date_str.count(':') == 2:
        hours = int(date_str.split(':')[0])
        date_str = date_str.partition(':')[2]

    try:
        minutes=int(date_str.split(':')[0])
        seconds=float(date_str.split(':')[1])
    except:
        pass

    return timedelta(   days=days,
                        hours=hours,
                        minutes=minutes,
                        seconds=seconds
                    )


# sacct -a -np -o JobID,JobName%99,CPUTime,Elapsed,TotalCPU,AllocCPUS,NTasks,Start,End,NodeList,ReqMem,MaxRSS,MaxVMSize --state=CD -S 2021-03-10T22:00:00 -E 2021-03-22 > jobs.txt
# awk 'NR % 2 == 0' jobs.txt > jobs-steps.txt
# awk 'NR % 2 == 1' jobs.txt > jobs-allocs.txt
# paste jobs-allocs.txt jobs-steps.txt | awk -F'|' '{print $1 "|" $2 "|" $3 "|" $4 "|" $5 "|" $6 "|" $20 "|" $8 "|" $9 "|" $10 "|" $11 "|" $25 "|" $26 "|"}' > jobs-fixed.txt
# python3 stats.py < jobs-fixed.txt | sort -n -k2 | awk '{print $2}' | jq -s '{minimum:min,maximum:max,average:(add/length),median:(sort|if length%2==1 then.[length/2|floor]else[.[length/2-1,length/2]]|add/2 end)}'
# {
#  "minimum": 3.89,
#  "maximum": 225.7,
#  "average": 90.0650599847306,
#  "median": 91.26
# }



# 1877442|TA2058510310_phleroy_6b20f20c-81e3-11eb-a2ac-fa163eb5237b_132_parsing_SIMsearch|00:00:01|00:00:01|00:01.137|1|1|2021-03-11T04:35:13|2021-03-11T04:35:14|tap-compute0005|5000Mn|952K|202972K|
jobid,jobname,cputime,elapsed,totalcpu,alloccpus,ntasks,start,end,nodelist,reqmem,maxrss,maxvmsize = range(0,13)

for line in sys.stdin:
  if line.count("|") == 0: continue
  data = line.split("|")
  JobID = int(data[jobid])
  Elapsed = get_timedelta(data[elapsed]).total_seconds()
  TotalCPU = get_timedelta(data[totalcpu]).total_seconds()
  if Elapsed > 0.0:
    efficiency = 100.0 * TotalCPU / Elapsed
    print(f"%09d %3.2f" % (JobID, efficiency))

