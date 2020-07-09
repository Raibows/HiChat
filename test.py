import tkinter as tk
import pickle
from PIL import Image
from tools import *

# def add_image(img):
#     text.config(state=tk.NORMAL)
#     text.image_create(tk.END, image = img) # Example 1
#     # text.window_create(tk.END, window=tk.Label(text, image=img))
#     text.insert(tk.END, '\n')
#     text.config(state=tk.DISABLED)
#
# root = tk.Tk()
#
# text = tk.Text(root, state=tk.DISABLED)
# text.pack(padx = 20, pady = 20)
#
# tk.Button(root, text = "Insert", command = lambda :add_image(photo)).pack()
#
# img = open("pics/welcome.png", 'rb').read()
# print(img.decode('utf-8'))
# photo = tk.PhotoImage(data=img)
# # print(pickle.dumps(img))
#
# root.mainloop()
#
# x = tk.BooleanVar(root, value=False)
# print(x)


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
    test = []
    root = tk.Tk()
    root.geometry('800x500+300+150')
    frm = tk.Frame(root, bg='green')
    frm.place(x=100, y=100, width=700, height=400)
    output = tk.Text(frm, state=tk.NORMAL, font=('仿宋', 20))
    output.place(x=0, y=0, width=700, height=350)
    output_scroll_bar = tk.Scrollbar(frm, command=output.yview, orient='vertical')
    output_scroll_bar.pack(side='right', fill=tk.Y)
    output.config(yscrollcommand=output_scroll_bar.set)

    other = tk.Text(frm, state=tk.NORMAL, font=('仿宋', 20), bg='red')
    other.place(x=0, y=0, width=700, height=350)
    output_scroll_bar.config(command=other.yview, orient='vertical')
    other.config(yscrollcommand=output_scroll_bar.set)
    # test.append(output)

    output.config(yscrollcommand=output_scroll_bar.set, bg='white')
    output_scroll_bar.config(command=output.yview)
    output.tkraise()

    other.tkraise()



    root.mainloop()
    x = {
        '1':[[1, 2, 3], ]
    }
    pass