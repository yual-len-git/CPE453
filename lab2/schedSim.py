import sys

valid = ["FIFO", "RR", "SRTN"]
quantumvalid = 1234567890

class Process:
    process_number = 0
    wait_time = 0
    turnaround_time = 0
    # remaining = 0
    finished = False


    def __init__(self, burst_time, arrival_time):
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.remaining = burst_time

def scheduleSetup():
    schedule = []
    file = open(sys.argv[1], "r")
    for line in file:
        line = line.rstrip().split(" ")
        schedule.append(Process(int(line[0]), int(line[1])))
    schedule = sorted(schedule, key=lambda job: job.arrival_time, reverse = False)
    pcount = 0
    for job in schedule:
        job.process_number = pcount
        pcount += 1

    return schedule

def getAlgorithm():
    algo = "FIFO"       #default
    if "-p" in sys.argv:
        indx = sys.argv.index("-p") + 1
        if sys.argv[indx] in valid:
            algo = sys.argv[indx]
        else:
            print("Not a valid algorithm")
            sys.exit()
    return algo

def getQuantum():
    quantum = 1             #default
    if "-q" in sys.argv:
        indx = sys.argv.index("-q") + 1
        if int(sys.argv[indx]) < 1:
            print("Quantum must be greater than or equal to 1")
            sys.exit()
        else:
            quantum = int(sys.argv[indx])
    return quantum

def FIFO(schedule):
    time = 0
    for job in schedule:
        job.wait_time = time - job.arrival_time
        time += job.burst_time
        job.turnaround_time = time - job.arrival_time
        jobTime(job)
    averageTime(schedule)

def RR(schedule, quantum):
    time = 0
    total = len(schedule)
    
    while total > 0:
        for job in schedule:
            if job.remaining < quantum:
                time += job.remaining
                job.remaining = 0
            else:
                time += quantum
                job.remaining -= quantum
            if job.remaining == 0 and job.finished == False:
                job.finished = True
                job.turnaround_time = time - job.arrival_time
                job.wait_time = job.turnaround_time - job.burst_time
                total -= 1
                jobTime(job)
    averageTime(schedule)


def SRTN(schedule):
    time = 0




def jobTime(job):
    print("Job %3d -- Turnaround %3.2f Wait %3.2f" % (job.process_number, job.turnaround_time, job.wait_time))

def averageTime(schedule):
    turnaround = 0
    wait = 0
    for job in schedule:
        turnaround += job.turnaround_time
        wait += job.wait_time
    turnaround = turnaround / len(schedule)
    wait = wait / len(schedule)

    print("Average -- Turnaround %3.2f Wait %3.2f" % (turnaround, wait))

def main():
    if (len(sys.argv) < 2 or len(sys.argv) % 2 != 0):
        print("Input: python3 schedSim <job-file.txt> -p <ALGORITHM> -q <QUANTUM>")
        print("-p and -q are optional but required if picking a algorithm or quantum")
        print("-p options are 'FIFO' 'RR' 'SRTN' default is FIFO")
        print("-q is optional and only for round robin default is 1")
        sys.exit()

    algorithm = getAlgorithm()
    quantum = getQuantum()
    schedule = scheduleSetup()

    if algorithm == "FIFO":
        FIFO(schedule)
    elif algorithm == "RR":
        RR(schedule, quantum)
    elif algorithm == "SRTN":
        SRTN(schedule)


    for job in schedule:
        print(job.process_number)
        schedule.remove(job)
        for jobs in schedule:
            print(jobs.process_number)
            print(" ")



if __name__ == "__main__":
    main()