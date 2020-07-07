import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.simpledialog import askstring
from tkinter import ttk
from client import TCPClient
from queue import Queue, PriorityQueue


class LoginPanel():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('登录')
        self.root.geometry('500x380+400+300')
        self.font = ("仿宋", 16, "bold")
        self.client = TCPClient()

        # header
        self.header = tk.Canvas(self.root)
        self.image_file = tk.PhotoImage(file='pics/welcome.png')
        self.image_file = self.image_file.subsample(2, 2)
        self.header.place(x=0, y=0, width=380, height=200)
        self.header.create_image(210, 5, anchor='nw', image=self.image_file)


        # input
        self.input = tk.Canvas(self.root, bg='#ffffff')
        self.input.place(x=0, y=130, heigh=250, width=500)

        self.btn_login = tk.Button(self.input, text='登陆', bg='#99FFFF', command=self.btn_login_click_event)
        self.btn_login.place(x=120, y=160, heigh=50, width=100)
        self.btn_register = tk.Button(self.input, text='注册', bg='#FFFF99', command=self.btn_register_click_event)
        self.btn_register.place(x=280, y=160, height=50, width=100)

        self.lab_account = tk.Label(self.input, text='账户', font=self.font)
        self.lab_account.place(x=90, y=30)
        self.ent_account = tk.Entry(self.input, font=self.font)
        self.ent_account.place(x=160, y=30)
        self.lab_password = tk.Label(self.input, text='密码', font=self.font)
        self.lab_password.place(x=90, y=90)
        self.ent_password = tk.Entry(self.input, font=self.font, show='*')
        self.ent_password.place(x=160, y=90)


    def check_account_password(self, account, password):
        account_len = len(account)
        password_len = len(password)
        flag = True
        if account_len == 0 or password_len == 0:
            flag = False
            messagebox.showerror(message='账户和密码不能为空', parent=self.root)
        elif account_len > 6:
            flag = False
            messagebox.showerror(message='账户最多为6位', parent=self.root)
        elif password_len > 6:
            flag = False
            messagebox.showerror(message='密码最多为6位', parent=self.root)
        return flag

    def btn_login_click_event(self):
        acc = self.ent_account.get()
        pwd = self.ent_password.get()
        if self.check_account_password(acc, pwd):
            if self.client.login(acc, pwd):
                messagebox.showinfo(message='登录成功！', parent=self.root)
            else:
                messagebox.showerror(message='密码错误！', parent=self.root)

    def btn_register_click_event(self):
        register_window = RegisterPanel(self.root, self.client)
        register_window.run()

    def run(self):
        self.root.mainloop()

class RegisterPanel:
    def __init__(self, window:tk.Tk, client:TCPClient):
        self.root = tk.Toplevel(window)
        self.root.title('注册')
        self.root.geometry('450x350+400+200')
        self.font = ("仿宋", 16, "bold")
        self.client = client
        tk.Label(self.root, text='注册', font=("仿宋", 22, "bold")).place(x=200, y=20)

        self.input = tk.Canvas(self.root, bg='#ffffff')
        self.input.place(x=0, y=60, height=290, width=450)

        self.btn_login = tk.Button(self.input, text='注册', bg='#99FFFF', command=self.btn_register_click_event)
        self.btn_login.place(x=120, y=220, heigh=50, width=100)
        self.btn_register = tk.Button(self.input, text='取消', bg='#FFFF99', command=self.btn_cancel_click_event)
        self.btn_register.place(x=280, y=220, height=50, width=100)

        self.lab_account = tk.Label(self.input, text='账户', font=self.font)
        self.lab_account.place(x=90, y=30)
        self.ent_account = tk.Entry(self.input, font=self.font)
        self.ent_account.place(x=160, y=30)

        self.lab_password = tk.Label(self.input, text='密码', font=self.font)
        self.lab_password.place(x=90, y=90)
        self.ent_password = tk.Entry(self.input, font=self.font, show='*')
        self.ent_password.place(x=160, y=90)

        self.lab_password_con = tk.Label(self.input, text='确认', font=self.font)
        self.lab_password_con.place(x=90, y=150)
        self.ent_password_con = tk.Entry(self.input, font=self.font, show='*')
        self.ent_password_con.place(x=160, y=150)


    def check(self, acc, pwd, pwd_con):
        acc_len = len(acc)
        pwd_len = len(pwd)
        pwd_con_len = len(pwd_con)
        flag = True
        if acc_len == 0 or pwd_len == 0 or pwd_con_len == 0:
            flag = False
            messagebox.showerror(message='请填写完整', parent=self.root)
        elif acc_len > 6 or pwd_len > 6:
            flag = False
            messagebox.showerror(message='账号或密码不能大于6位', parent=self.root)
        elif pwd != pwd_con:
            flag = False
            messagebox.showerror(message='密码两次输入不一致', parent=self.root)
        return flag



    def btn_register_click_event(self):
        acc, pwd = self.ent_account.get(), self.ent_password.get()
        if self.check(acc, pwd, self.ent_password_con.get()):
            if self.client.register(acc, pwd):
                messagebox.showinfo(message='注册成功', parent=self.root)
                self.root.destroy()
            else:
                messagebox.showerror(message='注册失败，换一个账号试试', parent=self.root)

    def btn_cancel_click_event(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()





if __name__ == '__main__':
    t = LoginPanel()
    t.run()
