'''
Created on Feb 16, 2014

@author: tgdscm41
'''
import random

from wrapper_log import loghandle
from bitoperation import bitoperation

         
class hwIF_stub(object):

    def __init__(self,i2cAddr = 0x20):
        
        self._loghandle = loghandle()

  #      self._loghandle.info('mcp23017Driver::init, Object created: Version: %s, Date: %s',__VERSION__,__DATE__)   
  #      self._loghandle.debug('Start DeviceSimulator i2c Address: %s',i2cAddr)
   #     self._i2cAdd = i2cAddr
        
    def ConfigIO(self,ioPin,iodir):
        """ Setup ioPin configuration
            ioPin = pin 0...15 as integer
            iodir = 0 output / 1 input
        """
        self._loghandle.info('simulator::ConfigIO, i2cAddress: %s Pin-number: %d Direction: %s',self._i2cAdd,ioPin,iodir)
        
        return True
    
    def WritePin(self,ioPin,value):
        
        self._loghandle.info('simulator::WritePin, i2cAddress: %s Pin-number: %d Value: %s',self._i2cAdd,ioPin,value)
        
        return True
    
    def ReadPin(self,ioPin):
              
        value = random.randint(0,1) 
        self._loghandle.info('simulator::ReadPin, i2cAddress: %s Pin-number: %d Value: %s',self._i2cAdd,ioPin,value)
        return value
    
 