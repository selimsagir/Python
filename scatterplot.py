from turtle import pen
import PyQt6
import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtCore

win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting scatter")
win.resize(1000, 600)
win.setWindowTitle('Plotting')





p1 = win.addPlot(title="graph1")

x = np.random.normal(size=1000)
y = np.random.normal(size=1000)
p1.plot(x, y, pen=None, symbol='o')  ## setting pen=None disables line drawing

p2 = win.addPlot(title="graph2")


x1 = np.random.normal(size=10)
y1 = np.random.normal(size=10)

p2.plot(x1,y1,pen=None,symbol='o')

win.nextRow()

p3 = win.addPlot(title="graph3")
x = np.cos(np.linspace(0, 2*np.pi,1000))
y = np.sin(np.linspace(0, 4*np.pi,1000))
p3.plot(x,y)
p3.showGrid(x=True, y=True)


p4 = win.addPlot(Title="updating plot")
curve = p4.plot(pen='y')
data= np.random.normal(size=(10,1000))
ptr=0
def update():
    global curve, data,ptr, p4
    curve.setData(data[ptr%10])
    if ptr ==0:
        p4.enableAutoRange('xy', False)

    ptr += 1

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)




if __name__ == '__main__':
    pg.exec()
