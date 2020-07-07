import tkinter as tk
import pickle
from PIL import Image
from tools import *

def add_image(img):
    text.config(state=tk.NORMAL)
    text.image_create(tk.END, image = img) # Example 1
    # text.window_create(tk.END, window=tk.Label(text, image=img))
    text.insert(tk.END, '\n')
    text.config(state=tk.DISABLED)

root = tk.Tk()

text = tk.Text(root, state=tk.DISABLED)
text.pack(padx = 20, pady = 20)

tk.Button(root, text = "Insert", command = lambda :add_image(photo)).pack()

img = open("pics/welcome.png", 'rb').read()
print(img.decode('utf-8'))
photo = tk.PhotoImage(data=img)
# print(pickle.dumps(img))

root.mainloop()

x = tk.BooleanVar(root, value=False)
print(x)


# class PageCanvas1(tk.Toplevel):
#     def __init__(self, parent):
#         self.root = tk.Toplevel(parent)
#         self.root.title('Canvas')
#         self.root.geometry('400x600')
#         self.arr = {}
#         canvas = tk.Canvas(self.root, bg='white', scrollregion=(0, 0, 400, 20000))
#         # canvas.pack(fill='both', expand=True)
#         canvas.place(x=0, y=0, width=400, height=600)
#
#         vbar = tk.Scrollbar(canvas, orient='vertical')
#         vbar.pack(side='right', fill='y')
#         vbar.config(command=canvas.yview)
#         canvas.config(yscrollcommand=vbar.set)
#         canvas.create_text(5, 0, anchor='nw', text="Choose users: ")
#         # we need a container widget to put into the canvas
#         f = tk.Frame(canvas, bg='green')
#         f.place(x=0, y=0, anchor='nw')
#         # you need to create a window into the canvas for the widget to scroll
#         canvas.create_window(0, 0, window=f, anchor='nw')
#         for i in range(0, 20):
#             self.arr[i] = tk.IntVar()
#             # widget must be packed into the container, not the canvas
#             # tk.Checkbutton(f, text=str(i), variable=self.arr[i]).pack()#.grid(row=i, sticky=W)
#             temp = tk.Checkbutton(f, text=str(i), variable=self.arr[i], height=5)
#             temp.pack()
#             # temp.place(x=10, y=50*i, anchor='nw')
#             # f.pack(fill="both", expand=True)

if __name__ == "__main__":
    # root = tk.Tk()

    pass