import serial
import time
import struct
import pyqtgraph as pg
import pyqtgraph.parametertree as ptree
from pyqtgraph.Qt import QtWidgets, QtCore

import numpy as np
from scipy.fftpack import fft

Nf=4
T =0.001081 # sample period
plotLength = 16384
fftLength = 1024

app = pg.mkQApp("KTU dsplab UART Live Data")

children = [
    dict(name='Connect', type='action'),
    dict(name='sigcons', title='Connection', type='group', children=[
        dict(name='Port', type='str', value="/dev/pts/2"),
		dict(name='BaudRate', type='int', value=115200),
		dict(name='Data Bits', type='list', limits=[5, 6, 7, 8], value=8),
		dict(name='Stop Bits', type='list', limits=[1, 1.5, 2], value=1),
		dict(name='Parity', type='list', limits={'None':'N', 'Even':'E', 'Odd':'O', 'Mark':'M', 'Space':'S'}, value='N'),
    ]),
    dict(name='parseropts', title='Parser Options', type='group', children=[
        dict(name='StartByte', type='str', value="AA BB"),
        dict(name='EndByte', type='str', value=""),
        dict(name='Channels', type='int', value=3),
		dict(name='DataType', type='list', limits={'INT8':0, 'UINT8':1, 
                                                   'INT16':2, 'UINT16':3, 
                                                   'INT32':4, 'UINT32':5, 
                                                   'INT64':6, 'UINT64':8, 
                                                   'FLOAT':8, 'DOUBLE':9}, value=4),
        dict(name='Endianness', type='list', limits={'LITTLE':0, 'BIG':1}, value=0),
        dict(name='Expected:', type='str', value='', readonly=True),
    ]),
    dict(name='plotteropts', title='Plotter Options', type='group', children=[
        dict(name='Autoscale', type='bool', value=True, enabled=False),
        dict(name='Plot Length', type='int', limits=[0, None], step = 1000, value=plotLength),
        dict(name='Offset', type='float', value=0.0, precision=2, enabled=False),
        dict(name='Multiplier', type='float', value=1.0, precision=2, enabled=False),
    ]),
    dict(name='FFTopts', title='FFT Options', type='group', children=[
        dict(name='Autoscale', type='bool', value=True, enabled=False),
        dict(name='Show DC', type='bool', value=True),
        dict(name='NSamples', type='int', limits=[0, None], value=fftLength),
    ]),
    dict(name='stats', title='Stats', type='group', children=[
        dict(name='Sample/s', type='float', value=0.0, precision=1, readonly=True, units='sps'),
        dict(name='Queue', type='int', value=0, readonly=True, units='packets'),
    ]),
]

params = ptree.Parameter.create(name='Parameters', type='group', children=children)
pt = ptree.ParameterTree(showHeader=False)
pt.setParameters(params)

glw = pg.GraphicsLayoutWidget(show=True, title="KTU dsplab UART Live Data")
#glw.resize(800,800)

pt1 = glw.addPlot(title="time domain")
pt1.setLabel('left', 'amplitude', units='v')
pt1.setLabel('bottom', 'time', units='s')
# lr = pg.LinearRegionItem([(plotLength - fftLength) * T,plotLength * T])
# pt1.addItem(lr)

curvet0 = pt1.plot(pen='r', name="CH0")
curvet1 = pt1.plot(pen='g', name="CH1")
curvet2 = pt1.plot(pen='b', name="CH2")

glw.nextRow()

pf1 = glw.addPlot(title="freq domain")
pf1.setLabel('left', 'amplitude', units='v')
pf1.setLabel('bottom', 'freq', units='Hz')

curvef0 = pf1.plot(pen='r', name="CH0")
curvef1 = pf1.plot(pen='g', name="CH1")
curvef2 = pf1.plot(pen='b', name="CH2")

splitter = QtWidgets.QSplitter()
splitter.addWidget(pt)
splitter.addWidget(glw)
splitter.show()


