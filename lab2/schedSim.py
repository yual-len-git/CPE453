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
    running = []
    arrival = []
    time = 0
    for process in schedule:
        running.append(process.process_number)
        arrival.append(process.arrival_time)

    count = 1
    while running:
        for jobs in schedule:
            if jobs.finished == False:
                current = jobs
            else:
                continue
            for job in schedule:
                if job.finished == True:
                    continue
                elif job.arrival_time <= current.arrival_time or time >= job.arrival_time:
                    if job.burst_time <= current.burst_time and job.arrival_time <= current.arrival_time:
                        current = job

            # print(str(count) + " " + str(current.process_number))
            print("count: %d pn: %d time: %d arrival: %d" % (count, current.process_number, time, current.arrival_time))
            count += 1

            if arrival:
                for i in arrival:
                    if i == time:
                        arrival.remove(time)
                    print("Arrival: %d" % i)

                if time >= current.arrival_time:
                    time += 1
                    current.remaining -= 1
                else:
                    time += 1
                
            else:
                time += current.remaining
                current.remaining = 0

            print(str(current.process_number) + str(current.remaining))

            if current.remaining == 0 and current.finished == False:
                current.finished = True
                running.remove(current.process_number)
                current.wait_time = time - current.arrival_time - current.burst_time
                current.turnaround_time = time - current.arrival_time




    # for jobs in schedule:
    #     current = jobs
    #     for job in schedule:
    #         if job.process_number not in running:
    #             continue
    #         elif current.arrival_time == job.arrival_time:
    #             if current.burst_time > job.burst_time:
    #                 current = job

    #         # if arrival:
    #         #     for i in arrival:
    #         #         if i == time:
    #         #             arrival.remove(i)
    #         #     time += 1
    #         #     current.remaining -= 1
    #         # else:
    #         time += current.remaining
    #         current.remaining = 0

    #         # time += current.remaining
    #         # current.remaining = 0
        

    #     if current.remaining == 0 and current.finished == False:
    #         current.finished = True
    #         running.remove(current.process_number)
    #         current.wait_time = time - current.arrival_time - current.burst_time
    #         current.turnaround_time = time - current.arrival_time



    for job in schedule:
        jobTime(job)
    averageTime(schedule)


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

    for i in schedule:
        print(str(i.process_number) + " " +str(i.arrival_time) + " " + str(i.burst_time))

    if algorithm == "FIFO":
        FIFO(schedule)
    elif algorithm == "RR":
        RR(schedule, quantum)
    elif algorithm == "SRTN":
        SRTN(schedule)




if __name__ == "__main__":
    main()