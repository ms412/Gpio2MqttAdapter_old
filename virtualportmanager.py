
import time

from wrapper_log import loghandle

class BinaryOut(object):
    '''
    classdocs
    '''
    def __init__(self, hwHandle, hwDevice, configuration):
        '''
        Constructor
        '''    

        self._hwHandle = hwHandle
        self._hwDevice = hwDevice
        self._config = configuration
        self._loghandle = loghandle()
        
        self.Setup()
        
    def Setup(self):
        
        self._SavePinState = ''
        
 
        if any(temp in self._hwDevice for temp in ['MCP23017','RASPBERRY']):
            ''' 
            Mandatory configuration Items
            '''
            try:
                self._NAME = self._config.get('NAME')
                self._HWID = int(self._config.get('HWID'))

            except:
                self._loghandle.critical('VPM::Init Mandatory Parameter missing for Port %s',self._NAME)
                
            ''' 
            optional configuration Items
            '''
            self._MODE = self._config.get('MODE','BINARY-OUT')
            self._DIRECTION = self._config.get('DIRECTION','OUT')
            self._OFF_VALUE = self._config.get('OFF_VALUE','OFF')
            self._ON_VALUE = self._config.get('ON_VALUE','ON')
            self._INITIAL = self._config.get('INITIAL',None)
            
            ''' 
            set initial configuration
            '''
            if self._INITIAL != None:
                self.Set(self._INITIAL)
            
            '''
            configure port as Output
            '''
            self._hwHandle.ConfigIO(self._HWID,0)
                
            self._loghandle.info('VPM::Init Configure Port %s HardwareID %s in Mode %s',self._NAME,self._HWID,self._MODE)

        else:
            self._loghandle.crittical('VDM::Setup: Device not Supported')
            
        return True
            
    def Set(self,value):
        
        if self._ON_VALUE in value:
            self._hwHandle.WritePin(self._HWID, 1)
            self._SavePinState  = 1
            self._loghandle.info('BinaryOut::Set %s port %s set to %s',self._NAME,self._HWID, value)  
            
        elif self._OFF_VALUE in value:
            self._hwHandle.WritePin(self._HWID, 0) 
            self._SavePinState  = 0
            self._loghandle.info('BinaryOut::Set %s port %s set to %s',self._NAME,self._HWID, value) 
             
        else:
            self._loghandle.error('BinaryOut::Set %s port %s command NOT %s found',self._NAME,self._HWID, value)  
    
        return True
 
            
    def Get(self):
        
        value = None
        
        if self._hwHandle.ReadPin(self._HWID) == 0:
            self._SavePinState  = 0
            value = self._OFF_VALUE

        else:
            self._SavePinState  = 1
            value = self._ON_VALUE

        self._loghandle.info('BinaryOut::Get %s port %s Status %s',self._NAME, self._HWID, value) 
        
        return value 
            
    def Update(self):
        
        update = False
        
        pinState = self._hwHandle.ReadPin(self._HWID)
        
        if  pinState != self._SavePinState:
            
            update = True
            
            if self._hwHandle.ReadPin(self._HWID) == 0:
                self._SavePinState  = 0
                value = self._OFF_VALUE
 
            else:
                self._SavePinState  = 1
                value = self._ON_VALUE
            
            self._loghandle.info('BinaryOut::Update %s port %s Port changed to %s',self._NAME, self._HWID, value)
             
        return {'Update':update,'State':value}
    
    def GetDirection(self):
        return self._DIRECTION
    
    def GetName(self):
        return self._NAME
        
    def GetMode(self):
        return self._MODE
    
