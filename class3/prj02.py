#######################匯入模組#######################
# 輸入 tkinter 模組
from tkinter import *
from PIL import Image, ImageTk

import sys
import os

#######################設定工作目錄########################
# 找到現在的資料夾位置
os.chdir(sys.path[0])
#######################建立視窗########################
# 建立主視窗
window = Tk()
# 設定視窗標題
window.title("2D遊戲")
#######################創建畫布########################
canva = Canvas(window, width=600, height=600, bg="white")
canva.pack()
#######################設定視窗圖片########################

#######################載入圖片########################
image = Image.open("比中指.png")
img = ImageTk.PhotoImage(image)
#######################顯示圖片########################
my_img = canva.create_image(300, 300, image=img)
#######################運行應用程式########################
# 開始執行主迴圈，等待用戶操作
window.mainloop()
