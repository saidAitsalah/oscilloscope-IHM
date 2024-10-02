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
    if _name_ == "_main_" :
        print("Your python version is : ",major,minor)
        print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog 

from math import pi,sin,radians
from generator import Generator
from screen import Screen

class Controller :
    def __init__(self,model,view): #bg white dans la vue
        self.view=view
        self.model=model
        self.gui()
        self.actions_binding()

    def gui(self) :
        print("Controller.gui()")
        #self.screen=tk.Canvas(view, bg=view.bg,width=view.width,height=view.height)
        name=self.model.get_name()
        self.frame=tk.LabelFrame(self.view.parent,text=name)
        self.var_mag=tk.IntVar()
        self.var_mag.set(self.model.get_magnitude())
        
        self.var_frequency=tk.IntVar()
        self.var_frequency.set(self.model.get_frequence())
        
        self.var_echantillon=tk.IntVar()
        self.var_echantillon.set(self.model.get_samples())
        
        self.var_harmonics=tk.IntVar()
        self.var_harmonics.set(self.model.get_harmonics())
        
        self.var_phase=tk.IntVar()
        self.var_phase.set(self.model.get_phase())
        
        self.scaleA=tk.Scale(self.frame,variable=self.var_mag,
                             label="Amplitude",
                             orient="horizontal",length=250,
                             from_=0,to=5,tickinterval=1)
        self.scaleP=tk.Scale(self.frame,variable=self.var_phase,
                             label="Phase",
                             orient="horizontal",length=250,
                             from_=-90,to=90,tickinterval=20)
        self.scaleF=tk.Scale(self.frame,variable=self.var_frequency,
                             label="Frequency",
                             orient="horizontal",length=250,
                             from_=0,to=50,tickinterval=5)
        self.scaleE=tk.Scale(self.frame,variable=self.var_echantillon,
                             label="Samples",
                             orient="horizontal",length=250,
                             from_=0,to=1500,tickinterval=200)
        self.scaleH=tk.Scale(self.frame,variable=self.var_harmonics,
                             label="Harmonies",
                             orient="horizontal",length=250,
                             from_=0,to=50,tickinterval=5)
        
        self.btn_odd_even = tk.IntVar()
        self.frame_btn_odd_even=tk.Frame(self.frame)
        self.odd = tk.Radiobutton(self.frame_btn_odd_even, text="Odd", variable=self.btn_odd_even, value=2, command=self.harmony_pair_impair)
        self.even = tk.Radiobutton(self.frame_btn_odd_even, text="Even", variable=self.btn_odd_even, value=1,  command=self.harmony_pair_impair)
        self.all = tk.Radiobutton(self.frame_btn_odd_even, text="All", variable=self.btn_odd_even, value=0, command=self.harmony_pair_impair)
        
        self.btn_spot = tk.IntVar()
        self.frame_btn_spot=tk.Frame(self.frame)
        self.spot = tk.Radiobutton(self.frame_btn_spot, text="Spot", variable=self.btn_spot, value=1, command=self.spot_unspot)
        self.unspot = tk.Radiobutton(self.frame_btn_spot, text="Unspot", variable=self.btn_spot, value=0,  command=self.spot_unspot)
        
        
    def actions_binding(self) :
        print("Controller.actions_binding()")
        self.view.screen.bind("<Configure>",self.resize)
        self.scaleA.bind("<B1-Motion>",self.on_magnitude_action)
        self.scaleP.bind("<B1-Motion>",self.on_phase_action)
        self.scaleF.bind("<B1-Motion>",self.on_frequency_action)
        self.scaleH.bind("<B1-Motion>",self.on_harmony_action)
        self.scaleE.bind("<B1-Motion>",self.on_echantillon_action)
    # callbacks (on_<name>_action(...) )
    def on_magnitude_action(self,event):
        print("Controller.on_magnitude_action()")
        if  self.model.m != self.var_mag.get() :
            self.model.m=self.var_mag.get()
            self.model.generate()
            #self.update()
    def on_frequency_action(self,event):
        print("Controller.on_frequency_action()")
        if  self.model.get_frequence() != self.var_frequency.get() :
            self.model.set_frequence(self.var_frequency.get())
            self.model.generate()
    
    def on_phase_action(self,event):
        print("Controller.on_phase_action()")
        if  self.model.get_phase() != self.var_phase.get() :
            self.model.set_phase(self.var_phase.get())
            self.model.generate()

    def on_harmony_action(self,event):
        print("Controller.on_harmony_action()")
        if  self.model.get_harmonics() != self.var_harmonics.get() :
            self.model.set_harmonics(self.var_harmonics.get())
            self.model.generate()
    
    def on_echantillon_action(self,event):
        print("Controller.on_echantillon_action()")
        if  self.model.get_samples() != self.var_echantillon.get() :
            self.model.set_samples(self.var_echantillon.get())
            self.model.generate()
   
    def harmony_pair_impair(self):
        print("Controller.vibration()")
        selected_value = self.btn_odd_even.get()
        self.model.set_pair_impair(selected_value)
        self.model.generate()

    def spot_unspot(self):
        print("Controller.spot_unspot()")
        if  self.btn_spot.get() == 1:
            self.view.spoot=1
            # Call the spot function
            print("Controller.spot()")
            self.view.animate_spot(self.view.get_canvas(),self.model.get_signal(),1)
        else:
            # Call the unspot function
            print("Controller.unspot()")
            self.view.spoot=0
            self.view.unspot()

    def resize(self,event):   #vue
        print("controller.resize()")
        self.view.width,self.view.height=event.width,event.height
        print(self.view.width,self.view.height)
        if self.view.screen.find_withtag("grid"):
            self.view.screen.delete("grid") 
        self.view.create_grid(self.view.units)
        for name,model in self.view.models.items():
            self.view.plot_signal(model,name)
        #self.view.resize(self.view.parent.winfo_width(),self.view.parent.winfo_height())
       
    def layout(self) :        #vue
        print("controller.layout()")
        # self.screen.pack(fill="x")
        # self.screen.pack(fill="both",padx=10,pady=20)
        # self.screen.pack(expand=True,fill="both",padx=10,pady=20)
        self.frame.pack(side="left",fill="both", expand="true")
        self.scaleA.pack(fill="both", expand="true")
        self.scaleP.pack(fill="both", expand="true")
        # self.scaleF.pack(fill="both", expand="true")
        #self.scaleH.pack(fill="both", expand="true")
        self.scaleE.pack(fill="both", expand="true")
        self.frame_btn_odd_even.pack()
        self.odd.pack(side="left")
        self.even.pack(side="left")
        self.all.pack(side="left")
        self.frame_btn_spot.pack()
        self.spot.pack(side="left")
        self.unspot.pack(side="left")

if   __name__ == "__main__" :
    root=tk.Tk()
    
    view=Screen(root)
    view.create_grid(8)
    view.layout()
    
    model=Generator()
    model.attach(view)
    model.set_frequence(20)
    model.generate()
    ctrl= Controller(model, view)
    ctrl.layout()
    
    model1=Generator("Y")
    model1.attach(view)
    model1.generate()
    ctrl= Controller(model1, view)
    ctrl.layout()
    
    root.mainloop()