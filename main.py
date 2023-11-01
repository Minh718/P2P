import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import socket
import json
import funcClient
from tkinter import messagebox
from tkinter import filedialog, StringVar, OptionMenu
def show_home_page():
    flogin.pack_forget()
    fregister.pack_forget()
    window.geometry("700x700")
        # Hiển thị khung được chỉ định
    # leftpagehome.grid(row=0, column=0, padx=10)
    # leftpagehome.pack()
    # rightpagehome.grid(row=0, column=1,padx=10)
    leftpagehome.pack(side="left",padx=10, anchor="n")
    rightpagehome.pack(side="right", padx=10, anchor="n")
    rightListUsers.pack_forget()
    rightListFiles.pack()
def show_frame(frame):
    # Ẩn tất cả các khung
    flogin.pack_forget()
    fregister.pack_forget()
    leftpagehome.pack_forget()
    rightpagehome.pack_forget()
    # Hiển thị khung được chỉ định
    frame.pack()

def switch_to_flogin():
    show_frame(flogin)
def deleteFilePublish(file): return

def switch_to_fregister():
    show_frame(fregister)
def register():
    username = fregister_username_entry.get()
    password = fregister_password_entry.get()
    repassword = fregister_repassword_entry.get()
    
    if password == repassword:
        message = funcClient.sendRegister(username, password)
        if(message == "success"):
            show_frame(flogin)
        else:
            fregister_error_username.config(text="Tên đăng nhập đã được sử dụng")
            
    fregister_username_entry.delete(0, tk.END)
    fregister_password_entry.delete(0, tk.END)
    fregister_repassword_entry.delete(0, tk.END)
def login():
    username = flogin_username_entry.get()
    password = flogin_password_entry.get()
    message = funcClient.sendLogin(username, password)
    # if(message == "success"):
    if type(message) is tuple:
        global files
        username = message[0]
        rightpagehome_username_label.config(text=username)
        files = message[1]
        listAvalFiles = ", ".join(message[2])
        rightpagehome_files_server.config(text=f"Các files có thể fetch bao gồm: {listAvalFiles}" ,  anchor='w', pady=10, wraplength=280)
        
        for file in files:
            tk.Label(leftpagehomeL, text=file[1], pady=5).pack()
            tk.Label(leftpagehomeM, text=file[0],  wraplength=230, padx=10, pady=5).pack()
            tk.Button(leftpagehomeR, text="Xóa", command=lambda fl=file: deleteFilePublish(file)).pack(pady=5)
        show_home_page()
    # else:
        # fregister_error_username.config(text="Tên đăng nhập đã được sử dụng")     
    # window.geometry("500x500")
    flogin_username_entry.delete(0, tk.END)
    flogin_password_entry.delete(0, tk.END)

def select_directory():
    global directory_path 
    directory_path = filedialog.askdirectory()
    if directory_path:
        leftpagehome_address_label.config(text=f"Vị trí file tại: {directory_path}", wraplength=380, justify="left")
def select_directory_save():
    global directory_path_save 
    directory_path_save = filedialog.askdirectory()
    if directory_path_save:
        rightpagehome_address_save_label.config(text=f"Vị trí lưu file tại: {directory_path_save}", wraplength=280, justify="left")
     
def publishFile ():
    global directory_path
    namefile = leftpagehome_namefile_entry.get()
    message = funcClient.sendPublishFile(directory_path,namefile)
    if type(message) == str:
        print("errror")
    else:
        tk.Label(leftpagehomeL, text=namefile, pady=5).pack()
        tk.Label(leftpagehomeM, text=directory_path,  wraplength=380, padx=10, pady=5).pack()
        tk.Button(leftpagehomeR, text="Xóa", command=lambda x=directory_path, y = namefile: deleteFilePublish((x, y))).pack(pady=5)
        directory_path=""
    
    
    leftpagehome_address_label.config(text=f"Vị trí file tại: {directory_path}", wraplength=380, justify="left")    
    leftpagehome_namefile_entry.delete(0, tk.END)
    return
def get_users_file ():
    global optionList
    namefile = rightpagehome_namefile_save_entry.get()
    users = funcClient.sendGetUsersFile(namefile)
    # print(users)
    rightpagehome_users_have_file.config( text=f"Danh sách người dùng hiện online và có file {namefile}")
    menuUsers['menu'].delete(0, 'end')
    # users = ["Minh", "Đồng", "KA"]
    for user in users:
        menuUsers['menu'].add_command(label=user,command=tk._setit(optionList, user))
    # # OptionMenu(rightListUsers, optionList, *(users)).pack(side="left")
    # # menuUsers.update(rightListUsers, optionList, *(users))
    optionList.set("Chọn người lấy file")
    rightListFiles.pack_forget()
    rightListUsers.pack()
    rightpagehome_namefile_save_entry.delete(0, tk.END)
    return
