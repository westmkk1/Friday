import socket
import ServerInfo

#A connection to a device
class DeviceConnection:

    def __init__(self):
        #Get server information
        self.securityCode = ServerInfo.SECURITY_CODE
        self.serverIp = ServerInfo.SERVER_IP
        self.serverPort = ServerInfo.SERVER_PORT
        self.serverAddress = (self.serverIp, self.serverPort)
        self.packetSize = 4

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)#Create the socket

    #Opens the connection and waits for a device to connect to it
    #Returns true if device is connected, false if not able to connect
    def openConnection(self):
        self.socket.bind(self.serverAddress)
        self.socket.listen(0)

        #Accept a connection and get the connected socket and device address from it
        self.deviceConnection, self.deviceAddress = self.socket.accept()

        #The device should send a security code right away so be sure to check it
        print("Device: " + str(self.deviceAddress[0]) + " connected to Server")
        print("Authenticating device...")

        code = self.getData(ServerInfo.SECURITY_CODE_BYTES)#Recieve 8 bytes (Security codes are 8 bytes long)

        #Check the security code
        if code == self.securityCode:
            print("Device: " + str(self.deviceAddress[0]) + " has been authenticated")
            print("Retreiving device information...")

            #After the device has authenticated itself it should send information about itself
            
            #First it will send its device type
            self.deviceType = self.getData()
            #Then it sends device name
            self.deviceName = self.getData(ServerInfo.DEVICE_NAME_LENGTH_MAX)

            #Tell the object how many bytes it should be expecting when recieving data from the device
            self.packetSize = ServerInfo.Device_Packet_Sizes[self.deviceType]
            return True;
        else:
            
            print("Device: " + str(self.deviceAddress[0]) + " is not authorized to connect to Server")
            print("Closing connection...")
            self.closeConnection()
            return False;

    #Terminates the connection
    def closeConnection(self):
        self.deviceConnection.shutdown(socket.SHUT_RDWR)
        self.deviceConnection.close()
        #Create new socket, cant use old one anymore
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.socket.bind(self.serverAddress)#Bind the socket to server address
        

    #Receives data
    def getData(self, packetSize):
        if not packetSize:
            packetSize = self.packetSize

        return self.deviceConnection.recv(packetSize);

    #Sends data
    def sendData(self, data):
        self.deviceConnection.send(data)

    #Gets the type of device
    def getDeviceType(self):
        return self.deviceType;

    #Gets the name of the device
    def getDeviceName(self):
        return self.deviceName;


    #Reconnect to the device with a new socket
    def reconnectToDevice(self):
        self.sendData("sckRstWait")
        self.closeConnection()#Make sure the socket is closed before making a new one
        
        self.connection = self.socket.connect(self.deviceAddress)#The device should be waiting for a connection so re-connect to it

        #Check for security code to make sure we reconnected
        code = self.getData(ServerInfo.SECURITY_CODE_BYTES)

        if code == ServerInfo.SECURITY_CODE:
            return True;
        else:
            return False:
        
        
