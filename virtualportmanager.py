
import time

from wrapper_log import loghandle

class vpm(object):
    '''
    classdocs
    '''
    def __init__(self, hwHandle, hwDevice, configuration):
        '''
        Constructor
        '''    

        self._hwHandle = hwHandle
        self._hwDevice = hwDevice
        self._loghandle = loghandle()
        
#        self._loghandle.info('Virtuafrom RPIO import PWM


        self._loghandle.debug('virtualport::init Create Object with configuration %s',configuration)
        
        self._config = configuration

#        if any(Device in str for Device in ['23017','SIMULATOR']):
 #       self._DIRECTION = configuration.get('DIRECTION')
  #      self._MODE = configuration.get('MODE')
   #     self._NAME = configuration.get('NAME')
    #    self._HW_ID = int(configuration.get('HW_ID'))
     #   self._OFF_VALUE = configuration.get('OFF_VALUE','OFF')
      #  self._ON_VALUE = configuration.get('ON_VALUE','ON')

        

        
        self._currentPinStatus = 0
        
  #      self.Setup()
        
 #   def Setup(self):
        print self._hwDevice
        self._MODE = configuration.get('MODE','GPIO')
        
        if 'GPIO' in self._MODE:
 #           if any(self._hwDevice in str for self._hwDevice in ['MCP23017','RASPBERRY','SIMULATOR']):
            if any(temp in self._hwDevice for temp in ['MCP23017','RASPBERRY','SIMULATOR']):
                try:
                    self._NAME = configuration.get('NAME')
                    self._HW_ID = int(configuration.get('HW_ID'))
                    self._DIRECTION = configuration.get('DIRECTION')
                except:
                    self._loghandle.critical('VPM::Init Mandatory Parameter missing for Port %s',self._NAME)
                # Optional
                self._savedState = configuration.get('INITIAL',False)
                self._OFF_VALUE = configuration.get('OFF_VALUE','OFF')
                self._ON_VALUE = configuration.get('ON_VALUE','ON')
                self._loghandle.info('VPM::Init Configure Port %s HardwareID %s in Mode %s',self._NAME,self._HW_ID,self._MODE)
                
                if 'IN' in self._DIRECTION:
                    self._hwHandle.ConfigIO(self._HW_ID,1)
                else:
                    self._hwHandle.ConfigIO(self._HW_ID,0)     
              
        elif 'FLASH' in self._MODE:
            ''' Flash mode supports only output '''
     #       if any(self._hwDevice in str for self._hwDevice in ['MCP23017','RASPBERRY','SIMULATOR']):
            if any(temp in self._hwDevice for temp in ['MCP23017','RASPBERRY','SIMULATOR']):
                try:
                    self._NAME = configuration.get('NAME')
                    self._HW_ID = int(configuration.get('HW_ID'))

                except:
                    self._loghandle.critical('VPM::Init Mandatory Parameter missing for Port %s',self._NAME)
                # Optional
                self._DIRECTION = configuration.get('DIRECTION','OUT')
                self._flashMAX = float(configuration.get('MAX',10))
                self._flashMIN = float (configuration.get('MIN',0.5))
                self._INITIAL = configuration.get('INITIAL','LOW')

                self._OFF_VALUE = configuration.get('OFF_VALUE','OFF')
                self._ON_VALUE = configuration.get('ON_VALUE','ON')
            
                # Initial Configuration
                self._flashState = False
                self._hwHandle.ConfigIO(self._HW_ID,0)   
                self._flashFrequency = 2
                self._flashT1 = time.time()
                self._flashT2 = self._flashT1 + self._flashFrequency
            

            
                self._loghandle.info('VirtualPort::Setup Configure Port %s HardwareID %s in Mode %s',self._NAME,self._HW_ID,self._MODE)  
                ''' Startvalue''' 
                if 'LOW' in self._INITIAL:  
                    self._hwHandle.WritePin(self._HW_ID, 0)
                    self._currentPinStatus  = 0
                else:
                    self._hwHandle.WritePin(self._HW_ID, 1)
                    self._currentPinStatus  = 1
            
        elif 'PUSH_BUTTON' in self._MODE:
     #       if any(self._hwDevice in str for self._hwDevice in ['MCP23017','RASPBERRY','SIMULATOR']):
            if any(temp in self._hwDevice for temp in ['MCP23017','RASPBERRY','SIMULATOR']):
                try:
                    self._NAME = configuration.get('NAME')
                    self._HW_ID = int(configuration.get('HW_ID'))

                except:
                    self._loghandle.critical('VPM::Init Mandatory Parameter missing for Port %s',self._NAME)
                # Optional
                self._DIRECTION = configuration.get('DIRECTION','OUT')
                self._PULS_LENGTH = float(configuration.get('PULS_LENGTH',2))
                self._INITIAL = configuration.get('INITIAL','LOW')
                
                self._OFF_VALUE = configuration.get('OFF_VALUE','OFF')
                self._ON_VALUE = configuration.get('ON_VALUE','ON')  
                
                self._hwHandle.ConfigIO(self._HW_ID,0) 
                self._pushButtonState = False
        
        elif 'PWM' in self._MODE:
            if any(temp in self._hwDevice for temp in ['RASPBERRY','SIMULATOR']):
                try:
                    self._NAME = configuration.get('NAME')
                    self._HW_ID = int(configuration.get('HW_ID'))

                except:
                    self._loghandle.critical('VPM::Init Mandatory Parameter missing for Port %s',self._NAME)
                    
                # Optional
                self._DIRECTION = configuration.get('DIRECTION','OUT')
                self._flashMAX = float(configuration.get('MAX',10))
                self._flashMIN = float (configuration.get('MIN',0.5))
                self._INITIAL = configuration.get('INITIAL','LOW')
                
                self._OFF_VALUE = configuration.get('OFF_VALUE','OFF')
                self._ON_VALUE = configuration.get('ON_VALUE','ON')
            
                # Initial Configuration
                self._pwmState = False
                self._hwHandle.ConfigPWM(self._HW_ID)   
  #              self._flashFrequency = 2
  #              self._flashT1 = time.time()
 #               self._flashT2 = self._flashT1 + self._flashFrequency
                    
 #           if any(self._hwDevice in str for self._hwDevice in ['RASPBERRY']):
                self._loghandle.error('VirtualPort::Init Mode %s not supported',self._MODE)  
            
        elif 'DEBOUNCE' in self._MODE:
            if any(temp in self._hwDevice for temp in ['MCP23017','RASPBERRY']):
                try:
                    self._NAME = configuration.get('NAME')
                    self._HW_ID = int(configuration.get('HW_ID'))

                except:
                    self._loghandle.critical('VPM::Init Mandatory Parameter missing for Port %s',self._NAME)
                    
                # Optional
                self._DIRECTION = configuration.get('DIRECTION','IN')
                self._OFF_VALUE = configuration.get('OFF_VALUE','OFF')
                self._ON_VALUE = configuration.get('ON_VALUE','ON')
                self._INITIAL = configuration.get('INITIAL','LOW')
                
                '''
                Setup required variables and set initial configuration
                '''
                self._T0 = 0
                self._T1 = 0
                self._T2 = 0
                
                ''' 
                Setup port as Input
                '''
                self._hwHandle.WritePin(self._HW_ID, 0)
                
            
                self._loghandle.error('VirtualPort::Init Mode %s not supported',self._MODE)  

            
        elif 'S0' in self._MODE:
            if any(temp in self._hwDevice for temp in ['MCP23017','RASPBERRY','SIMULATOR']):
 #           if any(self._hwDevice in str for self._hwDevice in ['MCP23017','RASPBERRY','SIMULATOR']):
                self._loghandle.error('VirtualPort::Init Mode %s not supported',self._MODE)
                
        else:
            self._loghandle.error('VirtualPort::Init MODE not supported!')
            
            
        
    def Get(self):
        result = None
        
        if self._hwHandle.ReadPin(self._HW_ID) == 0:
            self._currentPinStatus  = 0
            result = self._OFF_VALUE
        else:
            self._currentPinStatus  = 1
            result = self._ON_VALUE
        
        return {'State':result}

    def Set(self,value):
 #       print "Received Value:", value, "Configured Value:",self._ON_VALU
