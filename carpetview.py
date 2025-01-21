import pyqtgraph as pg
import numpy as np

class CarpetView(pg.ImageView):
    def __init__(self, parent=None, view=None):
        super().__init__(parent, view=pg.PlotItem())
        self.ui.menuBtn.hide()
        self.ui.roiBtn.hide()
        cm = pg.colormap.getFromMatplotlib('jet')
        self.setColorMap(cm)
        self.view.setMouseEnabled(x=False, y=True)

        ax = self.getView().getAxis('left')
        ax.tickStrings = self.tickStrings

    def setXticks(self, left_off, right_off, sampling_rate, num=6):
        ticks = np.linspace(0, left_off+right_off, num)
        ax = self.getView().getAxis('bottom')
        ax.setTicks([
           [(t.item(), str(int((t-sampling_rate)*1000/sampling_rate))) for t in ticks]
           ])
        
    def RtoTime(self, R):
        return ""
   
    def tickStrings(self, values, scale, spacing):
        return [self.RtoTime(v) for v in values]