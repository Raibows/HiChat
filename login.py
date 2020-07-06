import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.simpledialog import askstring
from tkinter import ttk





class MainPanel():
    def __init__(self):
        self.root = tk.Tk() # create window
        self.root.title("Hi Chat")
        self.root.geometry("900x700+300+100")
        self.root.resizable(0, 0)
        
        
        
        self.frame_header = tk.Frame(self.root, bg='#FFFFCC')
        self.frame_header.place(x=0, y=0, width=900, height=30)
    

        self.frame_right_bar = tk.Frame(self.root, bg='#C0C0C0')
        self.frame_right_bar.place(x=650, y=30, width=250, height=620)

        self.canvas_right_bar = tk.Canvas(self.frame_right_bar)
        self.canvas_right_bar.place(x=0, y=0, width=250, height=620)
        self.right_scroll_bar = tk.Scrollbar(self.frame_right_bar, orient='vertical', command=self.canvas_right_bar.yview)
        self.right_scroll_bar.pack(side='right', fill=tk.Y)
        self.canvas_right_bar.config(yscrollcommand=self.right_scroll_bar.set)
        self.groups = {}
        default_group = tk.Button(self.canvas_right_bar, text='default', width=20, height=2)
        self.groups['default'] = ([], default_group)
        self.canvas_right_bar.create_window(0, 0, window=default_group)
        self.canvas_right_bar.configure(scrollregion=self.canvas_right_bar.bbox("all"))



        
        self.frame_right_bottem = tk.Frame(self.root)
        self.frame_right_bottem.place(x=650, y=650, width=250, height=50)
        self.btn_add_user = tk.Button(self.frame_right_bottem, text='添加用户', font=('仿宋', 18), bg='#00CCCC',
                                      command=self.add_user)
        self.btn_add_user.place(x=10, y=0)
        self.btn_add_group = tk.Button(self.frame_right_bottem, text='创建群组', font=('仿宋', 18), bg='#FF6699',
                                      command=self.add_group)
        self.btn_add_group.place(x=120, y=0)
        
        
    
        self.frame_chat = tk.Frame(self.root, bg='white')
        self.frame_chat.place(x=0, y=30, width=650, height=520)
        self.output = tk.Text(self.frame_chat, state=tk.NORMAL, font=('仿宋', 20))
        self.output.place(x=0, y=0, width=650, height=520)
        self.output_scroll_bar = tk.Scrollbar(self.frame_chat, command=self.output.yview, orient='vertical')
        self.output_scroll_bar.pack(side='right', fill=tk.Y)
        self.output.config(yscrollcommand=self.output_scroll_bar.set)
        

        
        self.frame_user_input = tk.Frame(self.root)
        self.frame_user_input.place(x=0, y=520, width=650, height=180)
        self.user_input = tk.Text(self.frame_user_input, font=('仿宋', 18))
        self.user_input.place(x=0, y=0, width=635, height=130)
        self.btn_user_input_ok = tk.Button(self.frame_user_input, text='发送', font=('仿宋', 18), bg='#99FF99', command=lambda :self.get_text_data(self.user_input))
        self.btn_user_input_ok.place(x=560, y=130)
        self.btn_user_input_browse = tk.Button(self.frame_user_input, text='文件', font=('仿宋', 18), bg='#66FFFF', command=self.ask_open_file)
        self.btn_user_input_browse.place(x=470, y=130)

        self.friend_users = set()


    def add_user(self):
        user_window = AddUserPanel(self.root, self.groups, self.friend_users)
        # user = askstring(title='Add User', prompt='请输入对方账户')
        # print(user)

    def add_group(self):
        group_window = GroupManagePanel(self, self.groups, self.friend_users)
        group_window.run()

    def ask_open_file(self):
        file = filedialog.askopenfile(mode='r')
        print(file)

    def get_text_data(self, text: tk.Text):
        text_content = text.get('1.0', tk.END).strip('\n')
        text.delete('1.0', tk.END)
        print(text_content)


    def run(self):
        self.root.mainloop()


