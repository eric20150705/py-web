#######################匯入模組#######################
# 輸入 tkinter 模組
from tkinter import *


#######################定義函數########################
def butten():
    # 顯示hi在終端機上
    print("hi")
    display.config(text="歡迎來到2D遊戲", fg="red", bg="black")


def clear():
    # 清除標籤內容，將文字顏色和背景顏色設為白色
    display.config(text="", fg="white", bg="white")


#######################建立視窗########################
# 建立主視窗
window = Tk()
# 設定視窗標題
window.title("2D遊戲")

############################建立按鈕########################
# 建立按鈕，當按鈕被按下時，會呼叫 butten 函數
btn1 = Button(window, text="show", command=butten)
# 將按鈕加入視窗中
btn1.pack()
# 建立按鈕，當按鈕被按下時，會呼叫 butten 函數
btn2 = Button(window, text="clean", command=clear)
# 將按鈕加入視窗中
btn2.pack()
#########################建立標籤########################
# 建立標籤，顯示歡迎訊息，文字顏色為紅色，背景顏色為黑色
# Label參數說明：(視窗名稱,文字內容,前景顏色,背景顏色)
display = Label(window, text="")

# 將標籤加入視窗中
display.pack()
#######################運行應用程式########################
# 開始執行主迴圈，等待用戶操作
window.mainloop()
