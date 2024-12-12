# Carpets GUI

Requirements:
- pyside6
- pyqtgraph

Tips:
- run Qt Designer with `pyside6-designer`
- `ui_mainwindow.py` file can by generated from the console with `pyside6-uic mainwindow.ui -o ui_mainwindow.py` or directly from Qt Designer (Menu: Form -> View Python Code... -> Save)



For the serious application developer, all of the functionality in pyqtgraph is available via widgets that can be embedded just like any other Qt widgets. Most importantly, see: PlotWidget, ImageView, GraphicsLayoutWidget, and GraphicsView. PyQtGraph’s widgets can be included in Designer’s ui files via the “Promote To…” functionality:

In Designer, create a QGraphicsView widget (“Graphics View” under the “Display Widgets” category).

Right-click on the QGraphicsView and select “Promote To…”.

Under “Promoted class name”, enter the class name you wish to use (“PlotWidget”, “GraphicsLayoutWidget”, etc).

Under “Header file”, enter “pyqtgraph”.

Click “Add”, then click “Promote”.