class BinaryIn(object):
    '''
    classdocs
    '''
    def __init__(self, hwHandle, hwDevice, configuration):
        '''
        Constructor
        '''    

        self._hwHandle = hwHandle
        self._hwDevice = hwDevice
        self._config = configuration
        self._loghandle = loghandle()
        
        self.Setup()
        
    def Setup(self):
        
        self._SavePinState = ''
        
 
        if any(temp in self._hwDevice for temp in ['MCP23017','RASPBERRY']):
            ''' 
            Mandatory configuration Items
            '''
            try:
                self._NAME = self._config.get('NAME')
                self._HWID = int(self._config.get('HWID'))

            except:
                self._loghandle.critical('BinaryOut::Init Mandatory Parameter missing for Port %s',self._NAME)
                
            ''' 
            optional configuration Items
            '''
            self._MODE = self._config.get('MODE','BINARY-IN')
            self._DIRECTION = self._config.get('DIRECTION','IN')
            self._OFF_VALUE = self._config.get('OFF_VALUE','OFF')
            self._ON_VALUE = self._config.get('ON_VALUE','ON')
                
            '''
            configure port as Input
            '''
            self._hwHandle.ConfigIO(self._HWID,1)
                
            self._loghandle.info('BinaryOut::Init Configure Port %s HardwareID %s in Mode %s',self._NAME,self._HWID,self._MODE)

        else:
            self._loghandle.crittical('BinaryOut::Setup: Device not Supported')
            
        return True
 
            
    def Get(self):
        
        value = None
        
        if self._hwHandle.ReadPin(self._HWID) == 0:
            self._SavePinState  = 0
            value = self._OFF_VALUE

        else:
            self._SavePinState  = 1
            value = self._ON_VALUE

            
        self._loghandle.info('BinaryOut::Get %s port %s Status %s',self._NAME, self._HWID, value) 
        return value 
            
    def Update(self):
        
        update = False
        value = ''
        
        pinState = self._hwHandle.ReadPin(self._HWID)
        
        if  pinState != self._SavePinState:
            print "pin", pinState, self._SavePinState
            update = True
            
            if self._hwHandle.ReadPin(self._HWID) == 0:
                self._SavePinState  = pinState
                value = self._OFF_VALUE
 
            else:
                self._SavePinState  = pinState
                value = self._ON_VALUE
            
            self._loghandle.info('BinaryIN::Update %s port %s Port changed to %s',self._NAME, self._HWID, value)
             
        return {'Update':update,'State':value}
    
    def GetDirection(self):
        return self._DIRECTION
    
    def GetName(self):
        return self._NAME
        
    def GetMode(self):
        return self._MODE
        
class TimerOut(object):
    '''
    classdocs
    '''
    def __init__(self, hwHandle, hwDevice, configuration):
        '''
        Constructor
        '''    

        self._hwHandle = hwHandle
        self._hwDevice = hwDevice
        self._config = configuration
        self._loghandle = loghandle()
        
        self.Setup()
        
    def Setup(self):
        
        self._SavePinState = ''
        
 
        if any(temp in self._hwDevice for temp in ['MCP23017','RASPBERRY']):
            ''' 
            Mandatory configuration Items
            '''
            try:
                self._NAME = self._config.get('NAME')
                self._HWID = int(self._config.get('HWID'))

            except:
                self._loghandle.critical('BinaryOut::Init Mandatory Parameter missing for Port %s',self._NAME)
                
            ''' 
            optional configuration Items
            '''
            self._MODE = self._config.get('MODE','TIMER-OUT')
            self._DIRECTION = self._config.get('DIRECTION','OUT')
            self._ON_VALUE = self._config.get('ON_VALUE','ON')
            self._PULS_LENGTH = float(self._config.get('PULS_LENGTH',2))
            
            self._T0 = time.time()
            self._TimerOutState = False
                
            '''
            configure port as Input
            '''
            self._hwHandle.ConfigIO(self._HWID,0)
                
            self._loghandle.info('BinaryOut::Init Configure Port %s HardwareID %s in Mode %s',self._NAME,self._HWID,self._MODE)

        else:
            self._loghandle.crittical('BinaryOut::Setup: Device not Supported')
            
        return True
    
    def Set(self, value):
        if self._ON_VALUE in value:
            self._T0 = time.time()
            self._TimerOutState = True
            self._hwHandle.WritePin(self._HWID, 1)
            self._loghandle.info('VirtualPort::SetPushButton Counter: %s, start T0: %s, Puls Length: %s',self._TimerOutState, self._T0, self._PULS_LENGTH)  
        else:
            self._loghandle.error('VirtualPort::Set Command %s not found for port',value)  
    
        return True
    
    def Get(self):
        
        value = None
        
        if self._hwHandle.ReadPin(self._HWID) == 0:
            self._SavePinState  = 0
            value = self._OFF_VALUE

        else:
            self._SavePinState  = 1
            value = self._ON_VALUE

        self._loghandle.info('BinaryOut::Get %s port %s Status %s',self._NAME, self._HWID, value) 
        
        return value 

    def Update(self):         
        
        if self._TimerOutState == True:

            self._T1 = self._PULS_LENGTH + self._T0

            if time.time() > self._T1:
                
                if self._TimerOutState == True:
                    self._hwHandle.WritePin(self._HWID, 0) 
                    self._TimerOutState = False
                    self._loghandle.info('VirtualPort::PushButton timed out Port %s', self._NAME)
            
        return True            
    
    def GetDirection(self):
        return self._DIRECTION
    
    def GetName(self):
        return self._NAME
        
    def GetMode(self):
        return self._MODE
    
  