from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
from tkinter import filedialog
import matplotlib.colors as mcolors
import matplotlib.patches as mpatch

plt.rcParams.update({'font.size':24})
root = Tk()
root.title("Selct RMSD files to be plotted")
root.geometry("900x800")


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

"""
def random_color():
    levels = range(32,256,32)
    return tuple(random.choice(levels) for _ in range(3))
"""
def browsefunc():
    global filename
    filename = filedialog.askopenfilename()
    pathlabel.config(text=filename)

def addbox():
    global e
    browsebutton = Button(root, text="Browse", command=browsefunc)
    browsebutton.grid(row = 5, column = 1,sticky = W)
    leg_label = Label(root, text= "Enter legend name:", font =("Helvetica", "10") )
    leg_label.grid(row = 5,column =2)
    e = Entry(root, width = 20)
    e.grid(row = 5,column = 3,sticky = E)



my_label = Label(root, text= "Add file: select xvg file(s)\n Plot: plot the graph \n Save: save high res image \n Show map: shows colour map \n Enter curve name for the legend and color code from the map", font =("Helvetica", "15"))
my_label.grid(row = 0,column =1, sticky=E)

f, ax = plt.subplots(figsize=(20, 10))
ax.set_xlabel("Time (ns)", fontsize="35",  labelpad=25)
ax.set_ylabel("RMSD (nm)", fontsize="35" , labelpad=25)
plt.ion()


pathlabel = Label(root)
pathlabel.grid(row =1, column = 1 )

col_label = Label(root, text= "Enter the color code from color map", font =("Helvetica", "10") )
col_label.grid(row = 7,column =1)
colorcode = Entry(root)
colorcode.grid(row = 7,column = 2,sticky = E)


def clicked1():
    (x, y) = processxvg(filename)
    ax.plot(x,y)
    ax.plot(x,y,label = e.get(), color = colorcode.get())
    ax.legend(bbox_to_anchor=(1, 1))
    plt.show()

def savefile():
    (x, y) = processxvg(filename)
    ax.plot(x,y)
    ax.plot(x,y,label = e.get(),color = colorcode.get())
    ax.legend(bbox_to_anchor=(1, 1))
    plt.savefig("High resoltion.jpeg",dpi=800)

def showcolourmap():

    overlap = {name for name in mcolors.CSS4_COLORS
               if f'xkcd:{name}' in mcolors.XKCD_COLORS}

    fig = plt.figure(figsize=[9, 5])
    ax = fig.add_axes([0, 0, 1, 1])

    n_groups = 3
    n_rows = len(overlap) // n_groups + 1

    for j, color_name in enumerate(sorted(overlap)):
        css4 = mcolors.CSS4_COLORS[color_name]
        xkcd = mcolors.XKCD_COLORS[f'xkcd:{color_name}'].upper()

        # Pick text colour based on perceived luminance.
        rgba = mcolors.to_rgba_array([css4, xkcd])
        luma = 0.299 * rgba[:, 0] + 0.587 * rgba[:, 1] + 0.114 * rgba[:, 2]
        css4_text_color = 'k' if luma[0] > 0.5 else 'w'
        xkcd_text_color = 'k' if luma[1] > 0.5 else 'w'

        col_shift = (j // n_rows) * 3
        y_pos = j % n_rows
        text_args = dict(fontsize=10, weight='bold' if css4 == xkcd else None)
        ax.add_patch(mpatch.Rectangle((0 + col_shift, y_pos), 1, 1, color=css4))
        ax.add_patch(mpatch.Rectangle((1 + col_shift, y_pos), 1, 1, color=xkcd))
        ax.text(0.5 + col_shift, y_pos + .7, css4,
                color=css4_text_color, ha='center', **text_args)
        ax.text(1.5 + col_shift, y_pos + .7, xkcd,
                color=xkcd_text_color, ha='center', **text_args)
        ax.text(2 + col_shift, y_pos + .7, f'  {color_name}', **text_args)

    for g in range(n_groups):
        ax.hlines(range(n_rows), 3*g, 3*g + 2.8, color='0.7', linewidth=1)
        ax.text(0.5 + 3*g, -0.3, 'X11/CSS4', ha='center')
        ax.text(1.5 + 3*g, -0.3, 'xkcd', ha='center')

    ax.set_xlim(0, 3 * n_groups)
    ax.set_ylim(n_rows, -1)
    ax.axis('off')

    plt.show()



add_files_button = Button(root, text ="Add files", command = addbox)
add_files_button.grid(row = 2, column = 1)

plotbutton = Button(root, text ="Plot", command = clicked1 )
plotbutton.grid(row = 2, column = 2)

save_button = Button(root, text ="Save", command = savefile)
save_button.grid(row = 4, column = 1)

colourmapbutton = Button(root, text ="Show map", command = showcolourmap)
colourmapbutton.grid(row = 4, column = 2)


root.mainloop()

 
