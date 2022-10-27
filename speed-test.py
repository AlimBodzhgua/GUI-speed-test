from wonderwords import RandomWord
import tkinter as tk
from tkinter import ttk

import threading

class SpeedTestGUI:
    window = tk.Tk()
    window.title("Speed test application")
    window.geometry("640x450")
    window.resizable(False, False)

    text_font = ("Roboto", 18)
    entry_font = ("Roboto", 15)
    speed_font = ("Roboto", 14, 'italic')
    button_font = ("Roboto", 13)

    def __init__(self):
        self.rw = RandomWord()

        self.main = tk.Frame(SpeedTestGUI.window)

        self.text = tk.Label(self.main,
            text=[word for word in self.rw.random_words(10)],
            wraplength=465,
            font=SpeedTestGUI.text_font)
        self.text.grid(row=0, column=0, columnspan=2, padx=5)

        self.text_entry = tk.Entry(self.main, width=50, font=SpeedTestGUI.speed_font)
        self.text_entry.grid(row=1, column=0, columnspan=2, pady=10, padx=5)
        self.text_entry.bind('<KeyRelease>', self.start)

        self.char_info = tk.Label(self.main, text="CPM: 0.00\nCPS: 0.00",
        font=SpeedTestGUI.speed_font)
        self.char_info.grid(row=2, column=0, padx=5)

        self.word_info = tk.Label(self.main, text="WPM: 0.00\nWPS: 0.00", font=SpeedTestGUI.speed_font)
        self.word_info.grid(row=2, column=1, padx=5)

        self.reset_button = tk.Button(self.main, text="reset", command=self.reset, font=SpeedTestGUI.button_font)
        self.reset_button.grid(row=3, column=0, columnspan=2,pady=5, padx=5)

        self.change_button = tk.Button(self.main, text="change words number", font=SpeedTestGUI.button_font, command=self.change_quantity)
        self.change_button.grid(row=4, column=0, columnspan=2, pady=5, padx=5)

        self.running = False
        self.count = 0
        
        self.main.pack(expand=True)
        SpeedTestGUI.window.mainloop()


    def start(self, key):
        if not self.running:
            if not key.keycode in [16, 17, 18]:
                self.running = True
                threading.Thread(target=self.start_thread_count).start()
        if not self.text.cget('text').startswith(self.text_entry.get()):
            self.text_entry.config(fg='red')
        else:
            self.text_entry.config(fg='black')

        if self.text_entry.get() == self.text.cget('text'):
            self.running = False
            self.text_entry.config(fg='green', state=tk.DISABLED)


    def change_quantity(self):
        self.combo = ttk.Combobox(self.main, 
        values=([i for i in range(1,31)]), font=SpeedTestGUI.entry_font, width=20)
        self.combo.grid(row=5, column=0, columnspan=2)

        self.submit_button = tk.Button(self.main, text="submit", command=self.change_words_number, font=SpeedTestGUI.button_font)
        self.submit_button.grid(row=6, column=0, columnspan=2)


    def change_words_number(self):
        self.text.config(text=[word for word in self.rw.random_words(int(self.combo.get()))])
        self.combo.destroy()
        self.submit_button.destroy()


    def start_thread_count(self):
        while self.running:
            self.count += 0.1
            cps = len(self.text_entry.get()) / self.count
            cpm = cps * 60
            wps = len(self.text_entry.get().split(' ')) / self.count
            wpm = wps * 60
            self.char_info.config(
                text=f"CPM: {cpm:.2f}\nCPS: {cps:.2f}")
            self.word_info.config(
                text=f"WPM: {wpm:.2f}\nWPS: {wps:.2f}")


    def reset(self):
        self.running = False
        self.count = 0
        self.char_info.config(text="CPM: 0.00\nCPS: 0.00")
        self.word_info.config(text="WPM: 0.00\nWPS: 0.00")
        self.text.config(text=[word for word in self.rw.random_words(10)])
        self.text_entry.config(state=tk.NORMAL)
        self.text_entry.delete(0, tk.END)


def main():
    SpeedTestGUI()

if __name__ == "__main__":
    main()