class GroupManagePanel():
    def __init__(self, other:MainPanel, groups:dict, users:set):
        self.parent = other
        self.root = tk.Toplevel(other.root)
        self.root.title('用户组管理')
        self.root.geometry('600x500+300+300')
        self.font = ('仿宋', 18)

        tk.Label(self.root, text='用户组', font=self.font).place(x=0, y=10, width=100)
        tk.Label(self.root, text='数量', font=self.font).place(x=100, y=10, width=100)
        tk.Label(self.root, text='用户', font=self.font).place(x=200, y=10, width=50)
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.place(x=0, y=50, width=600, height=400)
        self.canvas = tk.Canvas(self.canvas_frame, bg='white')
        self.canvas.place(x=0, y=0, width=600, height=2000)
        self.hbar = tk.Scrollbar(self.canvas, orient=tk.HORIZONTAL)
        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.hbar.config(command=self.canvas.xview)
        self.vbar = tk.Scrollbar(self.canvas, orient=tk.VERTICAL)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.vbar.config(command=self.canvas.yview)

        self.frame = tk.Frame(self.root)
        self.frame.place(x=0, y=400, width=600, height=100)
        self.btn_ok = tk.Button(self.frame, bg='green', text='更改')
        self.group_choice = ttk.Combobox(self.frame, values=list(groups.keys()), state='readonly', )
        self.group_choice.current(list(groups.keys()).index('default'))
        self.btn_new = tk.Button(self.frame, bg='#FFFF00', text='新建', command=self.btn_new_event)

        self.btn_ok.place(x=100, y=30, width=50)
        self.group_choice.place(x=220, y=30)
        self.btn_new.place(x=470, y=30, width=50)


        self.groups = groups
        self.users = users
        self.vars = {}
        self.show()

    def show(self):
        self.canvas.delete('all')
        for row, (key, val) in enumerate(self.groups.items()):
            tk.Label(self.canvas, bg='#FFFF99', text=f"{key}", font=self.font, width=8).place(x=0, y=50*row)
            tk.Label(self.canvas, text=f"{len(val[0])}", font=self.font, width=8).place(x=100, y=50*row)
            self.vars[key] = [tk.BooleanVar(self.canvas, value=False) for _ in val[0]]
            for column, user in enumerate(val[0]):
                tk.Checkbutton(self.canvas, variable=self.vars[key][column], onvalue=True, offvalue=False,
                               text = user).place(x=200+column*100, y=50*row, width=100)



        self.canvas.config(scrollregion=self.canvas.bbox('all'),
                           xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)


    def btn_new_event(self):
        group = askstring(title='Add Group', prompt='请输入新用户组', parent=self.root)
        if group == None: return None
        if len(group) > 6:
            messagebox.showerror(message='用户组不能超过6个字符！', parent=self.root)
            return None
        if group in self.groups:
            messagebox.showerror(message='用户组重复！', parent=self.root)
            return None
        self.groups[group] = ([], tk.Button(self.parent.canvas_right_bar, text='default', width=20, height=2))
        self.show()

    def quit(self):
        self.root.quit()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


class AddUserPanel():
    def __init__(self, parent:tk.Tk, groups, users:set):
        self.parent = parent
        self.root = tk.Toplevel(parent)
        self.root.title('添加联系人')
        self.root.geometry('360x160+300+300')
        self.font = ('仿宋', 18)
        self.users = users
        self.groups = groups
        self.user_accounts= {x[0] for x in self.users}

        self.lb_ent_account = tk.Label(self.root, font=self.font, text='对方账户')
        self.ent_account = tk.Entry(self.root, font=self.font)
        self.lb_ent_account.grid(row=0, column=0)
        self.ent_account.grid(row=0, column=1)

        self.lb_groups = tk.Label(self.root, font=self.font, text='选择群组')
        self.group_choice = ttk.Combobox(self.root, values=list(groups.keys()), state='readonly',)
        self.group_choice.current(list(groups.keys()).index('default'))
        self.lb_groups.grid(row=1, column=0)
        self.group_choice.grid(row=1, column=1)

        self.btn_ok = tk.Button(self.root, text='提交', font=self.font, bg='green', command=self.btn_ok_event)
        self.btn_cancel = tk.Button(self.root, text='取消', font=self.font, bg='red', command=self.quit)
        self.btn_ok.place(x=110, y=100)
        self.btn_cancel.place(x=210, y=100)

        self.root.mainloop()

        g = 'default'
        for u in range(100000, 100015):
            u = str(u)
            self.users.add((u, g))
            self.user_accounts.add(u)
            self.groups[g][0].append(u)

    def btn_ok_event(self):
        u, g = self.ent_account.get(), self.group_choice.get()
        if len(u) == 0 or len(g) == 0:
            messagebox.showerror(message='账号或群组不能为空!', parent=self.root)
        elif len(u) > 6:
            messagebox.showerror(message='账号不能大于6位', parent=self.root)
        elif u in self.user_accounts:
            messagebox.showerror(message='该好友已经添加', parent=self.root)
        else:
            self.users.add((u, g))
            self.user_accounts.add(u)
            self.groups[g][0].append(u)
            messagebox.showinfo(message='添加成功', parent=self.root)


    def quit(self):
        self.root.quit()
        self.root.destroy()

if __name__ == '__main__':
    root = MainPanel()
    root.run()


