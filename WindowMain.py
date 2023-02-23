import tkinter as tk
import json

from CounterController import Counter
from WindowSetting import Setting

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("KYNCounter2")
        self.geometry("260x115")

        self.counter = Counter()
        self.create_widgets()
        self.update_text()

    def create_widgets(self):
        # ラベルの作成
        self.label = tk.Label(self, text="", font=14)

        self.win_button = tk.Button(self, text="Win", command=self.win)
        self.lose_button = tk.Button(self, text="Lose", command=self.lose)
        self.back_button = tk.Button(self, text="Back", command=self.back)        
        self.clear_button = tk.Button(self, text="Clear", command=self.clear)
        
        self.setting_button = tk.Button(self, text="設定", command=self.setting)
        
        # ウィジェットの配置
        self.label.grid(row=0, column=0, columnspan=4, pady=10)
        
        self.win_button.grid(row=1, column=0)
        self.lose_button.grid(row=1, column=1)
        self.back_button.grid(row=1, column=2)
        self.clear_button.grid(row=1, column=3)
        
        self.setting_button.grid(row=2, columnspan=4, pady=10)
        
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.columnconfigure(3,weight=1)


    def win(self):
        self.counter.win()
        self.update_text()

    def lose(self):
        self.counter.lose()
        self.update_text()

    def clear(self):
        self.counter.clear()
        self.update_text()

    def back(self):
        self.counter.rollback()
        self.update_text()

    def update_text(self):
        self.label.config(text=f"現在:{self.counter.count_win}勝 {self.counter.count_lose}敗 {self.counter.count_streak}連勝中")
        self.counter.update_count()
    
    def setting(self):
        setting = Setting()
        setting.mainloop()



if __name__ == '__main__':
    app = App()
    app.mainloop()
