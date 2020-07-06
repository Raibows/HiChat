# import tkinter as tk
#
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
# tk.Button(root, text = "Insert", command = lambda :add_image(img)).pack()
#
# img = tk.PhotoImage(file = "pics/welcome.png")
#
# root.mainloop()
#
# x = tk.BooleanVar(root, value=False)
# print(x)

import tkinter as tk

class PageCanvas1(tk.Toplevel):
    def __init__(self, parent):
        global arr # why use global? set it as an attribute?
        global users # same as above?
        arr = {}
        tk.Toplevel.__init__(self, parent)
        self.title('Canvas')
        self.geometry('400x600')
        canvas = tk.Canvas(self, bg='white', scrollregion=(0, 0, 400, 20000))
        canvas.pack(fill='both', expand=True)

        vbar = tk.Scrollbar(canvas, orient='vertical')
        vbar.pack(side='right', fill='y')
        vbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=vbar.set)
        canvas.create_text(5, 0, anchor='nw', text="Choose users: ")
        # we need a container widget to put into the canvas
        f = tk.Frame(canvas)
        # you need to create a window into the canvas for the widget to scroll
        canvas.create_window((200, 0), window=f, anchor="n")
        for i in range(0, 1000):
            arr[i] = tk.IntVar()
            # widget must be packed into the container, not the canvas
            tk.Checkbutton(f, text=str(i), variable=arr[i]).pack()#.grid(row=i, sticky=W)

if __name__ == "__main__":
    app = PageCanvas1(None)
    app.mainloop()