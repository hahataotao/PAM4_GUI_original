from aardvark_py import *
from time import sleep,clock
import sys
import string
I2C_BITRATE     = 400   # I2C bit rate, normally 400 [kHz]
BUS_TIMEOUT     = 150   # [ms]
QSFP_I2C_ADDR   = 0x50
Rx_Eval_CDR_addr=0x18
MAX_PAGE        = 30

handle = 0
class AardVark_control(object):
     def __init__(self):
        pass
     def detectAardVark(self):
        print("Detecting Aardvark adapters...")

        # Find all the attached devices
        msg=""
        (num, ports, unique_ids) = aa_find_devices_ext(16, 16)
        if num > 0:
            print("%d device(s) found:" % num)

            # Print the information on each device
            for i in range(num):
                port = ports[i]
                unique_id = unique_ids[i]

                # Determine if the device is in-use
                inuse = "(free)"
                if (port & AA_PORT_NOT_FREE):
                    inuse = "(occupied)"
                    port = port & ~AA_PORT_NOT_FREE

                    # Display device port number, in-use status, and serial number
                msg=msg+str(port) + " "+ inuse+" "+ str(unique_id / 1000000) +"--"+ str(unique_id % 1000000) +'\n'
            return (msg)
        else:
            return ("No device found!")

     def i2c_write(self,data):
         data_out = array('B', data)
         ret = aa_i2c_write(handle, QSFP_I2C_ADDR, AA_I2C_NO_FLAGS, data_out)
         return ret

     def i2c_write_eval(self, data):
         data_out = array('B', data)
         ret = aa_i2c_write(handle,  Rx_Eval_CDR_addr>>1, AA_I2C_NO_FLAGS, data_out)
         return ret

     def i2c_read_eval(self,nbytes):
         (count, data_in) = aa_i2c_read(handle, Rx_Eval_CDR_addr>>1, AA_I2C_NO_FLAGS, nbytes)
         if count != nbytes:
             print "error: i2c_read: aa_i2c_read returned %d (expected %d)" % (count, nbytes)
             data_in = []
         return data_in

     def i2c_read(self,nbytes):
         (count, data_in) = aa_i2c_read(handle, QSFP_I2C_ADDR, AA_I2C_NO_FLAGS, nbytes)
         if count != nbytes:
             print "error: i2c_read: aa_i2c_read returned %d (expected %d)" % (count, nbytes)
             data_in = []
         return data_in

     def write_password(self):
         # QSFP-DD: 122-125
         wrdat = [122, 0xab, 0xcd, 0x12, 0x34]
         data_out = array('B', wrdat)
         rc = self.i2c_write(data_out)


     def openQSFPddAA(self):
        global handle
        (num, ports, unique_ids) = aa_find_devices_ext(16, 16)
        if num < 1:
            print "error: No Aardvarks found"
            return False
        #pick AAid port number
        port = ports[0]
        if (port & AA_PORT_NOT_FREE):
            print "error: Aardvark on port %d already open" % port
            return False

        print '%d Aardvark%s found, using #0' % (num, (num > 1 and 's' or ''))
        handle = aa_open(port)
        if (handle <= 0):
            print "error: Can't open Aardvark on port %d" % port
            return False

        # Ensure that the I2C subsystem is enabled, set bitrate and bus lock timeout
        aa_configure(handle, AA_CONFIG_GPIO_I2C)
        bitrate = aa_i2c_bitrate(handle, I2C_BITRATE)
        bus_timeout = aa_i2c_bus_timeout(handle, BUS_TIMEOUT)

        # Dump the page(s)
        self.write_password()
        wrbuf = [127, 0x08]  # set page pointer
        self.i2c_write(wrbuf)
        return True
     def closeQSFPddAA(self):
        aa_close(handle)
        return True
     #need to select bus first before talking to CDR
     def selectI2CBus(self,bus):

        if bus > 1:
            bus = 1
        wrbuf = [225, bus]  # set I2C bus number
        self.i2c_write(wrbuf)
        # wrbuf = [226, dev]  # set I2C device address
        # self.i2c_write(wrbuf)
        # wrbuf = [227, reg]  # set I2C register address
        # self.i2c_write(wrbuf)
        print "Select Bus %d "% (bus)

    #all input variables to hex format
     def write2CDR(self,bus,deviceAddr,regaddr,data):
         wrbuf = [127, 0x08]  # set page pointer
         self.i2c_write(wrbuf)
         dev = deviceAddr & 0xff
         reg = regaddr & 0xff
         dat = data & 0xff

         if bus > 1:
             bus = 1
         wrbuf = [225, bus]  # set I2C bus number
         self.i2c_write(wrbuf)
         wrbuf = [226, dev]  # set I2C device address
         self.i2c_write(wrbuf)
         wrbuf = [227, reg]  # set I2C register address
         self.i2c_write(wrbuf)

         wrbuf = [228, dat]  # set I2C register data
         self.i2c_write(wrbuf)
         wrbuf = [224, 1]  # start I2C write
         self.i2c_write(wrbuf)
         wrbuf = [224]  # poll write op for completion
         self.i2c_write(wrbuf)
         rdbuf = self.i2c_read(1)
         count = 0
         while (rdbuf[0] != 0):
             count = count + 1
             self.i2c_write(wrbuf)
             rdbuf = self.i2c_read(1)
        # print count
         print "Write to Device 0x%02x reg 0x%02x: 0x%02x" % (dev, reg, dat)

     def write2CDREval(self,regaddr, data):
         reg = regaddr & 0xff
         dat = data & 0xff
         wrbuf = [reg, dat]  # set I2C register address  # set I2C register data
         self.i2c_write_eval(wrbuf)
         print "Write to reg 0x%02x: 0x%02x" % ( reg, dat)

     def readfromCDREval(self, regaddr):
         reg = regaddr & 0xff
         wrbuf = [reg]  # set I2C register address
         self.i2c_write_eval(wrbuf)
         rdbuf = self.i2c_read_eval(1)
         count = 0
         # while (rdbuf[0] != 0):
         #     count = count + 1
         #     self.i2c_write_eval(wrbuf)
         #     rdbuf = self.i2c_read_eval(1)
         dat = rdbuf[0]
         # print ""Bus %d device 0x%02x reg 0x%02x: 0x%02x"" % (bus, dev, reg, dat)
         return dat
         # print ""Device 0x%02x reg 0x%02x: 0x%02x"" % (bus, dev, reg, dat)"

     def readfromCDR(self,regaddr):

         reg = regaddr & 0xff
         wrbuf = [reg]  # set I2C register address
         self.i2c_write(wrbuf)


         wrbuf = [224, 2]  # start I2C read
         self.i2c_write(wrbuf)
         wrbuf = [224]  # poll write op for completion
         self.i2c_write(wrbuf)
         rdbuf = self.i2c_read(1)
         count = 0
         while (rdbuf[0] != 0):
             count = count + 1
             self.i2c_write(wrbuf)
             rdbuf = self.i2c_read(1)
         wrbuf = [228]  # get I2C data result
         self.i2c_write(wrbuf)
         rdbuf = self.i2c_read(1)
         dat = rdbuf[0]
         #print "Bus %d device 0x%02x reg 0x%02x: 0x%02x" % (bus, dev, reg, dat)
         return dat
         #print "Device 0x%02x reg 0x%02x: 0x%02x" % (bus, dev, reg, dat)
     #
def main():
    AACtrl=AardVark_control()
    AACtrl.openQSFPddAA()    #open COM port, page #
    AACtrl.selectI2CBus(0)  #set select port
    startTime=clock()
    AACtrl.write2CDR(0,0x18,0xff,0x00)    #set page number verify chip ID 54, 0x14 d6
    print "Read value=" + str(hex(AACtrl.readfromCDR(0,0x18,0x00)))
    AACtrl.closeQSFPddAA()
    finishTime=clock()
    print "Elapsed time " + str(finishTime-startTime)
if __name__ == "__main__":
     main()

