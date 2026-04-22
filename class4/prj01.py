#######################匯入模組#######################
# 輸入 tkinter 模組
from tkinter import *
import sys
import os

#######################設定工作目錄########################
# 找到現在的資料夾位置
os.chdir(sys.path[0])


#######################定義函式########################
def move_circle(event):
    key = event.keysym
    print(key)
    if key == "Right":
        canva.move(circle, 10, 0)
    elif key == "Left":
        canva.move(circle, -10, 0)
    elif key == "Up":
        canva.move(circle, 0, -10)
    elif key == "Down":
        canva.move(circle, 0, 10)
    if key == "d":
        canva.move(rect, 10, 0)
    elif key == "a":
        canva.move(rect, -10, 0)
    elif key == "w":
        canva.move(rect, 0, -10)
    elif key == "s":
        canva.move(rect, 0, 10)


def hi_quit():
    window.destroy()


#######################建立視窗########################
# 建立主視窗
window = Tk()
# 設定視窗標題
window.title("2D遊戲")
#######################建立按鈕########################
quit_btn = Button(window, text="離開", command=hi_quit)
quit_btn.pack()
#######################創建畫布########################
canva = Canvas(window, width=600, height=600, bg="white")
canva.pack()
#######################設定視窗圖片########################

#######################載入圖片########################

img = PhotoImage(file="比中指.png")
#######################顯示圖片########################
my_img = canva.create_image(300, 300, image=img)
#######################畫圖形##########################
circle = canva.create_oval(250, 150, 300, 200, fill="green")

rect = canva.create_rectangle(220, 400, 340, 430, fill="blue")

msg = canva.create_text(300, 100, text="########", fill="black", font=("Arial", 30))
#######################綁定按鍵事件########################
canva.bind_all("<Key>", move_circle)
#######################運行應用程式########################
# 開始執行主迴圈，等待用戶操作
window.mainloop()
