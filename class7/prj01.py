#######################匯入模組#######################
# 輸入 tkinter 模組
from ttkbootstrap import *
import sys
import os

#######################設定工作目錄########################
os.chdir(sys.path[0])


#######################定義函式########################
def on_switch_change():
    check_label.config(text=str(check_type.get()))


#######################建立視窗########################
# 建立主視窗
window = Tk()
# 設定視窗標題
window.title("fun game")

#######################設定字形########################
font_size = 20
window.option_add("*Font", ("Helvetica", font_size))

#######################設定主題########################
style = Style(theme="vapor")
style.configure("my.TButton", font=("Helvetica", font_size))
style.configure("my.TCheckbutton", font=("Helvetica", font_size))

#######################建立變數########################
# 建立布林變數
check_type = BooleanVar()
# 預設為勾選狀態
check_type.set(True)
#######################建立標籤########################
# 建立標籤，顯示目前Checkbutton對應的布林值
check_label = Label(window, text="True")
# 將標籤放到視窗中指定位置
check_label.grid(row=1, column=2, padx=10, pady=10)
#######################建立Checkbutton########################
check = Checkbutton(
    window,
    variable=check_type,
    onvalue=True,
    offvalue=False,
    command=on_switch_change,
    style="my.TCheckbutton",
)
check.grid(row=1, column=1, padx=10, pady=10)
#######################運行應用程式########################
window.mainloop()