def logOut(): 
    funcClient.sendLogOut()
    switch_to_flogin()
    window.geometry("400x350")

def on_closing():
    funcClient.closeApp()
    window.destroy()
# def OptionMenu_ChooseUser(event):
#     messagebox.showinfo("Option Menu", "You have selected the option: " + str(optionList.get()))
def fetchFile():
    funcClient.sendFetchFile(str(optionList.get()),directory_path_save, percent_download)
    
directory_path_save="./"
directory_path=""
files=[]
window = tk.Tk()
window.title("Đăng ký và Đăng nhập")
window.geometry("400x350")
flogin = tk.Frame(window)
fregister = tk.Frame(window)
leftpagehome = tk.Frame(window, width=400)
leftpagehomeL = tk.Frame(leftpagehome, width=50)
leftpagehomeM = tk.Frame(leftpagehome, width=300)
leftpagehomeR = tk.Frame(leftpagehome, width=50)
rightpagehome = tk.Frame(window, width=350)
rightListUsers = tk.Frame(rightpagehome)
rightListFiles = tk.Frame(rightpagehome)
listboxPublishFile = tk.Listbox(leftpagehome)
# leftpagehome.grid(row=0, column=0)
# leftpagehome.grid(row=0, column=1)

font_style = tkFont.Font(family="Helvetica", size=16, weight="bold", slant="italic")
font_style_title = tkFont.Font(family="Helvetica", size=14, weight="bold", slant="italic")
font_style1 = tkFont.Font( size=16,  slant="italic")

flogin_username_label = tk.Label(flogin, text="File sharing with P2P",font=font_style, pady=15)
flogin_username_label.pack()
flogin_username_label = tk.Label(flogin, text="Tên đăng nhập:" )
flogin_username_label.pack()

flogin_username_entry = tk.Entry(flogin,font=15 )
flogin_username_entry.pack(pady=5)

flogin_password_label = tk.Label(flogin, text="Mật khẩu:")
flogin_password_label.pack()
flogin_password_entry = tk.Entry(flogin, show="*", font=15 )  # Sử dụng dấu '*' để ẩn mật khẩu
flogin_password_entry.pack(pady=5)
flogin_login_button = tk.Button(flogin, text="Đăng nhập", command=login, cursor="hand2", pady=10, padx=20)
flogin_login_button.pack(pady=10)
flogin_register_button = tk.Button(flogin, text="Đi tới đăng ký", command=switch_to_fregister, borderwidth=0,  cursor="hand2")
flogin_register_button.pack()

fregister_username_label = tk.Label(fregister, text="File sharing with P2P",font=font_style, pady=15)
fregister_username_label.pack()
fregister_username_label = tk.Label(fregister, text="Tên đăng nhập:" )
fregister_username_label.pack()
fregister_username_entry = tk.Entry(fregister,font=15 )
fregister_username_entry.pack(pady=5)
fregister_error_username = tk.Label(fregister, text="", fg="red")
fregister_error_username .pack()
fregister_password_label = tk.Label(fregister, text="Mật khẩu:")
fregister_password_label.pack()
fregister_password_entry = tk.Entry(fregister, show="*", font=15 )  # Sử dụng dấu '*' để ẩn mật khẩu
fregister_password_entry.pack(pady=5)
fregister_repassword_label = tk.Label(fregister, text="Nhập lại mật khẩu:")
fregister_repassword_label.pack()
fregister_repassword_entry = tk.Entry(fregister, show="*", font=15 )  # Sử dụng dấu '*' để ẩn mật khẩu
fregister_repassword_entry.pack(pady=5)
fregister_login_button = tk.Button(fregister, text="Đăng ký", command=register, cursor="hand2", pady=10, padx=20)
fregister_login_button.pack(pady=10)
fregister_register_button = tk.Button(fregister, text="Đi tới đăng nhập", command=switch_to_flogin, borderwidth=0,  cursor="hand2")
fregister_register_button.pack()

leftpagehome_username_label = tk.Label(leftpagehome, text="File sharing with P2P",font=font_style, pady=15, padx=10)
leftpagehome_username_label.pack()



logout = tk.Frame(rightpagehome)
rightpagehome_button_logout= tk.Button(logout, text="logout", command=logOut, cursor='hand2')
rightpagehome_button_logout.pack(side="right")
rightpagehome_username_label = tk.Label(logout, text="Minhpro", pady=15, padx=10, font=font_style)
rightpagehome_username_label.pack(side="right")
logout.pack()

