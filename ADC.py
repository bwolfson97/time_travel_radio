#!/usr/bin/env python3
########################################################################
# Filename    : ADC.py
# Description : Use ADC module to read the voltage value of potentiometer.
# Author      : www.freenove.com
# modification: 2020/03/06
########################################################################
import time
#!/usr/bin/env python3
########################################################################
# Filename    : ADCDevice.py
# Description : Freenove ADC Module library.
# Author      : www.freenove.com
# modification: 2020/04/21
########################################################################

import smbus

class ADCDevice(object):
    def __init__(self):
        self.cmd = 0
        self.address = 0
        self.bus=smbus.SMBus(1)
        # print("ADCDevice init")
        
    def detectI2C(self,addr):
        try:
            self.bus.write_byte(addr,0)
            print("Found device in address 0x%x"%(addr))
            return True
        except:
            print("Not found device in address 0x%x"%(addr))
            return False
            
    def close(self):
        self.bus.close()

class ADS7830(ADCDevice):
    def __init__(self):
        super(ADS7830, self).__init__()
        self.cmd = 0x84
        self.address = 0x4b # 0x4b is the default i2c address for ADS7830 Module.   
        
    def analogRead(self, chn): # ADS7830 has 8 ADC input pins, chn:0,1,2,3,4,5,6,7
        value = self.bus.read_byte_data(self.address, self.cmd|(((chn<<2 | chn>>1)&0x07)<<4))
        return value

adc = ADCDevice() # Define an ADCDevice class object

def setup():
    global adc
    if(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n");
        exit(-1)
        
def loop():
    while True:
        value = adc.analogRead(0)    # read the ADC value of channel 0
        voltage = value / 255.0 * 3.3  # calculate the voltage value
        print ('ADC Value : %d, Voltage : %.2f'%(value,voltage))
        time.sleep(0.1)

def destroy():
    adc.close()
    
if __name__ == '__main__':   # Program entrance
    print ('Program is starting ... ')
    try:
        setup()
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()
        
    
