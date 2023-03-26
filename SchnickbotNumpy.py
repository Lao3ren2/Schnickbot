import tkinter as tk
import random as rd
import numpy as np
import math

class MyGUI:
    def __init__(self):
        self.played = []
        self.triples = np.empty(shape=(3,3,3)) # Leere Matrix mit 3x3x3 Einträgen
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

        self.scherebutton = tk.Button(self.root, text="Schere", command=self.schereplayed, font=("Arial bold",20))
        self.scherebutton.pack(fill="x",pady=7, padx=7)

        self.steinbutton = tk.Button(self.root, text="Stein",font=("Arial bold",20), command=self.steinplayed)
        self.steinbutton.pack(fill="x",pady=7, padx=7)

        self.papierbutton = tk.Button(self.root, text="Papier", font=("Arial bold",20), command=self.papierplayed)
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

        self.clearbutton = tk.Button(self.frame, text="Spielen", command=self.mehrspielen)
        self.clearbutton.grid(row=0,column=2)
    
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
            #ertrag = [situation[2]-situation[1], situation[0]-situation[2] ,situation[1]-situation[0]]
            gute_züge = np.argwhere(ertrag == np.amax(ertrag)).flatten() # Alle Züge mit maximalen Ertrag, Flatten machts in eine Dimension
            #gute_züge= [i for i in [0,1,2] if ertrag[i] == max(ertrag)]
            self.prediction = np.random.choice(gute_züge)
            
    
    def schereplayed(self):
        self.played.append(0)
        self.answered.append(self.prediction)
        if self.prediction == 1:
            self.botwin()
        if self.prediction == 2:
            self.playerwin()
            
        self.newprediction()
        self.updateentropie()
        
    def steinplayed(self):
        self.played.append(1)
        self.answered.append(self.prediction)
        if self.prediction == 2:
            self.botwin()
        if self.prediction == 0:
            self.playerwin()
        
        self.newprediction()
        self.updateentropie()
        
    def papierplayed(self):
        self.played.append(2)
        self.answered.append(self.prediction)
        if self.prediction == 0:
            self.botwin()
        if self.prediction == 1:
            self.playerwin()
            
        self.newprediction()
        self.updateentropie()
        
    def botwin(self):
        self.score[1]+=1
        self.updatescore()
    def playerwin(self):
        self.score[0]+=1
        self.updatescore()
    def updatescore(self):
        self.scorestring.set(str(self.score[0]) + ":" + str(self.score[1]))
    def updateentropie(self):
        n = len(self.played)
        freq = [ len([x for x in self.played if x==i])/n for i in [0,1,2]]
        e1 = sum([-math.log(f) / math.log(3) * f for f in freq if f!=0])

        if n==1:
            self.entropiestring.set("Entropie:" + str(e1) )
        else:
            pairs = list(zip(self.played,self.played[1:]))
            freqs = [[0 for i in range(3)] for j in range(3)]
            for (fst,snd) in pairs:
                freqs[fst][snd]+=1
            e2 = 0
            for i in [0,1,2]:
                if sum(freqs[i])>0:
                    z = sum(freqs[i])
                    k= sum([-math.log(f/z) / math.log(3) * f/z for f in freqs[i] if f!=0])
                    e2+= k * z/(n-1)
            self.entropiestring.set("Entropie:" + str(e1) +"\nEntropie2:" + str(e2))
MyGUI()     
