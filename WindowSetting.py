import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from CounterController import Counter

class Setting(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Setting")
        self.geometry("300x150")
        
        self.counter = Counter()
        self.create_widgets()

    def create_widgets(self):
        # ラベルの作成
        self.label = tk.Label(self, text="載せる文章のテンプレートを変更してください\n$w : 勝利数, $l : 敗北数, $s : 連勝数に変換されます")

        self.textbox = tk.Text(self, height=5, width=40)
        self.textbox.insert(1.0, self.counter.get_text_template())
        
        self.apply_button = tk.Button(self, text="OK", command=self.apply)
        self.cancel_button = tk.Button(self, text="Cancel", command=self.cancel)
        
        # ウィジェットの配置
        self.label.grid(row=0, column=0, columnspan=2, pady=5)
        
        self.textbox.grid(row=1, columnspan=2)
        
        self.apply_button.grid(row=2, column=0, pady=5)
        self.cancel_button.grid(row=2, column=1, pady=5)  
        
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        
    def apply(self):
        # テキストボックスの最初の文字から最後まで(ただし改行は除く)取得
        self.counter.set_text_template(self.textbox.get("1.0","en-1c"))
        self.counter.get_text()
        self.counter.update_count()
        self.destroy()
    
    def cancel(self):
        # 保存せず終了
        self.destroy()


if __name__== '__main__':
    setting = Setting()
    setting.mainloop()
