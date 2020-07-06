import tkinter as tk
from PIL import Image, ImageTk

window = tk.Tk()
window.title('Login')
window.geometry('550x350')

canvas = tk.Canvas(window, height=200, width=500)
image_file = tk.PhotoImage(file='pics/welcome.png')
image_file = image_file.subsample(2, 2)

# image_file = Image.open('pics/welcome.png')
# image_file = image_file.resize((50, 50), Image.ANTIALIAS)
# image_file = ImageTk.PhotoImage(image_file)

image = canvas.create_image(200, 0, anchor='nw', image=image_file)
canvas.pack(side='top')

tk.Label(window, text='Username').place(x=50, y=150)
tk.Label(window, text='Password').place(x=50, y=200)

var_username = tk.StringVar()
var_password = tk.StringVar()
entry_username = tk.Entry(window, textvariable=var_username)
entry_username.place(x=160, y=150)
entry_password = tk.Entry(window, textvariable=var_password, show='*')
entry_password.place(x=160, y=200)

def user_login():
    pass

def user_register():
    window_register = tk.Toplevel(window)
    window_register.geometry('350x300')
    window_register.title('Register')
    entry_username = tk.Entry(window_register, textvariable=var_username)
    entry_username.place(x=160, y=150)
    entry_password = tk.Entry(window_register, textvariable=var_password, show='*')
    entry_password.place(x=160, y=200)
    entry_password_confirm = tk.Entry(window_register, textvariable=var_password, show='*')
    entry_password_confirm.place(x=160, y=250)
    # window_register.destroy()

btn_login = tk.Button(window, text='Login', command=user_login)
btn_login.place(x=180, y=250)
btn_reigister = tk.Button(window, text='Register', command=user_register)
btn_reigister.place(x=250, y=250)






window.mainloop()