##########
##########
def paramValueChanged():
    global sp
    global fautoscale, fdc, fNSamples
    global tautoscale, tplotlength, toffset, tmultiplier
    global startBytes, endBytes, numChannel, dataType, endianness
    global Xf, Xt, Yt0, Yt1, Yt2, Yf0, Yf1, Yf2

    fftopts = params.child('FFTopts')
    fautoscale = fftopts['Autoscale']
    fdc = fftopts['Show DC']
    fNSamples = fftopts['NSamples']
    
    plotteropts = params.child('plotteropts')
    tautoscale = plotteropts['Autoscale']
    tplotlength = plotteropts['Plot Length']
    toffset = plotteropts['Offset']
    tmultiplier = plotteropts['Multiplier']
     
    parseropts = params.child('parseropts')
    startByteStr = parseropts['StartByte']
    startBytes = list(bytearray.fromhex(startByteStr))
    endByteStr = parseropts['EndByte']
    endBytes = list(bytearray.fromhex(endByteStr))
    numChannel = parseropts['Channels']
    dataType = parseropts['DataType']
    endianness = parseropts['Endianness']
    
    # set new parser config
    if sp != None:
        sp.setDataType(aStartSequence = startBytes, 
                       aEndSequence = endBytes, 
                       aDataType = dataType, 
                       aNumChannel = numChannel, 
                       aEndianness = endianness)
    
        expectedStr = sp.getExpected()
        parseropts.child('Expected:').setValue(expectedStr)
    
    # calculate X values for the plotter
    Xf = np.linspace(0.0, 1.0/(400.0*T),   tplotlength)
    Xt = np.linspace(0.0, tplotlength*T, tplotlength)
    Yt0 = np.linspace(0.0, fNSamples*T, fNSamples)
    Yt1 = np.linspace(0.0, fNSamples*T, fNSamples)
    Yt2 = np.linspace(0.0, fNSamples*T, fNSamples)
    Yf0 = np.linspace(0.0, fNSamples*T, fNSamples)
    Yf1 = np.linspace(0.0, fNSamples*T, fNSamples)
    Yf2 = np.linspace(0.0, fNSamples*T, fNSamples)

ser = None
def disconnect():
    global ser
    ser.close()
    
    if ser.is_open == False:
        # Remove old signal then connect new signal
        params.child('Disconnect').sigActivated.disconnect(disconnect)
        params.child('Disconnect').setName("Connect")
        params.child('Connect').sigActivated.connect(connect)
        params.child('sigcons').show()
        
        params.child('Connect').child('Connected').remove()
    else:
        print("Cannot disconnect")
      

def connect():
    global ser
    sigcons = params.child('sigcons')
    portname = sigcons['Port']
    baudrate = sigcons['BaudRate']
    stopbits = sigcons['Stop Bits']
    bytesize = sigcons['Data Bits']
    parity = sigcons['Parity']
    
    ser = serial.Serial(port=portname, 
                        baudrate=baudrate, 
                        bytesize=bytesize, 
                        stopbits=stopbits, 
                        parity=parity)

    if ser.is_open:
        # Remove old signal then connect new signal
        params.child('Connect').sigActivated.disconnect(connect)
        params.child('Connect').setName("Disconnect")
        params.child('Disconnect').sigActivated.connect(disconnect)
        params.child('sigcons').hide()
        
        connectedstr = "{} :{}".format(portname, baudrate)
        params.child('Disconnect').addChild({'name': 'Connected', 'type': 'str', 'value': connectedstr, 'readonly': True})
        
        print(ser)
    else:
        print("Cannot connect to: ", portname)
        

##########
# file: serialparser.py
# author: sefa unal
##########

class Endianness:
    LITTLE  = 0
    BIG     = 1
    
    def getParserChar(self, aEndianness):
        lParserChar = ['<', '>']
        return lParserChar[aEndianness]
    
class DataType:
    INT8    = 0
    UINT8   = 1
    INT16   = 2
    UINT16  = 3
    INT32   = 4
    UINT32  = 5
    INT64   = 6
    UINT64  = 7
    FLOAT32 = 8
    DOUBLE  = 9
    
    def getSize(self, aDataType):
        lDataSize = [1, 1, 2, 2, 4, 4, 8, 8, 4, 8]
        return lDataSize[aDataType]
    
    def getParserChar(self, aDataType):
        lParserChar = ['b', 'B', 'h', 'H', 'l', 'L', 'q', 'Q', 'f', 'd']
        return lParserChar[aDataType]

