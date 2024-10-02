# -*- coding: utf-8 -*-
import sys
major=sys.version_info.major
minor=sys.version_info.minor
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
elif major==3 and minor==6 :
    import tkinter as tk
    from tkinter import filedialog
    from PIL import ImageGrab

else :
    import tkinter as tk
    from tkinter import filedialog 
    from PIL import ImageGrab


class Menubar(tk.Frame):
    def __init__(self,parent=None):
        tk.Frame.__init__(self, borderwidth=2)
        if parent :
            self.parent=parent
            menu = tk.Menu(parent)
            parent.config(menu=menu)
            fileMenu = tk.Menu(menu)
            fileMenu.add_command(label="Save",command=self.save)
            fileMenu.add_command(label="Exit", command=self.close_app)
            fileMenu.add_command(label="ScreenSave",command=self.screensave)
            menu.add_cascade(label="File", menu=fileMenu)
 
            fileMenu = tk.Menu(menu)
            fileMenu.add_command(label="About Us ...",command=self.about_us)
            menu.add_cascade(label="Help", menu=fileMenu)
            
    def screensave(self):
        formats=[('Texte','*.py'),('Portable Network Graphics','*.png')]
        filename=filedialog.asksaveasfilename(parent=self,filetypes=formats,title="Save...")
        if len(filename) > 0:
            print("Sauvegarde en cours dans %s" % filename)
            # get the screen coordinates and dimensions
            x = self.parent.winfo_rootx()
            y = self.parent.winfo_rooty()
            width = self.parent.winfo_width()
            height = self.parent.winfo_height()
            # grab the screen content as an image
            image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            # save the image to the file
            image.save(filename)

    def save(self):
        formats=[('Texte','*.py'),('Portable Network Graphics','*.png')]
        filename=filedialog.asksaveasfilename(parent=self,filetypes=formats,title="Save...")
        if len(filename) > 0:
            print("Sauvegarde en cours dans %s" % filename)

    def close_app(self):
        exit()

    def about_us(self):
        print("about_us %s" % "Nom-Prenom")
        
if __name__ == "__main__" :
    mw = tk.Tk()
    app = Menubar(mw)
    mw.wm_title("Tkinter : Menubar")
    mw.mainloop()

