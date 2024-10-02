# coding: utf-8
import sys
import math
major=sys.version_info.major
minor=sys.version_info.minor
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
elif major==3 :
    import tkinter as tk
    from tkinter import filedialog
else :
    if __name__ == "__main__" :
        print("Your python version is : ",major,minor)
        print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog 

from math import pi,sin,radians
from generator import Generator
from observer import Observer


class Screen(Observer) :
    def __init__(self,parent,bg="white",width=600,height=300):
        self.parent=parent
        self.bg=bg
        self.width,self.height=width,height
        self.x,self.y,self.radius=0,0,10
        self.units=1
        self.models={}
        self.spoot=0
        self.gui()
        
    # properties getter/setter
    
    def gui(self) :
        print("Screen.gui()")
        self.screen=tk.Canvas(self.parent, bg=self.bg,width=self.width,height=self.height)
        self.spot=self.screen.create_oval(
            self.x-self.radius,self.y-self.radius,
            self.x+self.radius,self.y+self.radius,
            fill='yellow',outline='black',tags="spot")
        self.width_canva=int(self.screen.cget("width"))
        self.height_canva=int(self.screen.cget("height"))
    
    def get_canvas(self) :
        return self.screen
    
    def update(self,subject):
        name = subject.get_name()
        print("Screen.update()",name)
        signal = subject.get_signal()
        if name not in self.models.keys() :
            self.models[name]=signal
        if signal :
            self.plot_signal(signal,name)

    def plot_signal(self,signal=[],name="X",color="red"):
        print("Generator.plot_signal()")
        if signal and len(signal)>1:
            w,h=self.width,self.height
            if self.screen.find_withtag(name) :
                self.screen.delete(name)         
            plots=[(x*w,(h/self.units)*y+h/2) for (x,y) in signal]
            self.screen.create_line(plots,fill=color,smooth=1,width=3,tags=name)
        return
    
    # def plot_signals(self,signals):
    #     for name,signal in signals:
    #         if name not in self.models.keys() :
    #             self.models[name]=signal
    #         if signal :
    #             self.plot_signal(signal,name)
    #     return
    
    def create_grid(self,tiles=2):
        print("Screen.create_grid()")
        if self.screen.find_withtag("grid") :
            self.screen.delete("grid")         
        self.units=tiles
        tile_x=self.width/tiles
        for t in range(1,tiles+1):
            x =t*tile_x
            self.screen.create_line(x,0,x,self.height,tags="grid")
            self.screen.create_line(x,self.height/2-10, x,self.height/2+10,width=3,tags="grid")
        tile_y=self.height/tiles
        for t in range(1,tiles+1):
            y =t*tile_y
            self.screen.create_line(0,y,self.width,y,tags="grid")
            self.screen.create_line(self.width/2-10,y,self.width/2+10,y, width=3,tags="grid")
    def resize(self,width,height):
        print("Screen.resize()")
        self.width,self.height=width,height
        print("width,height",self.width,self.height)
        #self.create_grid(self.units)
        # for name,signal in self.models.items() :
        #     print(name)
        #     self.plot_signal(name,signal)
        # TO DO  :
        # delete existing grid
        # create grid with new dimension
        # plot signal with new dimension
    def layout(self) :
        print("Screen.layout()")
        #self.screen.pack()
        # self.screen.pack(fill="x")
        # self.screen.pack(fill="both",padx=10,pady=20)
        self.screen.pack(expand=True,fill="both",padx=10,pady=20)
        #self.frame.pack()
        #self.scaleA.pack()

    def animate_spot(self,canvas,signal,i=0):
        print("Controller.sssssssssssssspot()")
        #width,height=int(canvas.cget("width")),int(canvas.cget("height"))
        
        if(self.spoot):
            width,height=self.width,self.height
            #width,height=self.width,self.height
            #width,height=self.get_canvas().winfo_width(),self.get_canvas().winfo_height()
            msec=100
            if i==len(signal) :
                i=0
            x,y=signal[i][0]*width, height/self.units*(signal[i][1])+height/2
            canvas.coords(self.spot,x,y,x+self.radius,y+self.radius)
            after_id=self.parent.after(msec, self.animate_spot,canvas,signal,i+1)
            return after_id
    
    def unspot(self):
        self.screen.delete("spot")
        self.spot=self.screen.create_oval(
        self.x-self.radius,self.y-self.radius,
        self.x+self.radius,self.y+self.radius,
        fill='yellow',outline='black',tags="spot")
        pass
    

if   __name__ == "__main__" :
    root=tk.Tk()
    view=Screen(root)
    model=Generator()
    model.attach(view)
    model.generate()
    view.create_grid(8)
    view.layout()
    #view.update(model)
    root.mainloop()

