import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.simpledialog import askstring
from tkinter import ttk
from queue import Queue, PriorityQueue
from client import TCPClient
from tools import *
import time
import threading


class MainPanel():
    def __init__(self, username, client:TCPClient):
        self.root = tk.Tk() # create window
        self.root.title("Hi Chat")
        self.root.geometry("900x700+300+100")
        self.root.resizable(0, 0)
        self.username = username
        self.chat_with = ''
        self.client = client


        # header提示语
        self.frame_header = tk.Frame(self.root, bg='#FFFFCC')
        self.frame_header.place(x=0, y=0, width=900, height=30)
        tk.Label(self.frame_header, text=f'hello, {username}', font=('仿宋', 16)).place(x=680, y=5)
        self.chat_with_label = tk.Label(self.frame_header, text=f'{self.chat_with}', font=('仿宋', 16))
        self.chat_with_label.place(x=300, y=5)


        # 好友栏
        self.canvas_right_bar = tk.Canvas(self.root, scrollregion=(0, 0, 250, 2000))
        self.canvas_right_bar.place(x=650, y=30, width=250, height=620)
        self.right_scroll_bar = tk.Scrollbar(self.canvas_right_bar, orient='vertical', command=self.canvas_right_bar.yview)
        self.right_scroll_bar.pack(side='left', fill=tk.Y)
        self.canvas_right_bar.config(yscrollcommand=self.right_scroll_bar.set)
        self.frame_right_bar = tk.Frame(self.canvas_right_bar, bg='#C0C0C0')
        self.frame_right_bar.place(x=0, y=0)
        self.canvas_right_bar.create_window(20, 0, anchor='nw', window=self.frame_right_bar)

        self.groups = {}
        self.friend_users = set()
        self.create_new_group('default')
        self.update_groups()




        # 好友栏下部按钮
        self.frame_right_bottem = tk.Frame(self.root)
        self.frame_right_bottem.place(x=650, y=650, width=250, height=50)
        self.btn_add_user = tk.Button(self.frame_right_bottem, text='添加用户', font=('仿宋', 18), bg='#00CCCC',
                                      command=self.btn_add_user_event)
        self.btn_add_user.place(x=10, y=0)
        self.btn_add_group = tk.Button(self.frame_right_bottem, text='管理群组', font=('仿宋', 18), bg='#FF6699',
                                       command=self.btn_add_group_event)
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
        self.btn_user_input_ok = tk.Button(self.frame_user_input, text='发送', font=('仿宋', 18), bg='#99FF99',
                                           command=lambda :self.btn_get_text_data_event(self.user_input))
        self.btn_user_input_ok.place(x=560, y=130)
        self.btn_user_input_browse = tk.Button(self.frame_user_input, text='文件', font=('仿宋', 18), bg='#66FFFF',
                                               command=self.ask_open_file)
        self.btn_user_input_browse.place(x=470, y=130)

    def click_user_to_chat_event(self, event):
        widget = event.widget
        try:
            index = int(widget.curselection()[0])
        except:
            return None
        self.chat_with = widget.get(index)
        self.chat_with_label.config(text=self.chat_with)

    def create_new_group(self, group_name: str):
        frm = tk.Frame(self.frame_right_bar)
        btn = tk.Button(frm, text=group_name, width=23, height=2, bg='green',
                        command=lambda: self.btn_group_show_friends(group_name))
        btn.pack()
        self.groups[group_name] = [[], frm, 0]

    def btn_group_show_friends(self, group):
        group = self.groups[group]
        if group[2] == 0:
            if (len(group[0])) == 0: return None
            temp = tk.Listbox(group[1], font=('仿宋', 18))
            temp.bind('<<ListboxSelect>>', self.click_user_to_chat_event)
            for user in group[0]: temp.insert('end', user)
            temp.pack()
            group[2] = temp
        else:
            group[2].destroy()
            group[2] = 0
            self.update_groups()

    def update_groups(self):
        self.update_friend_users()
        # self.groups['default'][1].pack()
        for key, val in self.groups.items():
            # if key == 'default': continue
            val[1].pack(fill='both')

    def btn_add_user_event(self):
        user_window = AddUserPanel(self.root, self.groups)

    def btn_add_group_event(self):
        for g, val in self.groups.items():
            if val[2] != 0: self.btn_group_show_friends(g)
        group_window = GroupManagePanel(self, self.groups)
        print(1)
        group_window.run()
        print(2)
        self.update_groups()

    def output_one_message(self, data:MessageNode):
        header, msg = data.get_output()
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, header)
        if data.msg_type == 'pic':
            self.img = msg
            self.output.image_create(tk.END, image=msg)
            self.output.insert(tk.END, '\n')
        elif data.msg_type == 'text':
            self.output.insert(tk.END, msg)
        self.output.yview(tk.END)
        self.output.config(state=tk.DISABLED)

    def ask_open_file(self):
        file = filedialog.askopenfile(mode='r')
        temp = MessageNode('pic', time.time(), file.name, self.username, self.chat_with)
        self.output_one_message(temp)
        self.client.send_queue.put(
            temp
        )


    def btn_get_text_data_event(self, text: tk.Text):
        text_content = text.get('1.0', tk.END).strip('\n')
        text.delete('1.0', tk.END)
        temp = MessageNode('text', time.time(), text_content, self.username, self.chat_with)
        self.output_one_message(temp)
        self.client.send_queue.put(
            temp
        )

    def update_friend_users(self):
        self.friend_users.clear()
        for key, val in self.groups.items():
            [self.friend_users.add((x, key)) for x in val[0]]

    def run_output(self):
        while True:
            if self.client.receive_queue.empty():
                time.sleep(0.5)
                continue
            data = self.client.receive_queue.get()
            self.output(data)

    def run(self):
        output_thread = threading.Thread(target=self.run_output)
        self.root.mainloop()


