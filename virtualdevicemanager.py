
import threading
import Queue
import time


from virtualportmanager import vpm
from hwIF_23017 import hwIF_23017
from hwIF_stub import hwIF_stub
from hwIF_raspberry import hwIF_raspberry
from config import config
from wrapper_log import loghandle



class vdm(threading.Thread):
    '''irtualDeviceDrv23017
    classdocs
    '''

    def __init__(self, configuration, threadQueue):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        
        self._loghandle = loghandle()

        self._config = config(configuration)
        
        self._help = configuration
        
        self._DEVICE = configuration.get('DEVICE')
        self._MQTT_CHANNEL = configuration.get('MQTT_CHANNEL')
#        self._RASPBERRY_REV = int(configuration.get('RASPBERRY_REV'))
 #       self._I2C_ADDRESS = int(configuration.get('I2C_ADDRESS'),16)
        
        self._threadQueue = threadQueue
        self._setQueue = Queue.Queue()
        
        self._portInstanceList = []
#        self._loghandle.info('VirtualDeviceDrv23017::init  Version %s , Date %s',__VERSION__,__DATE__)
        self._loghandle.info('VirtualDeviceDrv23017::init Create Object Device %s Mqtt %s',self._DEVICE,self._MQTT_CHANNEL)
        self._loghandle.debug('VirtualDeviceDrv23017::init Create Object with configuration %s',configuration)
        
    def __del__(self):
        '''
        delets the mqtt wrapper object
        '''
        self._loghandle.debug('VirtualDeviceDrv23017::del Delete Object')
        
    def run(self):
        self._loghandle.info('VirtualDeviceDrv23017::run Startup Thread')
        
        self.Setup()
   #     self.SetupPort()
        
        #read the port status of all boards 
        data = self.Update('ALL')
        self._threadQueue.put(data)
        
        rc = 0
        while rc == 0:
  #          print "Simulator Loop"
            '''Read Updaet from GPIO Ports'''
            data = self.Update('UPDATE')
            ''' make update from Flash Ports'''
            self.UpdateFlash()
            self.UpdatePushButton()
            self._threadQueue.put(data)
            while self._setQueue.qsize():
            #    print self._setQueue.qsize()
                print self._setQueue.get()
            time.sleep(0.1)

        self._loghandle.critical('VirtualDeviceDrv23017::run Thread Crashed')
        return rc
        
    def Setup(self):
        if 'MCP23017' in self._DEVICE:
            self._RASPBERRY_REV = int(self._help.get('RASPBERRY_REV'))
            self._I2C_ADDRESS = int(self._help.get('I2C_ADDRESS'),16)
            self._loghandle.info('Start MCP23017 Hardware Interface with i2c address: %s',self._I2C_ADDRESS)
            self._hwHandle = hwIF_23017(self._RASPBERRY_REV,self._I2C_ADDRESS)
           
            for configItem in self._config.getSectionByRegex('Port[0-9]'): 
                self._loghandle.debug('VirtualPortManager:Setup Port Number %s for Device %s with Configuration',len(self._portInstanceList), self._DEVICE, configItem) 
                self._portInstanceList.append(vpm(self._hwHandle, self._DEVICE, configItem))
                
        elif 'RASPBERRY' in self._DEVICE:
            self._loghandle.info('Start Raspberry GPIO interface')
            self._hwHandle = hwIF_raspberry()
            
            for configItem in self._config.getSectionByRegex('Port[0-9]'): 
                self._loghandle.debug('VirtualPortManager:Setup Port Number %s for Device %s with Configuration',len(self._portInstanceList), self._DEVICE, configItem) 
                self._portInstanceList.append(vpm(self._hwHandle, self._DEVICE, configItem))
            
        elif 'SIMULATOR' in self._DEVICE:
            self._I2C_ADDRESS = 0
            self._loghandle.info('Start Simulator Hardware Interface with virtual i2c address: %s',self._I2C_ADDRESS)
            self._hwHandle = hwIF_stub(self._I2C_ADDRESS)
           
            for configItem in self._config.getSectionByRegex('Port[0-9]'): 
                self._loghandle.debug('VirtualPortManager:Setup Port Number %s for Device %s with Configuration',len(self._portInstanceList), self._DEVICE, configItem) 
                self._portInstanceList.append(vpm(self._hwHandle, self._DEVICE, configItem))
            
        else:
            self._loghandle.crittical('VDM::Setup: Device not Supported')
        
 #   def SetupPort(self):

  #      for configItem in self._config.getSectionByRegex('Port[0-9]'): 
   #         self._loghandle.debug('VirtualDeviceDrv23017::SetupPort Port %s', configItem) 
   #         self._portInstanceList.append(virtualPort(self._hwDevice, configItem))
        
    def SetPort(self,msg):
        self._setQueue.put(msg)
        return True
                       
    def Set(self, portName, value):
  #      self._loghandle.error('VirtualDeviceDrv23017::Set Debug Port %s %s', portName, value)
        print "PORTNAME", portName, value
        result, portInstance = self.GetPortInstance(portName)
            
        if result == True:
            if 'OUT' in portInstance.GetDirection(): 
                self._loghandle.info('VirtualDeviceDrv23017new::Set Port %s found in Portlist', portName)
                portInstance.Set(value)
            else:
                self._loghandle.error('VirtualDeviceDrv23017new::Set Port %s is not OUTPUT Port', portName)
                result = False
        else:
            self._loghandle.error('VirtualDeviceDrv23017nes::Set Port %s NOT found in Portlist', portName)
            result = False
            
        return result
    
    def Get(self, portName):
        
        result, portInstance = self.GetPortInstance(portName)

        if result == True:
            resultDict = portInstance.Get()

        return (resultDict) 
    
    def Update(self, mode):
        resultList = []
        
        for portInstance in self._portInstanceList:
            if 'UPDATE' in mode:
                if 'IN' in portInstance.GetDirection():
                    resultDict = portInstance.Update()
                    if resultDict.get('Update') == True:   
                        resultDict.update({'DeviceChannel':self._MQTT_CHANNEL})
                        resultDict.update({'PortName':portInstance.GetName()})
                        resultDict.update({'PortState':resultDict.get('State',None)})
                        resultList.append(resultDict)
                        
            elif 'ALL' in mode:

                resultDic = portInstance.Get()
            
                resultDic.update({'DeviceChannel':self._MQTT_CHANNEL})
                resultDic.update({'PortName':portInstance.GetName()})
                resultDic.update({'PortState':resultDic.get('State',None)})

                resultList.append(resultDic)
            
            else:
                self._loghandle.error('VirtualDeviceDrv23017::Update unknown Mode: %s', mode)  
                
        if len(resultList) > 1:
            self._loghandle.info('VirtualDeviceDrv23017::Update Result List %s', resultList)  
            
        return resultList
    
    def UpdateFlash(self):
        
        for portInstance in self._portInstanceList:
            if 'FLASH' in portInstance.GetMode():
                portInstance.UpdateFlash()   
                
    def UpdatePushButton(self):
        
        for portInstance in self._portInstanceList:
            if 'PUSH_BUTTON' in portInstance.GetMode():
                portInstance.UpdatePushButton()   
                
    def UpdateDebounce(self):    
        resultList = [] 
        
        for portInstance in self._portInstanceList:
            if 'DEBOUNCE' in portInstance.GetMode():
                resultDict = portInstance.UpdateDebounce()
                if resultDict.get('Update') == True: 
                    resultDic.update({'DeviceChannel':self._MQTT_CHANNEL})
                    resultDic.update({'PortName':portInstance.GetName()})
                    resultDic.update({'PortState':resultDic.get('State',None)})
                    
                    resultList.append(resultDic)
                    
        if len(resultList) > 1:
            self._loghandle.info('VirtualDeviceDrv23017::Update Result List %s', resultList)
                    
        return resultList
          
     
    def GetPortInstance(self, portName):    

        result = False
        portInstance = None
        
        portName = portName.strip()
        
        for instance in self._portInstanceList:
            print "Search instance Search: ", portName," instance name", instance.GetName()
            if portName == instance.GetName():
    #            self._loghandle.info('DRIVER_Simulator::TEst Portname %s, GetName() %2', portName, instance.GetName())
                portInstance = instance
                result = True
                print "Port FOUND"
                break
                
        self._loghandle.debug('VirtualDeviceDrv23017::GetPortInstance Result: %s Port Instance %s', result, portInstance)       
        return (result, portInstance)    

    
    def GetChannelName(self):
        return self._MQTT_CHANNEL
        

    
             