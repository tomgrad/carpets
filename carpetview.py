import pyqtgraph as pg

class CarpetView(pg.ImageView):
    def __init__(self, parent=None, view=None):
        super().__init__(parent, view=pg.PlotItem())
        self.ui.menuBtn.hide()
        self.ui.roiBtn.hide()
        cm = pg.colormap.getFromMatplotlib('jet')
        self.setColorMap(cm)
        self.view.setMouseEnabled(x=False, y=True)
        self.view.setAspectLocked(True)


    