import DeviceConnection

class BinaryDevice:

    def __init__(self, deviceConnection):
        self.deviceName = deviceConnection.getDeviceName()
        self.deviceType = deviceConnection.getDeviceType()

        self.connection = deviceConnection

    #Renew the connection to the device so we dont use the same socket all day
    def renewConnection(self):
        self.connection.reconnectToDevice(self)

    #Send an off signal to the device
    def switchOff(self):
        self.connection.sendData("DOff")

    def switchOn(self):
        self.connection.sendData("DeOn")
        

    
