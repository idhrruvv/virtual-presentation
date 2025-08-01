import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.filedialog import askopenfilename
import win32com.client
from pdf2image import convert_from_path
import os
from Presentaion import presentationWindow as pd


popper_path = "poppler-24.08.0\\Library\\bin"
# Window Tools - Header
root = ttk.Window(themename='superhero')
root.geometry("1280x720")
root.title("Virtual AI Presentation App")

# Variables
TextBox1Value = tk.StringVar()

base = 'temp-data'

# User Funcions

def Btn1_click():
    folderName = TextBox1Value.get()
    path = os.path.join(base, folderName)
    print(path)
    try :
        if folderName == "":
            label1.config(text='*Enter the Name of Presentation', bootstyle=(DANGER))
            return
        elif folderName in [i for i in os.listdir(f'{base}')]:
            if len([i for i in os.listdir(f'{path}')]):
                pd(folderName)
                return 
            else:
                label1.config(text='', bootstyle="primary", width=60, font=("consolas", 18))
                file = askopenfilename()
                label1.config(text=f'{file}', bootstyle="primary", width=60, font=("consolas", 18))
                os.mkdir(path)

        if folderName in [i for i in os.listdir(f'{base}')]:
            label1.config(text='', bootstyle="primary", width=60, font=("consolas", 18))
            file = askopenfilename()
            label1.config(text=f'{file}', bootstyle="primary", width=60, font=("consolas", 18))
        else:
            label1.config(text='', bootstyle="primary", width=60, font=("consolas", 18))
            file = askopenfilename()
            label1.config(text=f'{file}', bootstyle="primary", width=60, font=("consolas", 18))
            os.mkdir(path)

        ext = file.split('.')[-1]
        if ext in ['pptx', 'pdf','ppt']:
            label1.config(text=file)
            if ext == 'pptx':
                powerpoint = win32com.client.Dispatch("Powerpoint.Application")
                img = powerpoint.Presentations.Open(file, WithWindow=False)
                img.SaveAs(f'{os.getcwd()}\\{path}', 18)
                img.Close()
                pd(folderName)
            elif ext == 'ppt':
                powerpoint = win32com.client.Dispatch("Powerpoint.Application")
                img = powerpoint.Presentations.Open(file, WithWindow=False)
                img.SaveAs(f'{os.getcwd()}\\{path}', 18)
                img.Close()
                pd(folderName)
            elif ext == 'pdf':
                pages = convert_from_path(file, poppler_path=popper_path)
                for i, page in enumerate(pages):
                    imgname = f'{i + 1}.png'
                    page.save(os.path.join(f'{path}\\', imgname), 'PNG')
                pd(folderName)
            else:
                label1.config(text='Invalid File Choosed ,It can be PPTX or PDF', bootstyle = (DANGER))
            # Rename All Images
            Pdata = f'{base}\\{folderName}'
            images = sorted(os.listdir(Pdata), key=len)

            for num, i in enumerate(images):
                oldpath = os.path.join(Pdata, i)
                newpath = os.path.join(Pdata, f'{num + 1}.png')
                os.rename(oldpath, newpath)
            label1.config(text='', bootstyle=(PRIMARY))
        else:
            label1.config(text='Invalid File Type', bootstyle=(DANGER))
    except Exception as e:
        label1.config(text=e, bootstyle=(DANGER),font=("consolas",10))

def Btn2_click():
    folderName = TextBox1Value.get()
    path = os.path.join(base, folderName)
    try:
        if folderName in [i for i in os.listdir(base)]:
            for i in os.listdir(path):
                os.remove(f'{path}//{i}')
            os.rmdir(path)
            label1.config(text='')
        elif folderName == '':
            label1.config(text='Enter the Presentation Name', bootstyle=(DANGER))
        elif folderName not in [i for i in os.listdir(base)]:
            label1.config(text='Presentation Dosen\'t Exist', bootstyle=(DANGER))
        else:
            label1.config(text='Invalid File Type', bootstyle=(DANGER))
    except Exception as e:
        label1.config(text=e, bootstyle=(DANGER))


current_presentations = []
label_presentations = []

# Window Tools - Body

Title_Label = ttk.Label(root, text="Upload Files of PowerPoint,PDF...", font=("consolas", 28), justify=CENTER, bootstyle=(LIGHT))
Title_Label.pack(pady=0,padx=10)

TextBox1 = ttk.Entry(root, bootstyle="primary", width=60, textvariable=TextBox1Value)
TextBox1.pack(pady=50,padx=50)
btn1 = ttk.Button(root, text="Upload", command=Btn1_click)
btn1.pack(pady=50,padx=50)
btn2 = ttk.Button(root, text="Remove", bootstyle = (DANGER),command=Btn2_click)
btn2.pack(pady=0,padx=50)

label1 = ttk.Label(root, bootstyle="primary", width=60, font=("consolas", 18))
label1.pack(pady=0,padx=0,ipadx=10)

root.mainloop()

