#######################匯入模組#######################
# 輸入 tkinter 模組
from ttkbootstrap import *
import sys
import os

from tkinter import filedialog

from PIL import Image, ImageTk

#######################設定工作目錄########################
os.chdir(sys.path[0])


#######################定義函式########################
def open_file():
    global file_path
    file_path = filedialog.askopenfilename(initialdir=sys.path[0])
    label2.config(text=file_path)  # 顯示檔名


def show_img():
    global file_path
    image = Image.open(file_path)
    image = image.resize((canva.winfo_width(), canva.winfo_height()), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    canva.create_image(0, 0, anchor="nw", image=photo)
    canva.image = photo


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
label = Label(window, text="選擇圖片:")
label.grid(row=0, column=0, sticky="E")

label2 = Label(window, text="none")
label2.grid(row=0, column=1, sticky="NSEW")
#######################建立按鈕########################
button = Button(window, text="打開圖片", command=open_file, style="my.TButton")
button.grid(row=0, column=2, sticky="W")
button2 = Button(window, text="顯示", command=show_img, style="my.TButton")
button2.grid(row=1, column=0, columnspan=3, sticky="EW")
#######################建立放圖片的地方########################
canva = Canvas(window, width=600, height=600)
canva.grid(row=2, column=0, columnspan=3)
window.mainloop()
