import pyqtgraph as pg
import numpy as np

xPad = 0.05

class CarpetView(pg.ImageView):
    def __init__(self, parent=None):
        super().__init__(parent, view=pg.PlotItem())
        self.ui.menuBtn.hide()
        self.ui.roiBtn.hide()
        cm = pg.colormap.getFromMatplotlib('jet')
        self.setColorMap(cm)
        self.view.setMouseEnabled(x=False, y=True)
        self.view.setAutoVisible(y=False)
        self.view.setAspectLocked(lock=False)
        self.view.getAxis('left').setTickDensity(1.25)
        self.view.getAxis('left').setStyle(tickLength=5)
        self.view.getAxis('bottom').setStyle(tickLength=5)

        ax = self.getView().getAxis('left')
        ax.tickStrings = self.tickStrings

    def setXticks(self, left_off, right_off, sampling_rate, num=6, unit='ms'):
        
        if unit=='ms':
            majorTicks = np.linspace(0, left_off+right_off, num)
            minorTicks = np.linspace(0, left_off+right_off, 5*(num-1)+1)
            self.view.getAxis('bottom').setTicks([
            [(t.item(), str(int((t-left_off)*1000/sampling_rate))+' ms') for t in majorTicks],
            [(t.item(), '') for t in minorTicks]
            ])
        elif unit=='bpm':
            ticks = np.linspace(left_off, left_off+right_off, num+1)
            self.view.getAxis('bottom').setTicks([
            [(t.item(), str(int(60*sampling_rate/(t-left_off)))) if t>sampling_rate else (t.item(), 'bpm') for t in ticks ]
            ])
        
    def setFontSize(self, size):
        font = pg.QtGui.QFont('sans', size)
        self.view.getAxis('left').setTickFont(font)
        self.view.getAxis('bottom').setTickFont(font)
    
    def resetLimits(self):
        width, height = self.getImageItem().image.shape

        self.view.setLimits(
                xMin=-xPad*width, xMax=(1.+xPad)*width, 
                minXRange=(1.+2*xPad)*width, 
                maxXRange=(1.+2*xPad)*width, 
                yMin=-0.03*height, yMax=1.02*height, 
                minYRange=5, maxYRange=1.05*height,
        )
    
    def resetRange(self):
        width, height = self.getImageItem().image.shape

        self.view.setLimits(
                xMin=-xPad*width, xMax=(1.+xPad)*width, 
                minXRange=(1.+2*xPad)*width, 
                maxXRange=(1.+2*xPad)*width, 
                yMin=-0.03*height, yMax=1.02*height, 
                minYRange=5, maxYRange=1.05*height,
        )
        self.view.setRange(
            xRange=[-xPad*width, (1.+xPad)*width], 
            yRange=[-0.03*height, 1.02*height],
        )


    def RtoTime(self, R):
        return ""
   
    def tickStrings(self, values, scale, spacing):
        return [self.RtoTime(v) for v in values]