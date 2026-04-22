#######################匯入模組#######################
# 輸入 tkinter 模組
from ttkbootstrap import *
import sys
import os


#######################設定工作目錄########################
os.chdir(sys.path[0])


#######################定義函式########################

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

window.mainloop()
