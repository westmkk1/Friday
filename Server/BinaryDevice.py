import DeviceConnection
import time
import ServerInfo

class BinaryDevice:
	
	#Provide a connection to the device
    def __init__(self, deviceConnection):
        self.deviceName = deviceConnection.getDeviceName()
        self.deviceType = deviceConnection.getDeviceType()
        self.connection = deviceConnection
		
		self.lastActiveTime = time.time()

    #Renew the connection to the device so we dont use the same socket all day
    def renewConnection(self):
        self.connection.reconnectToDevice(self)
		
		#Say the last time the connection was active
		self.lastActiveTime = time.time()

		
    #Send an off signal to the device
    def switchOff(self):
		#Check if the connection need to be renewed
		if (time.time() - self.lastActiveTime) >= ServerInfo.SOCKET_RENEW_TIME:
			self.renewConnection()
			
        self.connection.sendData("DOff")

	
	#Send an On signal to the device
    def switchOn(self):
		#Check if the connection need to be renewed
		if (time.time() - self.lastActiveTime) >= ServerInfo.SOCKET_RENEW_TIME:
			self.renewConnection()
			
        self.connection.sendData("DeOn")
		
	
	def getDeviceName(self):
		return self.connection.getDeviceName();
	
	#Terminate the connection between the server and the device
	def disconnectDevice(self):
		self.connection.closeConnection()
		self.connection = None
		
        
	
    
