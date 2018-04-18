import os
import json
from AardVark_control import AardVark_control
import serial
from time import sleep, time,clock
from PyQt4 import QtGui,QtCore
from decimal import Decimal
import random

class rxCDRaddrMapping():

    def __init__(self):
        # hex value set in dictionary   #can reduce testing channel
        self.channelPageNo = {'Ch0': 0x20, 'Ch1': 0x21, 'Ch2': 0x22, 'Ch3': 0x23}
        self.ErrCounterCtrlAddr = 0xB0
        self.errCounterAddr = {'A1': 0xB4, 'A2': 0xB5, 'B1': 0xB6, 'B2': 0xB7}


class gatingWorker(QtCore.QObject):
    'Object managing the simulation'

    countErr = QtCore.pyqtSignal(str)
    calcBER= QtCore.pyqtSignal(str)
    elapsedTime= QtCore.pyqtSignal(str)
    transmittedBits=QtCore.pyqtSignal(str)
    #model is using for update GUI from Controllers
    def __init__(self,initFileDirectory, initFileName,model=None,AA=None,serialPortCtrl=None):
        super(gatingWorker, self).__init__()
        self._isRunning = False
        self._errorCount=[0]*4
        self._ber=[-1]*4
        self._totalErrCount=[0]*4
        self.totalRunningTime=[0]*4
        self._getSettingFromInitFile(initFileDirectory, initFileName)
        self.model=model
        self.AA=AA
        self.serialPortCtrl=serialPortCtrl
        self.model.timeElapsed=0
        self._totalbitsTransmitted=0


    def _getSettingFromInitFile(self, initFileDirectory, filename):
        with open(initFileDirectory + filename, 'r') as data_file:
            self.initData = json.load(data_file)
        self.berSelectBusNo = self.initData["BERTestHardwareConfiguration"]["berSelectedBusNo"]
        self.cdrDeviceAddr = self.initData["BERTestHardwareConfiguration"]["cdrBERDeviceAddr"]
        self.dataRatePAM4 = self.initData["BERTestHardwareConfiguration"]["dataRate"]
        self.channelWaitTime=self.initData["BER_TestMode"]["channelWaitTime"]
        self.pageCtrlAddr=0xff

    def task(self):
        if not self._isRunning:
            self._isRunning = True
            self.rxCDR=rxCDRaddrMapping()
            self.allChanneltime=0
            self._totalTransmittedBits=0
            self.timeCalOffset=0.07     #line code running time offset
            #reset BER and error counter
            for i in range(4):
                self._ber[i] =0
                self._errorCount[i] =0
                self._totalErrCount[i]=0
                self.totalRunningTime[i]=0
            #select bus for talking which side CDR
            self.AA.selectI2CBus(self.berSelectBusNo)
        #all print statement can be used as debug or log into log file
        while self._isRunning == True:
            #initialize section for preparing BER ,update GUI widget from model
            #Read error counter and calculate BER for four channel
            self.realGatingStartTime=clock()
            # self.AA.write2CDREval(0xff, 0)
            # q=self.AA.readfromCDREval(0)
            for i,ch in enumerate(self.rxCDR.channelPageNo.keys()):

                # self.AA.write2CDR(self.berSelectBusNo,self.cdrDeviceAddr, self.pageCtrlAddr,self.rxCDR.channelPageNo[ch])  # select pageNo for error counter read
                # self.AA.write2CDR(self.berSelectBusNo, self.cdrDeviceAddr,self.rxCDR.ErrCounterCtrlAddr,0x05)    #Reset the counter
                # self.AA.write2CDR(self.berSelectBusNo, self.cdrDeviceAddr, self.rxCDR.ErrCounterCtrlAddr,0x01)  # Release the reset
                self.AA.write2CDREval(self.pageCtrlAddr,self.rxCDR.channelPageNo[ch])
                self.AA.write2CDREval(self.rxCDR.ErrCounterCtrlAddr,0x05)    #Reset the counter
                self.AA.write2CDREval(self.rxCDR.ErrCounterCtrlAddr,0x01)  # Release the reset
                startTime = clock()
                sleep(self.channelWaitTime)
                print("Gating window waiting time is "+ str(self.channelWaitTime))
                #self.AA.write2CDR(self.berSelectBusNo, self.cdrDeviceAddr, self.rxCDR.ErrCounterCtrlAddr,0x09)  # Freeeze the counters
                self.AA.write2CDREval(self.rxCDR.ErrCounterCtrlAddr,0x09)  # Freeeze the counters
                finishTime = clock()
                #after error counter frozen and start counting error from all counter register
                print("use page Ctrol =0x%02x, pageNo=0x%02x" %(self.pageCtrlAddr,self.rxCDR.channelPageNo[ch]))
                #read error counter one by one
                for j,errcnt in enumerate(self.rxCDR.errCounterAddr.keys()):
                    self._errorCount[j]=self.AA.readfromCDREval(self.rxCDR.errCounterAddr[errcnt])
                    self._totalErrCount[i] += self._errorCount[j]
                    print("ErrCountAddr=0x%02x, Value=%d" % \
                          (self.rxCDR.errCounterAddr[errcnt], self._errorCount[j]))
                self.totalRunningTime[i]+=(finishTime-startTime)
                print("Ch" + str(i)+ ", TotalError=" + str(self._totalErrCount[i])+ " ,TimeElapsed=" + str(round(self.totalRunningTime[i],4))+ " seconds")
            self.realGatingFinishTime=clock()

            self.updateValueOnDisplay()
            #print "Elapsed time " + str(finishTime - startTime)
        print "Gating is finished and exit!"
    def loggingDataIntoExcelFile(self):
        pass

    def loggingDataIntoSQLDatabase(self):
        pass

    def updateValueOnDisplay(self):
        self.model.Ch0totalError = self._totalErrCount[0]
        self.model.Ch1totalError = self._totalErrCount[1]
        self.model.Ch2totalError = self._totalErrCount[2]
        self.model.Ch3totalError = self._totalErrCount[3]
        for i in range(4):
            self._ber[i] = self._totalErrCount[i] / self.totalRunningTime[i] / self.dataRatePAM4
        self.model.ch0BER = self._ber[0]
        self.model.ch1BER = self._ber[1]
        self.model.ch2BER = self._ber[2]
        self.model.ch3BER = self._ber[3]

        self.countErr.emit(str(self.model.Ch0totalError))
        self.countErr.emit(str(self.model.Ch1totalError))
        self.countErr.emit(str(self.model.Ch2totalError))
        self.countErr.emit(str(self.model.Ch3totalError))
        # convert to scientific notation number
        self.calcBER.emit(str(self.model.ch0BER))
        self.calcBER.emit(str(self.model.ch1BER))
        self.calcBER.emit(str(self.model.ch2BER))
        self.calcBER.emit(str(self.model.ch3BER))
        # display the real gating time ignoring error counter in frozen state

        # for i in range(4):
        #     self.allChanneltime = self.totalRunningTime[i]

        # elapsed time should be module total running time when turning on gating mode ,comment out last calculation
        self.allChanneltime += self.realGatingFinishTime - self.realGatingStartTime + self.timeCalOffset
        self.model.timeElapsed = int(self.allChanneltime)
        self.elapsedTime.emit(str(self.model.timeElapsed))
        self._totalTransmittedBits = round(self.allChanneltime * self.dataRatePAM4, 0)
        self.model.transmittedBits = self._totalTransmittedBits
        self.transmittedBits.emit(str(self.model.transmittedBits))
        QtGui.QApplication.processEvents()

    def simulatingTask(self):
        if not self._isRunning:
            self._isRunning = True
            self.rxCDR = rxCDRaddrMapping()
            self.allChanneltime = 0
            self._totalTransmittedBits = 0
            self.timeCalOffset = 0.07  # line code running time offset
            # reset BER and error counter
            for i in range(4):
                self._ber[i] = 0
                self._errorCount[i] = 0
                self._totalErrCount[i] = 0
                self.totalRunningTime[i] = 0
            # select bus for talking which side CDR

        # all print statement can be used as debug or log into log file
        while self._isRunning == True:
            # initialize section for preparing BER ,update GUI widget from model
            # Read error counter and calculate BER for four channel
            self.realGatingStartTime = clock()
            for i, ch in enumerate(self.rxCDR.channelPageNo.keys()):

                startTime = clock()
                sleep(self.channelWaitTime)
                print("Gating window waiting time is " + str(self.channelWaitTime))
                finishTime = clock()
                # after error counter frozen and start counting error from all counter register

                # read error counter one by one

                self._totalErrCount[i] += random.randint(1,100000)

                finishTime = clock()
                self.totalRunningTime[i] += (finishTime - startTime)
                print("Ch" + str(i) + ", TotalError=" + str(self._totalErrCount[i]) + " ,TimeElapsed=" + str(
                    round(self.totalRunningTime[i], 1)) + " seconds")
            self.realGatingFinishTime = clock()

            self.updateValueOnDisplay()
            # print "Elapsed time " + str(finishTime - startTime)
        print "Gating is finished and exit!"

    def stop(self):
        self.model.timeElapsed=0
        self._isRunning = False

