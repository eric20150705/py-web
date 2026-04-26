########################輸入模組##########################
from ttkbootstrap import *
import sys
import os
from PIL import Image, ImageTk

########################設定工作目錄########################
os.chdir(sys.path[0])
########################建立視窗########################
window = Tk()
window.title("fun game")
########################讀取圖片########################
image = Image.open("gugugaga.png")
weather_photo = ImageTk.PhotoImage(image)
########################建立標籤########################
weather_label = Label(window, image=weather_photo)
weather_label.pack(padx=20, pady=20)
weather_label.image = weather_photo
########################運行應用程式########################
window.mainloop()