class GroupManagePanel():
    def __init__(self, other: MainPanel, groups: dict):
        self.parent = other
        self.root = tk.Toplevel(other.root)
        self.root.title('用户组管理')
        self.root.geometry('600x500+300+300')
        self.font = ('仿宋', 18)
        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        tk.Label(self.root, text='用户组', font=self.font).place(x=0, y=10, width=100)
        tk.Label(self.root, text='数量', font=self.font).place(x=100, y=10, width=100)
        tk.Label(self.root, text='用户', font=self.font).place(x=200, y=10, width=50)
        self.canvas = tk.Canvas(self.root, bg='white', scrollregion=(0, 0, 3000, 3000))
        self.canvas.place(x=0, y=50, width=600, height=350)
        self.hbar = tk.Scrollbar(self.canvas, orient=tk.HORIZONTAL)
        self.hbar.pack(side=tk.TOP, fill=tk.X)
        self.hbar.config(command=self.canvas.xview)
        self.vbar = tk.Scrollbar(self.canvas, orient=tk.VERTICAL)
        self.vbar.pack(side=tk.LEFT, fill=tk.Y)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas_frame = tk.Frame(self.canvas, bg='green')
        self.canvas_frame.place(x=100, y=100, anchor='nw')

        self.canvas.create_window(30, 15, window=self.canvas_frame, anchor='nw')

        self.frame = tk.Frame(self.root)
        self.frame.place(x=0, y=400, width=600, height=100)
        self.btn_ok = tk.Button(self.frame, bg='green', text='移动', command=self.btn_ok_event)
        self.group_choice = ttk.Combobox(self.frame, values=list(groups.keys()), state='readonly', )
        self.group_choice.current(list(groups.keys()).index('default'))
        self.btn_new = tk.Button(self.frame, bg='#FFFF00', text='新建', command=self.btn_new_event)

        self.btn_ok.place(x=100, y=30, width=50)
        self.group_choice.place(x=220, y=30)
        self.btn_new.place(x=470, y=30, width=50)

        self.groups = groups
        self.vars = {}
        self.show()

    def show(self):
        self.group_choice.config(values=list(self.groups.keys()))
        self.group_choice.current(list(self.groups.keys()).index('default'))
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        for row, (key, val) in enumerate(self.groups.items()):
            t = tk.Label(self.canvas_frame, bg='#FFFF99', text=f"{key}", font=self.font,
                         width=8)  # .pack(side='left') #.place(x=0, y=50*row)
            t.grid(row=row, column=0)
            tk.Label(self.canvas_frame, text=f"{len(val[0])}", font=self.font, width=8).grid(row=row,
                                                                                             column=1)  # .pack(side='left', anchor='nw') #.place(x=100, y=50*row)
            self.vars[key] = [tk.BooleanVar(self.canvas, value=False) for _ in val[0]]
            for column, user in enumerate(val[0]):
                t = tk.Checkbutton(self.canvas_frame, variable=self.vars[key][column], onvalue=True, offvalue=False,
                                   text=user,
                                   font=self.font)  # .pack(side='left') #.place(x=200+column*100, y=50*row, width=100)
                t.grid(row=row, column=2 + column)
        self.canvas_frame.update()
        temp = [0, 0, 30, 30]
        for i in range(len(temp)):
            temp[i] += self.canvas_frame.bbox('all')[i]
        self.canvas.config(scrollregion=temp)

    def btn_ok_event(self):
        g = self.group_choice.get()
        for key, val in self.vars.items():
            idx = 0
            for var in val:
                if idx == len(val): break
                if var.get():
                    var.set(False)
                    if key == g:
                        idx += 1
                        continue
                    temp = self.groups[key][0][idx]
                    del self.groups[key][0][idx]
                    self.groups[g][0].append(temp)
                else:
                    idx += 1

        messagebox.showinfo(message='移动完毕', parent=self.root)
        self.show()

    def btn_new_event(self):
        group = askstring(title='Add Group', prompt='请输入新用户组', parent=self.root)
        if group == None: return None
        if len(group) > 6:
            messagebox.showerror(message='用户组不能超过6个字符！', parent=self.root)
            return None
        if group in self.groups:
            messagebox.showerror(message='用户组重复！', parent=self.root)
            return None
        # self.groups[group] = [[], tk.Button(self.parent.frame_right_bar, text=group, width=20, height=2), 0]
        self.parent.create_new_group(group)
        self.show()

    def quit(self):
        self.root.quit()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


class AddUserPanel():
    def __init__(self, parent: tk.Tk, groups):
        self.parent = parent
        self.root = tk.Toplevel(parent)
        self.root.title('添加联系人')
        self.root.geometry('360x160+300+300')
        self.font = ('仿宋', 18)
        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.groups = groups
        self.user_accounts = set()
        for key, val in self.groups.items():
            [self.user_accounts.add(x) for x in val[0]]

        self.lb_ent_account = tk.Label(self.root, font=self.font, text='对方账户')
        self.ent_account = tk.Entry(self.root, font=self.font)
        self.lb_ent_account.grid(row=0, column=0)
        self.ent_account.grid(row=0, column=1)

        self.lb_groups = tk.Label(self.root, font=self.font, text='选择群组')
        self.group_choice = ttk.Combobox(self.root, values=list(groups.keys()), state='readonly', )
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
            if u in self.user_accounts: continue
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
            self.user_accounts.add(u)
            self.groups[g][0].append(u)
            messagebox.showinfo(message='添加成功', parent=self.root)

    def quit(self):
        self.root.quit()
        self.root.destroy()




if __name__ == '__main__':
    root = MainPanel('chizuo', None)
    root.run()