class MainController(object):
    def __init__(self,initFileDirectory, initFileName,model=None,):
        self.model = model
        self.initFileDirectory=initFileDirectory
        self.initFileName=initFileName
        print('read configuration from setting file')
        self._getSettingFromInitFile(initFileDirectory, initFileName)
        #self.openAttrCOMPort()

    # called from view class
    def change_running(self, checked):
        # put control logic here
        self.model.running = checked
        self.model.announce_update()

    def dummyTestGating(self):
        print('Start BER gating!')
        print('Gating Start ,calculate and display Bit Error Rate matters')
        self.worker = gatingWorker(self.initFileDirectory, self.initFileName,self.model)
        self.thread = QtCore.QThread()
        # self.QSFPddAAID.write2CDR(self.berSelectBusNo, self.cdrDeviceAddr, 0xff, rxCDRaddrMapping.ch0errCnt['page'])  # set and select ch0 BER check page
        # logic algorithm to calculate BER
        # self.model.ch0BER=random.randint(1,5)

        self.worker.moveToThread(self.thread)

        self.worker.countErr.connect(self.model.announce_update)
        self.worker.calcBER.connect(self.model.announce_update)
        self.worker.simulatingTask()
        # print "Read value=" + str(hex(AACtrl.readfFromCDR(0, 0x18, 0x14)))
        # print "Elapsed time " + str(finishTime - startTime)

    # handle sensitivity mneasurement logic
    def startGating(self):
        print('Start BER gating!')
        print('Gating Start ,calculate and display Bit Error Rate matters')
        self.worker=gatingWorker(self.initFileDirectory,self.initFileName,self.model,self.QSFPddAAID,self.serialAttr)
        self.thread=QtCore.QThread()
        #self.QSFPddAAID.write2CDR(self.berSelectBusNo, self.cdrDeviceAddr, 0xff, rxCDRaddrMapping.ch0errCnt['page'])  # set and select ch0 BER check page
        # logic algorithm to calculate BER
        #self.model.ch0BER=random.randint(1,5)

        self.worker.moveToThread(self.thread)

        self.worker.countErr.connect(self.model.announce_update)
        self.worker.calcBER.connect(self.model.announce_update)
        self.worker.task()
        #print "Read value=" + str(hex(AACtrl.readfFromCDR(0, 0x18, 0x14)))
        #print "Elapsed time " + str(finishTime - startTime)
    def stopGating(self):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()

        print('Stop BER gating!')
        print('Gating Stop, finish all the calculation and display result')

    # called from view class
    def attrValueChange(self, value):
        # put control logic here
        size = float(value) / 2  # self.slsetAttr.value()

        # output=self.serialAttr.read()
        self.serialAttr.write("A" + str(size) + '\r\n')
        sleep(1)
        print("Sending command A%.1f and set attenuator " % size)
        value=round(size, 1)
        self.model.changedValue=value*2
        self.model.announce_update()
    def dummyTestAttrValueChange(self,value):
        size = float(value) / 2  # self.slsetAttr.value()

        # output=self.serialAttr.read()
        print("Sending command A%.1f and set attenuator " % size)
        value = round(size, 1)
        self.model.changedValue = value*2
        self.model.announce_update()


    def _getSettingFromInitFile(self, initFileDirectory, filename):
        with open(initFileDirectory + filename, 'r') as data_file:
            self.initData = json.load(data_file)
        self.attrCOMName = self.initData["BERTestHardwareConfiguration"]["attenuatorCOMPort"]
        self.attrCOMRateSelect = self.initData["BERTestHardwareConfiguration"]["attenuatorCOMPortRateSelect"]
        self.berAAID = self.initData["BERTestHardwareConfiguration"]["berAArdvarkID"]
        self.berRateSelect = self.initData["BERTestHardwareConfiguration"]["berAArdVarkRateSelectKhz"]
        self.testModeSelect= self.initData["BER_TestMode"]["testModeSelect"]
        self.testBERMode=self.initData["BER_TestMode"]["testModeSelect"]
        # self.berSelectBusNo=self.initData["BERTestHardwareConfiguration"]["berSelectedBusNo"]
        # self.cdrDeviceAddr=self.initData["BERTestHardwareConfiguration"]["cdrBERDeviceAddr"]
        # self.dataRatePAM4=self.initData["BERTestHardwareConfiguration"]["dataRate"]


    def openQSFPddAAID(self):
        self.QSFPddAAID = AardVark_control()
        if self.QSFPddAAID.openQSFPddAA():
            print('open AA successfully and module unlocked')
            return True
        else:
            print ("Failed open AArdvark and unlock QSFPDD")
            return False

    def closeQSFPddAAID(self):
        self.QSFPddAAID.closeQSFPddAA()
        print('QSFPdd AA ID is closed succesfully')

    def openAttrCOMPort(self):
        # configure the serial connections (the parameters differs on the device you are connecting to)
        self.serialAttr = serial.Serial(
            port=self.attrCOMName,
            baudrate=self.attrCOMRateSelect,
            # parity=serial.PARITY_ODD,
            # stopbits=serial.STOPBITS_TWO,
            # bytesize=serial.EIGHTBITS,
            # timeout = 2,  # non-block read
            # xonxoff = False,  # disable software flow control
            # rtscts = False,  # disable hardware (RTS/CTS) flow control
            # dsrdtr = False,  # disable hardware (DSR/DTR) flow control
            # writeTimeout = 2  # timeout for write
        )
        # try:
        #     self.serialAttr.open()
        #     print("Port Opened")
        # except Exception, e:
        #     print "error open serial port: " + str(e)
        #     return False

        #  use isOpen() in place of open()
        if self.serialAttr.isOpen():

            try:
                self.serialAttr.flushInput()  # flush input buffer, discarding all its contents
                self.serialAttr.flushOutput()  # flush output buffer, aborting current output
                # and discard all that is in buffer
                print("Fluash out all gabage is completed successfully")
                sleep(0.5)  # give the serial port sometime to receive the data
                return True

            except Exception, e1:
                print "error communicating...: " + str(e1)
                self.serialAttr.close()

        else:
            print "cannot open serial port "
            self.serialAttr.close()
            return False

    def closeAttrCOMPort(self):
        self.serialAttr.close()
        print('Attenuator COM port is closed!')





    def plotGraph(self):
        pass





if __name__ == '__main__':
    pass

