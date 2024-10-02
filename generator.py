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
from observer import Subject

class Generator(Subject) :
    def __init__(self,name="X",magnitude=1,frequence=2,phase=0,harmonics=1,samples=100):
        Subject.__init__(self)
        self.name=name
        self.signal=[]
        self.m,self.f,self.p=1.0,2.0,0.0
        self.harmonics=harmonics
        self.samples=samples
        self.type=0

    # properties getter/setter
    def get_name(self) :
        return self.name
    def set_name(self,name) :
        self.name=name
    def get_signal(self) :
        return self.signal
    def set_signal(self,signal) :
        self.signal=signal
    def get_magnitude(self) :
        return self.m
    def set_magnitude(self,magnitude) :
        self.m=magnitude
    def get_frequence(self) :
        return self.f
    def set_frequence(self,frequence) :
        self.f=frequence
    def get_phase(self) :
        return self.p
    def set_phase(self,phase) :
        self.p=phase
    def get_samples(self) :
        return self.samples
    def set_samples(self,samples) :
        self.samples=samples
    def get_harmonics(self) :
        return self.harmonics
    def set_harmonics(self,harmonics) :
        self.harmonics=harmonics
    def get_pair_impair(self) :
        return self.type
    def set_pair_impair(self,type) :
        self.type=type
                            
    def vibration(self,t):
        # Warning : take care of degrees_to_radians conversion on phase (self.p)
        # if you get degree from your slider, use radians() function from math module to convert
        m,f,p=self.m,self.f,self.p
        harmo=int(self.harmonics)
        sum=0
        for h in range(1,harmo+1) :
            if (self.type == 0) :
                # all
                sum=sum + (m/h)*sin(2*pi*(f*h)*t-p)
            elif (self.type == 1 and h%2 == 0) :
                # even
                sum=sum + (m/h)*sin(2*pi*(f*h)*t-p)
            elif (self.type == 2 and h%2 != 0) :
                # odd
                sum=sum + (m/h)*sin(2*pi*(f*h)*t-p)
        return sum
    def generate(self):
        print("Generator.generate()")
        del self.signal[0:]
        samples=int(self.samples)
        for t in range(samples+1) :
            self.signal.append([t/samples,self.vibration(t/samples)])
        self.notify()
        return self.signal

if   __name__ == "__main__" :
    generator=Generator()
    print(generator.generate())

