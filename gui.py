import PySimpleGUI as sg
from queue import Queue
from client import TCPClient


class ClinetGUI():
    def __init__(self):
        sg.theme('DarkAmber')
        self.font = ('Helvetica', 18)
        self.username = None
        self.window = None
        self.output = print
        self.messages = Queue()
        self.client = TCPClient(self.messages)

    def create_login_layout(self, font):
        layout = [
            [sg.Text('Enter your Nickname below', font=font)],
            [sg.Text('Nickname', font=font), sg.InputText(font=font, text_color='white', size=(20, 1))],
            [sg.Text('Password', font=font), sg.InputText(font=font, text_color='white', size=(20, 1))],
            [sg.Button('Ok', font=font), sg.Button('Register', font=font), sg.Button('Cancel', font=font)],
        ]
        return layout

    def create_chat_layout(self, font):
        layout = [
            [sg.Text(f'Hello, {self.username}', font=font, text_color='white')],
            [sg.Output(size=(40, 20), font=font, text_color='white', key='OUTPUT')],
            [sg.Input(font=font, size=(34, 1), do_not_clear=False), sg.FileBrowse(font=font)],
            [sg.OK(font=font), sg.Cancel(font=font)],
        ]
        return layout

    def create_register_layout(self, font):
        layout = [
            [sg.Text('Enter your Nickname below', font=font)],
            [sg.Text('Nickname', font=font), sg.InputText(font=font, text_color='white', size=(20, 1))],
            [sg.Text('Password', font=font), sg.InputText(font=font, text_color='white', size=(20, 1))],
            [sg.Text('Repeat', font=font), sg.InputText(font=font, text_color='white', size=(20, 1))],
            [sg.Button('Ok', font=font), sg.Button('Cancel', font=font)],
        ]
        return layout

    def run_register(self):
        window_register = sg.Window("Register", self.create_register_layout(self.font))
        res = False
        while True:
            event, values = window_register.read()
            if event == sg.WIN_CLOSED or event == 'Cancel': break
            if event == 'Ok' and len(values[0]) > 0 and len(values[1]) > 0 and values[1] == values[2]:
                res = self.client.register(values[0], values[1])
                if res: break
                else: sg.popup_error("Register failed!", font=self.font)
            else:
                sg.popup_error("Password and Repeat must equal!", font=self.font)
        if res: sg.popup_ok("Register success!", font=self.font)
        window_register.close()


    def run_login(self):
        window1 = sg.Window("Login", self.create_login_layout(self.font))
        res = False
        while True:
            event, values = window1.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            if event == 'Ok' and len(values[0]) and len(values[1]) > 0:
                res = self.client.login(values[0], values[1])
                if res:
                    self.username = values[0]
                    break
                else: sg.popup_error("登录失败，检查密码或网络环境", font=self.font)
            elif event == 'Register':
                self.run_register()
            else:
                sg.popup_error("Input username and password!", font=self.font)
        window1.close()
        return res

    def run_chat(self):
        window2 = sg.Window("Chat", self.create_chat_layout(self.font))
        self.window = window2
        self.client.run()
        while True:
            event, values = window2.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif len(values[0]) > 0:
                self.messages.put(('2', values[0]))
        self.client.stop_signal = True
        window2.close()

    def run(self):
        res = self.run_login()
        if res:
            self.run_chat()



if __name__ == "__main__":
    clientgui = ClinetGUI()
    clientgui.run()



