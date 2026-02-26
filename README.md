# ECG Carpets


Paper: [T. Gradowski, D. Waląg, T. Domański, T. Buchner: A novel method for analysis of transient morphological changes in quasiperiodic physiological signals and their neurogenic correlates (2026)](https://arxiv.org/abs/2602.19264)


![](screenshot.png)

## Requirements
- pyside6
- pyqtgraph
- neurokit2
- wfdb
- ishneholterlib

## Supported ECG file formats
- wfdb
- ishne
- AMEDTEC ECGPro

## Running the application
```bash
python main.py
```

## Known issues
- PySide6 6.9.1 breaks PyQtGraph
- upstream IshneHolterLib is not compatible with current NumPy, we provide patched version 