#        print "Set port",self._NAME ,"set", value
        if 'GPIO' in self._MODE:
            self._loghandle.info('VirtualPort::Set Mode %s Command %s found for port %s',self._MODE, value,self._NAME)
            self.SetGpio(value)
            
        elif 'FLASH' in self._MODE:
            self._loghandle.info('VirtualPort::Set Mode %s Command %s found for port %s',self._MODE, value,self._NAME)
            self.SetFlash(value)
            
        elif 'PUSH_BUTTON' in self._MODE:
            self._loghandle.info('VirtualPort::Set Mode %s Command %s found for pot %s',self._MODE, value, self._NAME) 
            self.SetPushButton(value)
                               
        elif 'PWM' in self._MODE:
            self._loghandle.info('VirtualPort::Set Mode %s Command %s found for port %s',self._MODE, value,self._NAME)
            self.SetPWM(value)
 #            self._loghandle.crittical('VirtualPort::Set Command %s not currently not supported',value) 
                        
        elif 'DEBOUNCE' in self._MODE:
            self._loghandle.crittical('VirtualPort::Set Command not supported only input') 
                        
        elif 'S0' in self._MODE:
            self._loghandle.crittical('VirtualPort::Set Command %s not currently not supported',value) 
            
        else:
            self._loghandle.crittical('VirtualPort::Set Command %s not supported',value)  
        return True      
            
    def SetGpio(self,value):
        if self._ON_VALUE in value:
            self._hwHandle.WritePin(self._HW_ID, 1)
            self._currentPinStatus  = 1
            self._loghandle.debug('VirtualPort::Set Command %s found for port',value)  
        elif self._OFF_VALUE in value:
            self._hwHandle.WritePin(self._HW_ID, 0) 
            self._currentPinStatus  = 0
            self._loghandle.debug('VirtualPort::Set Command %s found for port',value)  
        else:
            self._loghandle.error('VirtualPort::Set Command %s not found for port',value)  
    
        return True
 
            
    def Update(self):

        savedState = self._savedState
        resultDict = self.Get()
        pinState = resultDict.get('State',None)
        update = False

        if pinState != savedState:
            self._savedState = pinState
            update = True
            self._loghandle.debug('VirtualPort::Update Update available: %s',update)
        else:
            update = False
  #          self._loghandle.debug('VirtualPort::Update Update available: %s',update)
             
        return {'Update':update,'State':pinState}
    
    def SetFlash(self,value):
        
        try: 
            self._flashFrequency = float(value)
            self._loghandle.debug('TEST value %s, MIN %s MAX %s', self._flashFrequency, self._flashMIN, self._flashMAX)
            if self._flashFrequency < self._flashMIN:
