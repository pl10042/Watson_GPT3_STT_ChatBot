from tkinter import *
import pyttsx3
from Chat_Bot_Example import ask, append_interaction_to_chat_log
from transcribe import *
import time
import os

BG_GRAY = "#4E4E4E"
BG_COLOR = "#4E4E4E"
TEXT_COLOR = "#FFFFFF"

FONT = "Helvetica 11"
FONT_BOLD = "Helvetica 10 bold"



class ChatApplication:
    def __init__(self):
        self.window = Tk()  # top level
        self._setup_main_window()  # layout
        # self.transProg = os.system('python transcribe.py')
        self.chat_log = None
        self.msg1 = None
        self.msg2 = None
        self.my_entry = Entry(self.window, font=("Helvetica", 28))

    def run(self):
        self.window.mainloop()

    def run_2(self):
        os.system('python transcribe.py')
    def _setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=True, height=True)
        self.window.configure(width=470, height=550, bg=BG_COLOR)  # attributes

        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=.012)

        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=.745, relwidth=1, rely=.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(
            command=self.text_widget.yview)  # when scroll bar changed, y position changes to scroll up and down

        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # message entry box
        self.msg_entry = Entry(bottom_label, bg="#566CAC", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
        self.msg_entry.insert(0, "Default")

        # # send button
        # send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
        #                      command=lambda: [self._on_enter_pressed(None)])
        # send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

        # send button 2
        # self.send_button_2 = Button(bottom_label, text="Speak", font=FONT_BOLD, width=10, bg=BG_GRAY,
        #                      command=lambda: [self._after_enter_pressed_me(None), self._after_enter_pressed(None)])
        # self.send_button_2.place(relx=0.5, rely=0.008, relheight=0.06, relwidth=0.22)
        self.send_button_2 = Button(bottom_label, text="Speak", font=FONT_BOLD, width=10, bg=BG_GRAY,
                              command=lambda: [self.run_2(), self._on_enter_pressed(None), self._after_enter_pressed(None)])
        self.send_button_2.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)


    def _insert_message(self, msg):
        if not msg:
            return
        self.msg_entry.delete(0, END)
        # self.msg1 = f"{'Human'}: {msg}\n\n"
        file = open("sample.txt")
        line = file.read().replace("\n", " ")
        file.close()
        self.msg_entry.insert(0, line)
        self.msg1 = f"{'Human'}: {line}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, self.msg1)
        self.text_widget.configure(state=DISABLED)

        # self.msg2 = f"{'AI'}: {ask(self.msg1, self.chat_log)}\n\n"
        self.msg2 = f"{'AI'}: {ask(self.msg1, self.chat_log)}\n\n"
        self.msg2.replace('Human: ', '')
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, self.msg2)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg)
        # self._after_enter_pressed_me(self.msg1)
        # self._after_enter_pressed(self.msg2)
        if msg is not None:
            self.chat_log = append_interaction_to_chat_log(self.msg1, self.msg2, self.chat_log)
            if 'Human: ' in self.msg1 and 'AI: ' in self.msg2:
                self.msg1.replace('Human: ', '')
                self.msg2.replace('AI: ', '')
            if 'Human: ' in self.msg2:
                self.msg2.replace('Human: ', '')

    # def _invoke_(self):
    #     self.send_button_2.invoke()

    # AI Response Voice
    def _after_enter_pressed(self, event):
        msg = self.msg2
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[75].id)
        engine.setProperty('rate', 173)
        engine.setProperty('volume',0.5)
        new_msg = msg.replace('AI:', '')
        engine.say(new_msg)
        engine.runAndWait()


    # User voice
    def _after_enter_pressed_me(self, event):
        msg = self.msg1
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[2].id)
        engine.setProperty('rate', 173)
        engine.setProperty('volume',0.5)
        engine.say(msg)
        engine.runAndWait()



if __name__ == "__main__":
    app = ChatApplication()
    # app.run_2()
    app.run()
