import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo
from tkinter import END
import po2resizer

g_threshold = 0.5
g_max_res = 8192


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Power of 2 Texture Resizer')

        window_width = 740
        window_height = 350
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.input_dir = ""
        self.output_dir = ""
        self.threshold = g_threshold
        self.max_res = g_max_res
        self.to_jpg = 1
        self.jpg_quality = 95
        self.compression = 5

        #INPUT
        self.input_folder_label = ttk.Label(self, text='Input image folder:')
        self.input_folder_label.grid(column=0, row=0, sticky=tk.W, padx=20,pady=20)

        self.input_folder_text_var = tk.StringVar()
        self.input_folder_path_entry = ttk.Entry(self, textvariable=self.input_folder_text_var, width=70)
        self.input_folder_path_entry.grid(column=1, row=0)

        self.input_folder_path_button = ttk.Button(self, text='Browse...', command=lambda: self.browse_dir_button(self.input_dir, self.input_folder_text_var, self.input_folder_path_entry))
        self.input_folder_path_button.grid(column=2, row=0, sticky=tk.W, padx=10)

        #OUTPUT
        self.output_folder_label = ttk.Label(self, text='Output image folder:')
        self.output_folder_label.grid(column=0, row=1, sticky=tk.W, padx=20,pady=5)

        self.output_folder_text_var = tk.StringVar()
        self.output_folder_path_entry = ttk.Entry(self, textvariable=self.output_folder_text_var, width=70)
        self.output_folder_path_entry.grid(column=1, row=1)

        self.output_folder_path_button = ttk.Button(self, text='Browse...', command=lambda: self.browse_dir_button(self.output_dir, self.output_folder_text_var, self.output_folder_path_entry))
        self.output_folder_path_button.grid(column=2, row=1, sticky=tk.W, padx=10)

        
        #THRESHOLD
        self.threshold_label = ttk.Label(self, text='Upscale threshold (0-1):')
        self.threshold_label.grid(column=0, row=2, sticky=tk.W, padx=20, pady=20)

        self.threshold_text_var = tk.IntVar()
        self.threshold_text_var.set(self.threshold)
        self.threshold_entry = ttk.Entry(self, textvariable=self.threshold_text_var, width=10, justify="right")
        self.threshold_entry.grid(column=1, row=2, sticky=tk.W)


        #MAX RESOLUTION
        self.maxres_label = ttk.Label(self, text='Max. dimension:')
        self.maxres_label.grid(column=0, row=3, sticky=tk.W, padx=20)

        self.maxres_text_var = tk.IntVar()
        self.maxres_text_var.set(self.max_res)
        self.maxres_entry = ttk.Entry(self, textvariable=self.maxres_text_var, width=10, justify="right")
        self.maxres_entry.grid(column=1, row=3, sticky=tk.W)


        #JPG
        self.checkbutton_var = tk.IntVar()
        self.checkbutton_var.set(self.to_jpg)
        self.to_jpg_checkbox = ttk.Checkbutton(self, text="Convert all images to JPEG", command=self.to_jpg_checkbutton, variable=self.checkbutton_var)
        self.to_jpg_checkbox.grid(column=0, row=4, sticky=tk.W, padx=20, pady=(40,10))


        self.quality_label = ttk.Label(self, text='JPEG quality (0-100):')
        self.quality_label.grid(column=0, row=5, sticky=tk.W, padx=(40,50))
        self.quality_text_var = tk.IntVar()
        self.quality_text_var.set(self.jpg_quality)
        #valid_quality_cmd = self.register(self.is_int_in_range('%P'))
        #on_invalid_quality_cmd = self.register(self.nok(), '%P')
        self.quality_entry = ttk.Entry(self, textvariable=self.quality_text_var, width=10, justify="right")
        self.quality_entry.grid(column=1, row=5, sticky=tk.W)


        self.execute_button = ttk.Button(self, text='Run', command=self.execute_button, width=20)
        self.execute_button.grid(column=1, columnspan = 2, row=6, sticky=tk.E, padx = 10, pady=40)

        self.help_button = ttk.Button(self, text='Help (todo)', command=self.execute_button)
        self.help_button.grid(column=0, row=6, sticky=tk.W, padx=20, pady=40)


    def execute_button(self):
        self.input_dir = self.input_folder_path_entry.get()
        self.output_dir = self.output_folder_path_entry.get()

        try:
            self.threshold = float(self.threshold_entry.get())
        except:
            self.threshold = g_threshold
        
        try:
            self.max_res = int(self.maxres_entry.get())
        except:
            self.max_res = g_max_res

        self.to_jpg = self.checkbutton_var.get()

        try:
            self.jpg_quality = int(self.quality_entry.get())
        except:
            self.jpg_quality = 0.95

        if self.threshold < 0 or self.threshold > 1:
           self.threshold = g_threshold
        if self.max_res < 0:
           self.max_res = g_max_res
        if self.jpg_quality > 100 or self.jpg_quality < 0:
           self.jpg_quality = 95

        #print(self.max_res)
        po2resizer.resizer(self.input_dir, self.output_dir, 1 - self.threshold, self.max_res, self.to_jpg, self.jpg_quality, self.compression)
        showinfo("Status", "Run finished.")


    def to_jpg_checkbutton(self):
        if self.checkbutton_var.get() == 0:
            self.to_jpg = 0
            self.quality_entry.config(state='disabled')
            self.quality_label.config(state='disabled')
        else:
            self.to_jpg = 1
            self.quality_entry.config(state='enabled')
            self.quality_label.config(state='enabled')

    def browse_dir_button(self, dir_var, entry_text_var, entry):
        dir_var = filedialog.askdirectory()
        entry_text_var.set(dir_var)
        entry.xview_moveto(1)
        
if __name__ == "__main__":
    app = App()
    app.mainloop()