#                print "ON"
                self.SetGpio('ON')
                self._flashState = False
                self._loghandle.info('VirtualPort::SetFlash Frequency %s below MIN %s ;Pin %s ON; Flash State %s',self._flashFrequency,self._flashMIN,self._HW_ID,self._flashState)
               # self._hwHandle.WritePin(self._HW_ID, 0)
                #self._currentPinStatus = 0
            elif self._flashFrequency > self._flashMAX:
 #               print "OFF"
                self.SetGpio('OFF')
                self._flashState = False
                self._loghandle.info('VirtualPort::SetFlash Frequency %s above MAX %s ;Pin %s OFF; Flash State %s',self._flashFrequency,self._flashMAX,self._HW_ID,self._flashState)
              #  self._hwHandle.WritePin(self._HW_ID, 1)
               # self._currentPinStatus = 1
            else:
                self._flashT1 = time.time()
                self._flashT2 = self._flashT1 + self._flashFrequency
                self._flashState = True
                self._loghandle.info('VirtualPort::SetFlash CurrentClock: %s , Freqency %s, Flash State %s',self._flashT1,self._flashFrequency, self._flashState)
        except ValueError:
         #   self._flashFrequency = int(2)
          #  self._t1 = time.clock()
            self._loghandle.info('VirtualPort::SetFlash value error %s not supported',value)
        
        return True           
           
    def UpdateFlash(self):         
        
        if self._flashState == True:
            self._flashT1 = time.time()
            if self._flashT1 > self._flashT2:
                self._flashT2 = self._flashT1 + self._flashFrequency
     #           self._loghandle.info('VirtualPort::UpdateFlash Clock t2: %s, Clock t1 %s', self._flashT2, self._flashT1)
                self._flashT2 
                if self._currentPinStatus == 0:
                    self._hwHandle.WritePin(self._HW_ID, 1) 
                    self._currentPinStatus = 1
                else:
                    self._hwHandle.WritePin(self._HW_ID, 0) 
                    self._currentPinStatus = 0
            
        return True
    
    def SetPushButton(self,value):
        
        if self._ON_VALUE in value:
            self._pushButtonT1 = time.time()
            self._pushButtonState = True
            self._hwHandle.WritePin(self._HW_ID, 1)
            self._loghandle.info('VirtualPort::SetPushButton Counter: %s start TimeT1: %s Puls Length: %s',self._pushButtonState, self._pushButtonT1, self._PULS_LENGTH)  
        else:
            self._loghandle.error('VirtualPort::Set Command %s not found for port',value)  
    
        return True
    
    def UpdatePushButton(self):         
        
        if self._pushButtonState == True:
   #         print "Pushbutton counter active"
            self._pushButtonT2 = self._PULS_LENGTH + self._pushButtonT1
           # self._pushButtonDelta = self._pushButtonT1 + self._PULS_LENGTHtime.time()
            
 #           print "T2:",self._pushButtonT2
  #          print "Current Time:",time.time()
            if time.time() > self._pushButtonT2:
                
                if self._pushButtonState == True:
                    self._hwHandle.WritePin(self._HW_ID, 0) 
                    self._pushButtonState = False
                    self._loghandle.info('VirtualPort::PushButton timed out Port %s', self._NAME)
            
        return True
    
    def SetPWM(self,value):
        try: 
            self._flashFrequency = float(value)
            self._hwHandle.WritePWM(self._HW_ID,value) 
            
        except ValueError:
         #   self._flashFrequency = int(2)
          #  self._t1 = time.clock()
            self._loghandle.info('VirtualPort::SetPWM value error %s not supported',value) 
        return True
    
    def UpdateDebounce(self):

        savedState = self._savedState
        resultDict = self.Get()
        pinState = resultDict.get('State',None)
        update = False

        '''
        was there a state change in the last period
        '''
        if pinState != savedState:
            '''
            was it a T0 event or T1
            '''
            if self._T0 == 0:
                ''' T0 event '''
                self._T0 = time.time()
                update = False
            else:
                ''' T1 event '''
                self._T1 = time.time()
                update = True
                '''Calculate time between events'''
                self._T2 = self._T1 - self._T0
                
                self._T0 = 0
                self._loghandle.info('VirtualPort::Update DEBOUNCE button pressed for: %s seconds',self._T2)
        else:
            update = False
             
        return {'Update':update,'State':self._T2}
        
    
    def GetDirection(self):
        return self._DIRECTION
    
    def GetName(self):
        return self._NAME
        
    def GetMode(self):
        return self._MODE