import time as timer
import csv
import json
from MRTD import decode, encode

#this file tests the speed of encode and decode in MRTD.py

def readData(file):
    with open(file) as f:
        data = json.load(f)
    data = data[file[:-5]]
    return data
def testPerformance(file, function):
    #load the files
    print("running: ", file)
    title = file[:-5]# strip ending
    f = open(f'performance_{title}.csv', 'w')
    headers = ["lines read (n)", "time (s)"]
    writer = csv.writer(f)
    writer.writerow(headers)

    data = readData(file)
    iterations =  100
    while iterations <= 10000:
        start = timer.perf_counter()#take time
        for j in range(iterations):#read iterations number of items
            function(data[j])
        stop = timer.perf_counter()#stop time 
        time = stop - start#measure time
        printResult = f"running {iterations} took {time}s"
        result = [iterations, time]
        writer.writerow(result)
        print(printResult)

        if (iterations == 100): 
            iterations = 1000
            continue
        iterations += 1000
    print("done")

testPerformance("records_decoded.json", encode)
testPerformance("records_encoded.json", decode)