leftpagehome_username_label = tk.Label(leftpagehome,font=font_style_title ,text="Tải tên file có thể chia sẽ lên server", anchor='w', pady=10)
leftpagehome_username_label.pack(fill='both')

leftpagehome_select_button = tk.Button(leftpagehome, text="Chọn vị trí file", command=select_directory, anchor='w')
leftpagehome_select_button.pack()
leftpagehome_address_label = tk.Label(leftpagehome, text=f"Vị trí file tại:  {directory_path}", anchor="w")
leftpagehome_address_label.pack(fill="both")
leftpagehome_namefile_label = tk.Label(leftpagehome, text="Tên file:")
leftpagehome_namefile_label.pack()
leftpagehome_namefile_entry = tk.Entry(leftpagehome,font=20 )  # Sử dụng dấu '*' để ẩn mật khẩu
leftpagehome_namefile_entry.pack()
leftpagehome_publish_button = tk.Button(leftpagehome, text="publish", padx=10, pady=10, command=publishFile,  cursor="hand2")
leftpagehome_publish_button.pack(pady=10, padx=20)

leftpagehome_username_label = tk.Label(leftpagehome, text="Các files đã publish lên server",font=font_style_title, anchor='w', pady=10)
leftpagehome_username_label.pack(fill='both')
tk.Label(leftpagehomeL, text="Tên file:").pack()
tk.Label(leftpagehomeM, text="Địa chỉ:").pack()
tk.Label(leftpagehomeR, text="Action:").pack()
leftpagehomeL.pack(side="left")
leftpagehomeM.pack(side="left")
leftpagehomeR.pack(side="left")
# leftpagehomeM.grid(row=0, column=1)
# leftpagehomeR.grid(row=0, column=2)

tk.Label(rightpagehome, text="fetch file", font=font_style_title , anchor='w', pady=10).pack(fill='both')
rightpagehome_select_save_button = tk.Button(rightpagehome, text="Chọn vị trí lưu file", command=select_directory_save, anchor='w')
rightpagehome_select_save_button.pack()
rightpagehome_address_save_label = tk.Label(rightpagehome, text=f"Vị trí lưu file tại:  {directory_path_save}", anchor="w")
rightpagehome_address_save_label.pack(fill="both")
rightpagehome_namefile_save_label = tk.Label(rightpagehome, text="Tên file:")
rightpagehome_namefile_save_label.pack()
rightpagehome_namefile_save_entry = tk.Entry(rightpagehome, font=20 )  # Sử dụng dấu '*' để ẩn mật khẩu
rightpagehome_namefile_save_entry.pack()
rightpagehome_fetch_button = tk.Button(rightpagehome, text="fetch", command=get_users_file,  cursor="hand2", padx=10, pady=10)
rightpagehome_fetch_button.pack(pady=10)

rightpagehome_files_server = tk.Label(rightListFiles, text="Các files có thể fetch bao gồm:", anchor='w', pady=10)
rightpagehome_files_server.pack(fill='both')
rightpagehome_users_have_file =  tk.Label(rightListUsers, text="Danh sách người dùng hiện online và có file", font=font_style_title, wraplength=320, anchor='w', pady=10)
rightpagehome_users_have_file.pack(fill='both')
users = ["Name"]
optionList = StringVar()
optionList.set("Chọn người lấy file")
menuUsers = ttk.OptionMenu(rightListUsers, optionList, *users)
menuUsers.pack()
tk.Button(rightListUsers, text="Lấy file", padx=10,pady=10, command=fetchFile,  cursor="hand2").pack( padx=5)
# tk.Label(rightListUsers, text="",anchor='w', pady=10).pack()
percent_download = tk.Label(rightListUsers, text="", pady=10)
percent_download.pack()
tk.Button(rightListUsers, text="Tải lại trang", padx=10, command=show_home_page,  cursor="hand2").pack( padx=5, pady=20)

 # presets the first option
# options = ["Option A", "Option B", "Option C", "Option D"]
# OptionMenu(rightListUsers, optionList, *(options), command=OptionMenu_ChooseUser).pack()
# leftpagehome_publish_button = tk.Button(leftpagehome, text="publish", padx=10, pady=10, command=publishFile,  cursor="hand2")
# leftpagehome_publish_button.pack(pady=10, padx=20)




window.protocol("WM_DELETE_WINDOW", on_closing)

show_frame(flogin)
window.mainloop()
