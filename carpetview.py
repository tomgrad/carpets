import pyqtgraph as pg
import numpy as np

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
            ticks = np.linspace(0, left_off+right_off, num)
            self.view.getAxis('bottom').setTicks([
            [(t.item(), str(int((t-sampling_rate)*1000/sampling_rate))+' ms') for t in ticks]
            ])
        elif unit=='bpm':
            ticks = np.linspace(left_off+sampling_rate//4, left_off+right_off, num)
            self.view.getAxis('bottom').setTicks([
            [(t.item(), str(int(60*sampling_rate/(t-sampling_rate)))+' bpm') for t in ticks if t>sampling_rate]
            ])
        
    def setFontSize(self, size):
        font = pg.QtGui.QFont('sans', size)
        self.view.getAxis('left').setTickFont(font)
        self.view.getAxis('bottom').setTickFont(font)
    
    def resetLimits(self):
        width, height = self.getImageItem().image.shape

        self.view.setLimits(
                xMin=-0.1*width, xMax=1.1*width, 
                minXRange=1.2*width, 
                maxXRange=1.2*width, 
                yMin=-0.03*height, yMax=1.02*height, 
                minYRange=5, maxYRange=1.05*height,
        )
    
    def resetRange(self):
        width, height = self.getImageItem().image.shape

        self.view.setLimits(
                xMin=-0.1*width, xMax=1.1*width, 
                minXRange=1.2*width, 
                maxXRange=1.2*width, 
                yMin=-0.03*height, yMax=1.02*height, 
                minYRange=5, maxYRange=1.05*height,
        )
        self.view.setRange(
            xRange=[-0.1*width, 1.1*width], 
            yRange=[-0.03*height, 1.02*height],
        )


    def RtoTime(self, R):
        return ""
   
    def tickStrings(self, values, scale, spacing):
        return [self.RtoTime(v) for v in values]