class SerialParser:
    def __init__(self, aStartSequence, 
                 aDataType:DataType, 
                 aNumChannel, 
                 aEndianness:Endianness = Endianness.LITTLE,
                 aEndSequence = [],
                 aEnableDebug = 0):
        
        self.buffer             = bytearray()
        self.debug              = aEnableDebug
        self.setDataType(aStartSequence, aDataType, aNumChannel, aEndianness, aEndSequence)
        self.packetpersec       = 0
        self.totalPacket        = 0
        self.startTime          = 0
        # self.totalPacketold     = 0

    def setDataType(self, aStartSequence, 
                    aDataType:DataType, 
                    aNumChannel, 
                    aEndianness:Endianness = Endianness.LITTLE, 
                    aEndSequence = []):
        
        self.dataType           = aDataType
        self.numChannels        = aNumChannel
        self.startSequence      = aStartSequence
        self.endSequence        = aEndSequence
        self.endianness         = aEndianness
        
        sizex = DataType().getSize(self.dataType)
        self.payloadSize        = self.numChannels * sizex
        self.headerSize         = len(self.startSequence)
        self.packetSize         = self.headerSize + self.payloadSize + len(self.endSequence)
        
        self.parserString       = Endianness().getParserChar(self.endianness)
        for i in range(self.numChannels):
            self.parserString += DataType().getParserChar(self.dataType)
        
    def getPacketPerSecond(self):
        return self.packetpersec
    
    def getExpected(self):
        explst = []
        explst.extend(self.startSequence)
        for i in range(self.numChannels * DataType().getSize(self.dataType)):
            explst.append('XX')
        explst.extend(self.endSequence)
        return str(explst)
        
    def parse(self, data):
        parsedPackets = []
        self.buffer.extend(data)
        
        while len(self.buffer) >= self.packetSize:
            lNotFound = 0
            # search for start sequence
            for i, val in enumerate(self.startSequence):
                if self.buffer[i] != val :
                    lNotFound = 1
                    break
            
            if lNotFound:
                # remove a byte and search again
                self.buffer.pop(0)
                continue
            
            # search for end sequence
            for i, val in enumerate(self.endSequence):
                if self.buffer[i + self.headerSize + self.payloadSize] != val :
                    lNotFound = 1
                    break
                
            if lNotFound:
                # remove a byte and search again
                self.buffer.pop(0)
                continue
            
            # found a valid packet
            byte_range = self.buffer[self.headerSize:self.headerSize + self.payloadSize]
            parsedValues = struct.unpack(self.parserString, byte_range)
            parsedPackets.append(parsedValues)
            

            # remove parsed packet from buffer
            self.buffer = self.buffer[self.packetSize:]

        self.totalPacket += len(parsedPackets)
        curTime = time.perf_counter()
        if self.startTime == 0:
            self.startTime = curTime
        else:
            timeDelta = curTime - self.startTime
            if timeDelta > 1: # calculate packetpersecond value every second
                self.packetpersec = self.packetpersec * 0.2 + (self.totalPacket / timeDelta) * 0.8
                self.totalPacket = 0;
                self.startTime = curTime
                
        return parsedPackets
    
ch0 = []
ch1 = []
ch2 = []
def update():
    global ser, sp
    global fautoscale, fdc, fNSamples
    global tautoscale, tplotlength, toffset, tmultiplier
    global Xf, Xt, Yt0, Yt1, Yt2, Yf0, Yf1, Yf2
    global queue
    
    if ser == None:
        return
    
    if not ser.is_open:
        return

    inw = ser.in_waiting
    
    lDataBuffer = sp.parse(ser.read(inw))

    queue = len(lDataBuffer)
    if queue == 0:
        return
    
    # Transpose of lDataBuffer
    lDataBuffer = list(map(list, zip(*lDataBuffer)))

    ch0.extend(lDataBuffer[0])
    ch1.extend(lDataBuffer[1])
    ch2.extend(lDataBuffer[2])

    # ch0.append(data[0]*0.928/0x7fffff00)
    # ch1.append(data[1]*0.928/0x7fffff00)
    # ch2.append(data[2]*0.928/0x7fffff00)

    lFFTDC = 1
    if fdc == True:
        lFFTDC = 0
        
    # draw time domain plot
    tstart = -min(tplotlength + 1, len(ch0))
    tend = -1
    curvet0.setData(Xt[0:-tstart-1],ch0[tstart:tend])
    curvet1.setData(Xt[0:-tstart-1],ch1[tstart:tend])
    curvet2.setData(Xt[0:-tstart-1],ch2[tstart:tend]) 
    
    # draw frequency domain plot
    if(len(ch0) > fNSamples):
        tstart = -min(fNSamples + 1, len(ch0))
        
        fstart = lFFTDC
        fend = (fNSamples // 2) - 1
        
        Yf0=fft(ch0[tstart:tend])
        curvef0.setData(Xf[fstart:fend],abs(Yf0[fstart:fend]))
        Yf1=fft(ch1[tstart:tend])
        curvef1.setData(Xf[fstart:fend],abs(Yf1[fstart:fend]))
        Yf2=fft(ch2[tstart:tend])
        curvef2.setData(Xf[fstart:fend],abs(Yf2[fstart:fend]))

    app.processEvents()
       
def updateui():
    global sp
    global queue
    
    if sp == None:
        return
    params.child('stats').child('Queue').setValue(queue)
    params.child('stats').child('Sample/s').setValue(sp.getPacketPerSecond())

params.child('sigcons').sigTreeStateChanged.connect(paramValueChanged)
params.child('parseropts').sigTreeStateChanged.connect(paramValueChanged)
params.child('plotteropts').sigTreeStateChanged.connect(paramValueChanged)
params.child('FFTopts').sigTreeStateChanged.connect(paramValueChanged)
# params.sigTreeStateChanged.connect(paramValueChanged)
params.child('Connect').sigActivated.connect(connect)

def setupParser():
    global sp, startBytes, endBytes, numChannel, dataType, endianness
    sp = SerialParser(aStartSequence = startBytes, 
                      aEndSequence = endBytes, 
                      aDataType = dataType, 
                      aNumChannel = numChannel, 
                      aEndianness = endianness)
sp = None
queue = 0
paramValueChanged()
setupParser()
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(20)
timer1 = QtCore.QTimer()
timer1.timeout.connect(updateui)
timer1.start(500)

if __name__ == '__main__':
    pg.exec()