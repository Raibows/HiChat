import tkinter as tk
import tkinter.messagebox


window = tk.Tk()
window.title('title')
window.geometry('300x300+500+300')

# var = tk.StringVar()
# var1 = tk.BooleanVar()
# var2 = tk.BooleanVar()
#
# l = tk.Label(window, bg='yellow', width=4, textvariable=var)
# l.pack()
#
# def print_func():
#     if var1.get() and var2.get():
#         var.set('both')
#     else:
#         var.set('0')
#
# canvas = tk.Canvas(window, bg='blue', height=500, width=500)
# image_file = tk.PhotoImage(file="pic07-06-13-18-25.png")
# image = canvas.create_image(0, 0, anchor='center', image=image_file)
#
# canvas.pack()
#
# def moveit():
#     canvas.move(image, 20, 20)
#
# c1 = tk.Checkbutton(window, text='123', variable=var1, onvalue=True, offvalue=False, command=print_func)
# c2 = tk.Checkbutton(window, text='456', variable=var2, onvalue=True, offvalue=False, command=print_func)
#
#
# s = tk.Scale(window, label='try move', from_=5, to=10, orient=tk.VERTICAL, length=200,
#              showvalue=True, tickinterval=1, resolution=0.01)
#
# s.pack()
# c1.pack()
# c2.pack()


def hit_me():
    tk.messagebox.showinfo(title='error', message='errrrrrrrrr')

fram = tk.Frame(window).pack()
fram_l = tk.Frame(fram)
fram_l.pack(side='left')
fram_r = tk.Frame(fram)
fram_r.pack(side='right')

b = tk.Button(fram_l, text='move', command=hit_me).pack()
tk.Label(fram_l, text='left frame').place(x=10, y=10)
tk.Label(fram_l, text='left2 frame').pack()
tk.Label(fram_r, text='right frame').pack()

window.mainloop()