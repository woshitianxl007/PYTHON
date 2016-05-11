# coding:utf-8
import math
from decimal import Decimal

class TraceList:
    # Construction method
    def __init__(self, list):
        self.tracelist = list
    # Print the tracelist[num]:length,
    def PrintTrace(self, num):
        #if the trace-num has two or more elements:
        #else if trace-num has one element:
        #else if trace-num is empty:
        if (len(self.tracelist[num]) > 1):
            # The length of trace-num
            self.length = 0.00
            # The all length of trace-num
            self.lengths = 0.00
            # The longest Segment of trace-num
            self.longestSegment = 0.00
            # The allSamplingRate of trace-num
            self.allSamplingRate = 0.00
            # The collection of likely mode
            self.modesList = []
            # the templist of tract-num
            temp = self.tracelist[num]
            # compute the data of trace-num
            for i in range(1, len(temp)):
                if (temp[i]):
                    self.length = self.CountDistance(temp[i], temp[i - 1])
                    # compute the sum(every length of trace-num)
                    self.lengths += self.length
                    #if this length > longestSegment then replace the longestSegment
                    if (self.length > self.longestSegment):
                        self.longestSegment = self.length
                    rate =temp[i][2] - temp[i - 1][2]
                    # compute the sum(every rate of trace-num)
                    self.allSamplingRate += rate
                    # Impossible situation: rate <= 0
                    if rate > 0:
                        # get the speed between trace-num[i-1] and trace-num[i]
                        self.speed = Decimal(self.length / rate * 18 / 5).quantize(Decimal('0.00'))
                        # the likely mode insert into modeslist
                        if (self.length <> 0):
                            if (self.speed > 20):
                                self.modesList.append("motorised")
                            else:
                                self.modesList.append("non-motorised")
            # print the data of trace-num
            print "Trace " + str(num + 1) + "'s length is " \
                  + str(Decimal(self.lengths).quantize(Decimal('0.00'))) \
                  + "m, the length of its longest segment is " \
                  + str(Decimal(self.longestSegment).quantize(Decimal('0.00'))) \
                  + "m, its sampling rate is " \
                  + str(Decimal(self.allSamplingRate / (len(self.tracelist[num]) - 1)).quantize(Decimal('0.00'))) \
                  + "s, and the likely modes are " \
                  + str(self.modesList) \
                  + "."
        elif (len(self.tracelist[num]) == 1):
            print "Trace " + str(num + 1) + " consists of a single point."
        elif (len(self.tracelist[num]) < 1):
            print "Trace " + str(num + 1) + " has no points!"
        print "- - - - -"

    # Output:1.The total length 2.The shortest distance between the last two traces
    def PrintTotal(self):
        # The collection of template traces
        self.findTrace = []
        # The total length
        self.countLength = 0.00
        # The shortest distance between the last two traces
        self.shortestDistance = 0.00
        self.tempDistance = 0.00
        #loop the every trace
        for temp in self.tracelist:
            for i in range(1, len(temp)):
                if temp[i]:
                    ## compute the sum(every  length of trace)
                    self.countLength += self.CountDistance(temp[i], temp[i - 1])
                    if (i is len(temp) - 1):
                        # get the last traces, insert into findTrace
                        self.findTrace.append(temp[i])
        #two loop can get each distance between the last two traces
        for i in range(0, len(self.findTrace)):
            for j in range(i + 1, len(self.findTrace)):
                self.tempDistance = self.CountDistance(self.findTrace[j], self.findTrace[i])
                if (self.tempDistance < self.shortestDistance or self.shortestDistance == 0):
                    # get shortestDistance between findTrace[j] and self.findTrace[i]
                    self.shortestDistance = self.CountDistance(self.findTrace[j], self.findTrace[i])
        print "The total length of all traces is " + str(Decimal(self.countLength).quantize(Decimal('0.00'))) + "m."
        print "The shortest distance between the last two traces is " + str(Decimal(self.shortestDistance).quantize(Decimal('0.00'))) + "m."

    # compute the distance between trace1 and trace2
    # d^2 = (x1-x2)^2+(y1-y2)^2
    def CountDistance(self, trace1, trace2):
        return math.sqrt(
                (trace1[0] - trace2[0]) * (trace1[0] - trace2[0]) + (trace1[1] - trace2[1]) * (trace1[1] - trace2[1]))

if __name__ == "__main__":
    # bulid a list of GPS traces
    list = [[[0, 0, 0], [1000, 0, 600]],
            [],
            [[1000, 1000, 120]],
            [[0, 0, 0], [3000, 4000, 300], [3000, 4000, 720], [0, 0, 1020]],
            [[150, 0, 0], [1000, 0, 360], [4000, 4000, 660], [4000, 4000, 960], [100, 0, 1320]]]
    f = TraceList(list)
    #This method print the informations of each trace
    for i in range(0, len(f.tracelist)):
        f.PrintTrace(i)
    #This method print the total length and the shortest distance
    f.PrintTotal()