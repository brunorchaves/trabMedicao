"""
ldr.py
Display analog data from Arduino using Python (matplotlib)
Author: Mahesh Venkitachalam
Website: electronut.in
"""

import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque

import matplotlib.pyplot as plt 
import matplotlib.animation as animation

    
# plot class
class AnalogPlot:
  # constr
    def __init__(self, strPort, maxLen):
        # open serial port
        self.ser = serial.Serial(strPort, 115200)

        self.maxLen = maxLen
        self.plot_data = [[], [], [], []]

        plt.style.use("ggplot")
        self.fig = plt.figure(figsize=(10, 5))
        ax = plt.axes(xlim=(0, 100), ylim=(0, 1023))

        self.lines = []
        self.lines.append(ax.plot([], [], 'red', label='Tensão')[0])
        self.lines.append(ax.plot([], [], 'gray', label='Corrente')[0])
        self.lines.append(ax.plot([], [], 'blue', label='Temperatura')[0])
        self.lines.append(ax.plot([], [], 'green', label='Luminosidade')[0])
        ax.legend(loc='upper right')


  # update plot
    def update(self, frameNum):
        try:
            line = self.ser.readline()
            print(line)
            data = [int(val) for val in line.split()]
            # print data
            if(len(data) == 4):
                for idx, val in enumerate(data):                    
                    #print(data[0])
                    self.plot_data[idx].append(val)
                    if len(self.plot_data[idx]) > self.maxLen:
                        self.plot_data[idx].pop(0)
                    
                    self.lines[idx].set_data(range(len(self.plot_data[idx])), self.plot_data[idx])
            
        except KeyboardInterrupt:
            print('exiting')
        except Exception as e:
            print("An exception occurred")
            print(self.lines[0])
            print(e)


    # clean up
    def close(self):
        # close serial
        self.ser.flush()
        self.ser.close()    

# main() function
def main():
    # create parser
    parser = argparse.ArgumentParser(description="LDR serial")
    # add expected arguments
    parser.add_argument('--port', dest='port', required=True)

    # parse args
    args = parser.parse_args()
    
    #strPort = '/dev/tty.usbserial-A7006Yqh'
    strPort ="COM5"

    print('reading from serial port %s...' % strPort)

    # plot parameters
    print(strPort)
    print(type(strPort))
    analogPlot = AnalogPlot(strPort, 100)

    print('plotting data...')

    anim = animation.FuncAnimation(analogPlot.fig, analogPlot.update, interval=50)

    # show plot
    plt.show()
    
    # clean up
    analogPlot.close()

    print('exiting.')
  

# call main
if __name__ == '__main__':
    main()