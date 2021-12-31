import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

import os

from ishneholterlib import Holter
import wfdb
import neurokit2 as nk

W=512
H=512

def load_ishne(filename):
    record = Holter(filename)
    print(record.__dict__)

    record.load_data()
    return record.lead[0].data, record.sr

def load_mit(filename):
    record=wfdb.rdrecord(filename[:-4])
    print(record.__dict__)
    return record.p_signal[:,0], record.fs

def carpet(ecg, sampling_rate, start_sample=0, beats=H, left_off=W//2, right_off=W//2, method='neurokit'):
    # R-wave detection for a buffer, assuming <RR> < 2s
    _, rpeaks = nk.ecg_peaks(
        ecg[start_sample:start_sample+sampling_rate*2*beats], sampling_rate=sampling_rate, method=method)
    result = [ecg[r-left_off+start_sample:r+right_off+start_sample]
              for r in rpeaks['ECG_R_Peaks'][:beats]]
    r_first, r_last = rpeaks['ECG_R_Peaks'][0], rpeaks['ECG_R_Peaks'][beats]
    samples_range = (r_first-left_off+start_sample,
                     r_last+right_off+start_sample)
    return np.stack(result), samples_range


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # self.tk.call('tk', 'scaling', 4.0)


        self.geometry("1860x1020")
        self.wm_title("Tk Carpets")
        # self.option_add('*Font', '28')  # nie działa w Anacondzie!!

        leftframe = tk.Frame(self)
        rightframe = tk.Frame(self)

    # callbacks

        def toggle_update(*e):
            self.need_update = True

        def auto_update(*event):
            self.draw()

        def sigma_update(*e):
            if not self.var_auto.get():
                self.draw()
        
        def show_lead():
            ecg_window = tk.Toplevel()
            fig = Figure(figsize=(6, 2))
            ax = fig.add_subplot()
            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=ecg_window)
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            ax.plot(self.ecg)
            ax.grid()


    # variables

        self.var_cmap = tk.StringVar(value='jet')
        self.var_method = tk.StringVar(value='neurokit')
        self.var_sampling_rate = tk.IntVar(value=200)
        self.var_pos = tk.IntVar(value=1000)
        self.var_auto = tk.BooleanVar(value=True)
        self.var_range = tk.DoubleVar(value='1.0')
        self.var_range_min = tk.DoubleVar()
        self.var_range_max = tk.DoubleVar()
        self.need_update = False

        self.var_pos.trace('w', toggle_update)
        self.var_auto.trace('w', auto_update)
        self.var_cmap.trace('w', lambda *args: self.draw())
        self.var_method.trace('w', toggle_update)

    # labels
        self.label_filename = tk.Label(rightframe, text="filename")
        # label_sampling_rate = tk.Label(rightframe, text="sampling rate")        
        label_cmap = tk.Label(rightframe, text="colormap")
        label_method = tk.Label(rightframe, text="R-wave detection method")
        label_pos = tk.Label(rightframe, text='index')
        label_min = tk.Label(rightframe, text='min')
        label_max = tk.Label(rightframe, text='max')

    # buttons
        button_open = tk.Button(
            rightframe, text="Open ECG file", command=self.file_open)
        button_show_ecg = tk.Button(
            rightframe, text="Show ECG", command=show_lead)

        button_update = tk.Button(
            rightframe, text="Update", command=self.draw)
        button_save = tk.Button(
            rightframe, text="Save PNG", command=self.savefig)

    # figures

        self.fig = Figure(figsize=(6, 6))
        self.ax = self.fig.add_subplot()
        self.fig.tight_layout()


        self.fig_ecg, self.axs_ecg = plt.subplots(2, 1, figsize=(5, 3))
        self.fig_ecg.tight_layout()


        self.canvas_carpet = FigureCanvasTkAgg(self.fig, master=leftframe)
        self.canvas_ecg = FigureCanvasTkAgg(self.fig_ecg, master=rightframe)

    # widgets

        combo_cmap = ttk.Combobox(
            rightframe, textvariable=self.var_cmap)
        combo_cmap['values'] = ['jet', 'gray', 'jet_r', 'gray_r',
                                'inferno', 'cividis', 'Spectral', 'bwr', 'seismic']
        combo_cmap['state'] = 'readonly'

        combo_method = ttk.Combobox(
            rightframe, textvariable=self.var_method)
        combo_method['values'] = ['neurokit', 'pantompkins1985', 'hamilton2002', 'christov2004', 'gamboa2008',
                                  'elgendi2010', 'engzeemod2012', 'kalidas2017', 'martinez2003', 'rodrigues2021', 'promac']
        combo_method['state'] = 'readonly'

        # spinbox_sampling_rate = ttk.Spinbox(rightframe, from_=50, to=1000, increment=25, textvariable=self.var_sampling_rate)

        spinbox_pos = ttk.Spinbox(
            rightframe, from_=W, to=20000000, increment=200*60*10, textvariable=self.var_pos)

        spinbox_range_min = ttk.Spinbox(
            rightframe, from_=-10, to=10, increment=0.05, textvariable=self.var_range_min, command=self.draw_ecg)

        spinbox_range_max = ttk.Spinbox(
            rightframe, from_=-10, to=10, increment=0.05, textvariable=self.var_range_max, command=self.draw_ecg)

        check_auto = tk.Checkbutton(
            rightframe, text="autoscale", variable=self.var_auto)

    # layout
        leftframe.pack(side=tk.LEFT)
        rightframe.pack(side=tk.RIGHT)
        self.canvas_carpet.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.label_filename.pack()
        # label_sampling_rate.pack()
        # spinbox_sampling_rate.pack()
        button_open.pack()
        button_show_ecg.pack()        
        label_pos.pack()
        spinbox_pos.pack()
        label_method.pack()
        combo_method.pack()
        button_update.pack()

        check_auto.pack()

        label_max.pack()
        spinbox_range_max.pack()
        label_min.pack()
        spinbox_range_min.pack()

        label_cmap.pack(anchor=tk.CENTER)
        combo_cmap.pack()
        button_save.pack()

        self.canvas_ecg.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def make_carpet(self):
        self.carpet, (self.s_min, self.s_max) = carpet(self.ecg, sampling_rate=self.var_sampling_rate.get(), start_sample=self.var_pos.get(), beats=H,
                                                       left_off=W//2, right_off=W//2, method=self.var_method.get())
        self.cmean, self.cstdev = self.carpet.mean(), self.carpet.std()
        v_min = self.ecg[self.s_min:self.s_max].min()
        v_max = self.ecg[self.s_min:self.s_max].max()

        self.var_range_min.set(v_min)
        self.var_range_max.set(v_max)

    def file_open(self):
        fn=fd.askopenfilename(filetypes=(
            ('All files', '*.*'),
            ('Ishne ECG', '*.ecg'),
            ('MIT ECG', '*.hea')
        ))  # initialdir='../data'

        if fn=='':
            return

        file_ext=fn[-3:]
        if file_ext=='ecg':
            self.ecg, sampling_freq = load_ishne(fn)
        elif file_ext=='hea':
            self.ecg, sampling_freq = load_mit(fn)
        else:
            return
        
        self.var_sampling_rate.set(sampling_freq)
        self.filename=fn

        self.ecg = nk.ecg_clean(self.ecg, sampling_rate=self.var_sampling_rate.get())
        self.var_pos.set(W) # bug when 0
        self.make_carpet()
        print(f"Number of samples: {self.ecg.shape[0]}")
        self.label_filename.config(
            text=f"{self.filename} {self.ecg.shape[0]} samples")
        self.draw_ecg()
        self.draw()

    def draw(self):
        if self.need_update:
            self.make_carpet()
            self.need_update = False
            self.draw_ecg()
        t_ext = W/self.var_sampling_rate.get()
        cmap = plt.get_cmap(self.var_cmap.get())
        if self.var_auto.get():
            c_im = self.ax.imshow(self.carpet, cmap=cmap, extent=[-t_ext, t_ext, H, 0], aspect='auto')
        else:
            sigma = self.var_range.get()
            vmin = self.var_range_min.get()
            vmax = self.var_range_max.get()

            c_im = self.ax.imshow(
                self.carpet, cmap=cmap, extent=[-t_ext, t_ext, H, 0], aspect='auto', vmin=vmin, vmax=vmax)
            
        self.canvas_carpet.draw()

    def draw_ecg(self):
        x = np.arange(self.s_min, self.s_max)
        self.axs_ecg[0].cla()
        self.axs_ecg[1].cla()

        self.axs_ecg[0].grid()
        self.axs_ecg[1].grid()

        self.axs_ecg[0].plot(x, self.ecg[self.s_min:self.s_max], "k-")
        self.axs_ecg[0].plot(x, self.var_range_max.get()
                             * np.ones_like(x), "r--")
        self.axs_ecg[0].plot(x, self.var_range_min.get()
                             * np.ones_like(x), "r--")

        zoom = x.shape[0]//20
        self.axs_ecg[1].plot(
            x[:zoom], self.ecg[self.s_min:self.s_min+zoom], "g-", alpha=0.5)
        self.axs_ecg[1].plot(
            x[:zoom], self.ecg[self.s_max-zoom:self.s_max], "m-", alpha=0.5)

        self.axs_ecg[1].plot(x[:zoom], self.var_range_max.get()
                             * np.ones_like(x[:zoom]), "r--")
        self.axs_ecg[1].plot(x[:zoom], self.var_range_min.get()
                             * np.ones_like(x[:zoom]), "r--")

        self.canvas_ecg.draw()

    def savefig(self):

        fn = os.path.basename(self.filename)[:-4]
        pos = self.var_pos.get()
        sfn = f"{fn}_{pos}.png"
        self.fig.savefig(sfn)
        print(f"File saved: {sfn}")


app = App()
app.mainloop()
