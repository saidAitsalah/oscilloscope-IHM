from generator import Generator
from screen import Screen
from controller import Controller
from PIL import ImageGrab

import sys
major=sys.version_info.major
minor=sys.version_info.minor
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
    from tkinter import messagebox
elif major==3 :
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import messagebox
else :
    if _name_ == "_main_" :
        print("Your python version is : ",major,minor)
        print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog 


#Barre des Menus
class Menubar(tk.Frame):
    def __init__(self,canva,parent=None):
        tk.Frame.__init__(self,parent=None,borderwidth=2)
        self.parent=parent
        self.canva = canva
        menu=tk.Menu(parent) 
        parent.config(menu=menu)
        fileMenu = tk.Menu(menu)
        fileMenu.add_command(label="Save",command=self.save)
        fileMenu.add_command(label="Exit", command=self.close)
        fileMenu.add_command(label="Open", command=self.open)
        fileMenu.add_command(label="ScreenSave",command=self.screensave)
        menu.add_cascade(label="File", menu=fileMenu)
        helpMenu = tk.Menu(menu)
        helpMenu.add_command(label="About Us ...",command=self.about_us)
        helpMenu.add_command(label="About TK ...",command=self.about_tkinter)
        helpMenu.add_command(label="About Python ...",command=self.about_python)
        menu.add_cascade(label="Help", menu=helpMenu)
        
    def screensave(self):
        formats=[('Texte','*.py'),('Portable Network Graphics','*.png')]
        filename=filedialog.asksaveasfilename(parent=self,filetypes=formats,title="Save...")
        if len(filename) > 0:
            print("Sauvegarde en cours dans %s" % filename)
            # get the screen coordinates and dimensions
            x = self.canva.winfo_rootx()
            y = self.canva.winfo_rooty()
            width = self.canva.winfo_width()
            height = self.canva.winfo_height()
            # grab the screen content as an image
            image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            # save the image to the file
            image.save(filename)

    #Fonction sauvegarde en fichier JSON
    def save(self):
        print("Menubar.save()")
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".json")
        if filename is None:  
            return
        jsonlist=[]
        data={}
        data['nom']=model.get_name()
        data['echantillons']=model.get_samples()
        data['amplitude']=model.get_magnitude()
        data['frequence']=model.get_frequence()
        data['phase']=model.get_phase()
        data['harmoniques']=model.get_harmonics()
        jsonlist.append(data)
        json.dump(jsonlist, filename)
        return
    
    #Action d'ouvrir le fichier sauvegardé
    def open(self):
        filename = filedialog.askopenfile(mode='r', defaultextension=".json")
        if filename is None:
            return
        signal = json.load(filename)
        print(signal)
        ctr = 0
        model.set_samples(signal[ctr]['echantillons'])
        model.set_magnitude(signal[ctr]['amplitude'])
        model.set_frequence(signal[ctr]['frequence'])
        model.set_phase(signal[ctr]['phase'])
        model.set_harmonics(signal[ctr]['harmoniques'])
        model.generate()
        ctr += 1
        filename.close()
        return
    
    #Action de fermer l'application (avec message de confirmation)
    def close(self):
        confirmation = tk.messagebox.askyesno("Confirmation", "Vous êtes sur le point de quitter ce programme, êtes-vous sûr?")
        if confirmation:
            exit()

    #Info sur le créateur    
    def about_us(self):
        print("Menubar.about_us()")
        tk.messagebox.showinfo("About Us", " Etudiant Ait Salah Said \n Etudiant EL Makhroubi Ali \n 2023")

    #Info sur la version de Tkinter
    def about_tkinter(self):
        print("Menubar.about_tkinter()")
        tk.messagebox.showinfo("About Tkinter", "Tkinter version : 8.6")

    #Info sur la version de Python
    def about_python(self):
        print("Menubar.about_python()")
        tk.messagebox.showinfo("About Python", "Python version : 3.11.2")


if   __name__ == "__main__" :
    root=tk.Tk()
    
    view=Screen(root)
    view.create_grid(8)
    view.layout()
    
    model=Generator()
    model.attach(view)
    model.generate()
    ctrl= Controller(model, view)
    ctrl.layout()
    
    model1=Generator("Y")
    model1.attach(view)
    model1.generate()
    
    ctrl= Controller(model1, view)
    ctrl.layout()
    
    app = Menubar(view.screen,root)
    
    #view.animate_spot(view.get_canvas(),model1.get_signal())
        
    root.mainloop()