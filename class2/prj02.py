#######################匯入模組#######################
# 輸入 tkinter 模組
from tkinter import *
import random


#######################定義函數########################
def butten():
    fg_colors = "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
    """
    比對展開寫法
    fg_colors = "#"
    for j in range(6):
        fg_colors += random.choice("0123456789ABCDEF")
    """

    bg_colors = "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
    display.config(text="hi", fg=fg_colors, bg=bg_colors)


#######################建立視窗########################
# 建立主視窗
window = Tk()
# 設定視窗標題
window.title("2D遊戲")

window.options_add("*Font", ("微軟正黑體 100"))
############################建立按鈕########################
# 建立按鈕，當按鈕被按下時，會呼叫 butten 函數
btn1 = Button(window, text="按我", command=butten)
# 將按鈕加入視窗中
btn1.pack()
#########################建立標籤########################
# 建立標籤，顯示歡迎訊息，文字顏色為紅色，背景顏色為黑色
# Label參數說明：(視窗名稱,文字內容,前景顏色,背景顏色)
display = Label(window, text="歡迎來到2D遊戲", fg="red", bg="black")

# 將標籤加入視窗中
display.pack()
#######################運行應用程式########################
# 開始執行主迴圈，等待用戶操作
window.mainloop()
