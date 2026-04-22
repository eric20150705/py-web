#######################匯入模組#######################
# 輸入 tkinter 模組
from ttkbootstrap import *
import sys
import os


#######################定義函式########################
def text():
    print("text")


#######################建立視窗########################
# 建立主視窗
window = Tk()
# 設定視窗標題
window.title("fun game")
#######################設定字形########################
font_size = 20
window.option_add("*Font", ("新細明體", font_size))
#######################設定主題########################
style = Style(theme="vapor")
style.configure("my.TButton", font=("新細明體", font_size))
#######################建立標籤########################
label = Label(window, text="歡迎來到我的遊戲！")
label.grid(row=0, column=0, sticky="E")
#######################建立按鈕########################
button = Button(window, text="開始遊戲", command=text, style="my.TButton")
button.grid(row=0, column=1, sticky="W")
button2 = Button(window, text="顯示", command=text, style="my.TButton")
button2.grid(row=1, column=0, columnspan=2, sticky="EW")

window.mainloop()
