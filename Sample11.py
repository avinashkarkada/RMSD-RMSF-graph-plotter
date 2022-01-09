from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
from tkinter import filedialog

plt.rcParams.update({'font.size':24})
root = Tk()
root.title("Selct RMSD files to be plotted")
root.geometry("500x300")


def processxvg(filename):
    x, y = [], []
    with open(filename) as f:
        for line in f:
            if line[0] != "#" and line[0] != "@":
                cols = line.split()
                if len(cols) == 2:
                    x.append(float(cols[0]))
                    y.append(float(cols[1]))
    return x,y

def random_color():
    levels = range(32,256,32)
    return tuple(random.choice(levels) for _ in range(3))

def browsefunc():
    global filename
    filename = filedialog.askopenfilename()
    pathlabel.config(text=filename)

def addbox():
    global e
    browsebutton = Button(root, text="Browse", command=browsefunc)
    browsebutton.grid(row = 5, column = 1,sticky = W)
    e = Entry(root, width = 20)
    e.grid(row = 5,column = 1,sticky = E)

my_label = Label(root, text= "Browse the xvg file in the dir", font =("Helvetica", "30") )
my_label.grid(row = 0,column =1)

f, ax = plt.subplots(figsize=(20, 10))
ax.set_xlabel("Time (ns)", fontsize="35",  labelpad=25)
ax.set_ylabel("RMSD (nm)", fontsize="35" , labelpad=25)
plt.ion()


pathlabel = Label(root)
pathlabel.grid(row =1, column = 1 )


def clicked1():
    (x, y) = processxvg(filename)
    ax.plot(x,y)
    ax.plot(x,y,label = e.get())
    ax.legend(bbox_to_anchor=(1, 1))
    plt.show()


add_files_button = Button(root, text ="Add files", command = addbox)
add_files_button.grid(row = 2, column = 1)

plotbutton = Button(root, text ="Plot", command = clicked1 )
plotbutton.grid(row = 3, column = 1)

root.mainloop()

