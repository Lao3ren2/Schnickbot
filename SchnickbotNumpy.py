import tkinter as tk
import random as rd
import numpy as np
import math

class MyGUI:
    def __init__(self):
        self.played = []
        self.triples = np.zeros(shape=(3,3,3)) # Leere Matrix mit 3x3x3 Einträgen #habe zeros genommen statt empty, so hab ich exakte 0len darin
        self.answered = []
        self.score= [0,0]
        self.prediction = rd.randint(0,2)
        
        self.root = tk.Tk()
        self.root.geometry("600x600")


        self.scorestring = tk.StringVar()
        self.scorestring.set("0:0")
        self.scoreboard = tk.Label(self.root, textvariable = self.scorestring, font=("Arial",30))
        self.scoreboard.pack()

        self.botstring = tk.StringVar()
        self.botstring.set("")
        self.botplayed = tk.Label(self.root, textvariable = self.botstring, font=("Arial",20))
        self.botplayed.pack()                

        self.scherebutton = tk.Button(self.root, text="Schere", command=self.schereclicked, font=("Arial bold",20))
        self.scherebutton.pack(fill="x",pady=7, padx=7)

        self.steinbutton = tk.Button(self.root, text="Stein",font=("Arial bold",20), command=self.steinclicked)
        self.steinbutton.pack(fill="x",pady=7, padx=7)

        self.papierbutton = tk.Button(self.root, text="Papier", font=("Arial bold",20), command=self.papierclicked)
        self.papierbutton.pack(fill="x",pady=7, padx=7)

        self.entropiestring = tk.StringVar()
        self.entropiestring.set("Entropie:")
        self.entropielabel = tk.Label(self.root, textvariable = self.entropiestring, font=("Arial",10))
        self.entropielabel.pack()

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.mehr = tk.Entry(self.frame, width = 50)
        self.mehr.insert(0,'Hier mehrere Zahlen 0, 1 oder 2 für mehrere Züge (z.B. 02 für Schere, dann Papier)')
        self.mehr.grid(row=0, column = 0)

        self.clearbutton = tk.Button(self.frame, text="Clear", command=self.clearmehr)
        self.clearbutton.grid(row=0,column=1, padx=3)

        self.spielenbutton = tk.Button(self.frame, text="Spielen", command=self.mehrspielen)
        self.spielenbutton.grid(row=0,column=2)
    
        self.root.mainloop()
    def mehrspielen(self):
        s = self.mehr.get()
        for c in s:
            if c=="0":
                self.schereplayed()
            if c=="1":
                self.steinplayed()
            if c=="2":
                self.papierplayed()
        self.updatestats()

    def clearmehr(self):
        self.mehr.delete(0,tk.END)
    
    def newprediction(self):
        if self.prediction == 0:
            self.botstring.set("Computer hat Schere gespielt.")
        elif self.prediction ==1:
            self.botstring.set("Computer hat Stein gespielt.")
        else:
            self.botstring.set("Computer hat Papier gespielt.")
        #----
        if len(self.played)<3:
            self.prediction = rd.randint(0,2)
        else:
            pre1, pre2, pre3 = self.played[-1], self.played[-2], self.played[-3] # letzer, vorletzer, vorvorletzer Zug
            self.triples[pre3, pre2, pre1] += 1 # Triplefreqs werden continuously geupdated
            ertrag = np.diff(self.triples[pre2, pre1, [1, 2, 0, 1]]) # 2. - 1., 0. - 2., 1. - 0.
            gute_züge = np.argwhere(ertrag == np.amax(ertrag)).flatten() # Alle Züge mit maximalen Ertrag, Flatten machts in eine Dimension
            self.prediction = np.random.choice(gute_züge)

    def schereclicked(self):
        self.schereplayed()
        self.updatestats()

    def steinclicked(self):
        self.steinplayed()
        self.updatestats()

    def papierclicked(self):
        self.papierplayed()
        self.updatestats()
    
    def schereplayed(self):
        self.played.append(0)
        self.answered.append(self.prediction)
        if self.prediction == 1:
            self.botwin()
        if self.prediction == 2:
            self.playerwin()
            
        self.newprediction()
        
    def steinplayed(self):
        self.played.append(1)
        self.answered.append(self.prediction)
        if self.prediction == 2:
            self.botwin()
        if self.prediction == 0:
            self.playerwin()
        
        self.newprediction()
        
    def papierplayed(self):
        self.played.append(2)
        self.answered.append(self.prediction)
        if self.prediction == 0:
            self.botwin()
        if self.prediction == 1:
            self.playerwin()
            
        self.newprediction()
        
    def botwin(self):
        self.score[1]+=1
        self.updatescore()
    def playerwin(self):
        self.score[0]+=1
        self.updatescore()
    def updatescore(self):
        self.scorestring.set(str(self.score[0]) + ":" + str(self.score[1]))
    
    def updatestats(self):
        """
        Berechnet die Entropie dritter Ordnung der bisherigen Eingaben. Konvergiert diese nicht gegen 1, so sollte der Computer gewinnen.
        """
        n = len(self.played)
        e3 = 0
        for pr3 in range(3):
            for pr2 in range(3):
                total = np.sum(self.triples[pr3,pr2])
                if total>0:
                    weight = total/n
                    esmall = sum([-math.log(f) / math.log(3) * f for f in self.triples[pr3,pr2]/total if f!=0 ])
                    e3+= weight * esmall
        self.entropiestring.set("Entropie:" + str(e3) +" trits.")
        
MyGUI()     
