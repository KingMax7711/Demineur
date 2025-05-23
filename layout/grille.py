# Création et gestion de la grille de jeu
from tkinter import *
import random
import time
from PIL import Image, ImageTk

class Grille:
    def __init__(self, can, longueurX, largeurY, nbCase):
        self.can = can
        self.longueurX = longueurX
        self.largeurY = largeurY
        self.nbCase = nbCase
        self.padding = 5  # Décalage pour éviter que les tracés soient collés aux bords
        self.caseX = (longueurX - 2 * self.padding) / nbCase
        self.caseY = (largeurY - 2 * self.padding) / nbCase
        self.listeMines = []
        self.listeDrapeau = []
        self.listeMinesTrouver = []
        self.visiter = []
        self.img_bombArmed = ImageTk.PhotoImage(Image.open("image/bombArmed.png").resize((int(self.caseX), int(self.caseY))))
        self.img_bombDisarmed = ImageTk.PhotoImage(Image.open("image/bombDisarmed.png").resize((int(self.caseX), int(self.caseY))))
        self.img_flag = ImageTk.PhotoImage(Image.open("image/flag.png").resize((int(self.caseX), int(self.caseY))))

    def initialiserGrille(self):
        self.can.delete("all")
        for i in range(self.nbCase):
            for j in range(self.nbCase):
                x1 = self.padding + i * self.caseX
                y1 = self.padding + j * self.caseY
                x2 = x1 + self.caseX
                y2 = y1 + self.caseY
                self.can.create_rectangle(x1, y1, x2, y2, fill="green", outline="lightgrey", width=2, tags=f"case_{i}_{j}")
                self.can.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f"{i},{j}", tags=f"text_{i}_{j}", fill="") #? DEBUG DES COORDONNES

    def placerMines(self, nbMines, caseInitialX, caseInitialY):
        self.listeMines = []
        voisinsCaseInitial = self.getCaseVoisines(caseInitialX, caseInitialY)
        while len(self.listeMines) < nbMines:
            x = random.randint(0, self.nbCase - 1)
            y = random.randint(0, self.nbCase - 1)
            if (x, y) not in self.listeMines and x!= caseInitialX and y != caseInitialY and (x, y) not in voisinsCaseInitial:
                self.listeMines.append((x, y))

    def tracerMines(self):
        #! Attention, il faut que la grille soit initialisée avant de tracer les mines
        for (x, y) in self.listeMines:
            x1 = self.padding + x * self.caseX
            y1 = self.padding + y * self.caseY
            # Choix de l'image selon si la mine est trouvée ou non
            if (x, y) in self.listeMinesTrouver:
                img = self.img_bombDisarmed
            else:
                img = self.img_bombArmed
            # Affichage de l'image (ancre NW = coin supérieur gauche)
            self.can.create_image(x1, y1, image=img, anchor=NW, tags=f"mine_{x}_{y}")
            self.can.update()  # Met à jour l'affichage du canvas
            time.sleep(0.1)  # Pause pour voir les mines apparaître une par une

    def verifCouleurMine(self, x, y):
        if (x, y) in self.listeMinesTrouver:
            return "green"
        else: 
            return "red"

    def placerRetirerDrapeau(self, x, y):
        # Placer un drapeau sur la case (x, y)
        case = self.getCase(x, y)
        if case:
            if (x, y) not in self.listeDrapeau and len(self.listeDrapeau) < len(self.listeMines):
                # self.can.create_oval(self.can.coords(case), fill="yellow", outline="black", tags=f"drapeau_{x}_{y}")
                # Afficher l'image du drapeau
                self.can.create_image(self.can.coords(case)[0] + self.caseX / 2, self.can.coords(case)[1] + self.caseY / 2, image=self.img_flag, anchor=CENTER, tags=f"drapeau_{x}_{y}")
                self.listeDrapeau.append((x, y))
                # Vérifier si le drapeau est sur une mine
                if (x, y) in self.listeMines:
                    self.listeMinesTrouver.append((x, y))
            else:
                self.can.delete(f"drapeau_{x}_{y}")
                self.listeDrapeau.remove((x, y))
                # Vérifier si le drapeau est sur une mine
                if (x, y) in self.listeMinesTrouver:
                    self.listeMinesTrouver.remove((x, y))
            self.can.update()

    def endGame(self, victoire=False):
        # Suppression des cases
        for i in range(self.nbCase):
            for j in range(self.nbCase):
                case = self.getCase(i, j)
                if case:
                    if self.can.itemcget(case, "fill") != "":
                        # Animation de disparition progressive de la case
                        for alpha in range(10, -1, -1):
                            couleur = f"#00{hex(16*alpha)[2:]:>02}00"  # Du vert vers noir
                            self.can.itemconfig(case, fill=couleur)
                            self.can.update()
                            time.sleep(0.0001)
                        self.can.itemconfig(case, fill="")

                text = self.can.find_withtag(f"nombre_{i}_{j}")
                if text:
                    self.can.itemconfig(text, fill="")

                drapeau = self.can.find_withtag(f"drapeau_{i}_{j}")
                if drapeau:
                    self.can.delete(drapeau)

                self.can.update()  # Met à jour l'affichage du canvas
                time.sleep(0.01)  # Pause pour voir les cases disparaître une par une
        # Affichage des mines
        self.tracerMines()

    def getNombreMinesVoisines(self, x, y):
        # Compter le nombre de mines voisines autour de la case (x, y)
        mineVoisines = 0
        for case in self.getCaseVoisines(x, y):
            if case in self.listeMines:
                mineVoisines += 1
        return mineVoisines
    
    def propagation(self, x, y):
        if (x, y) in self.visiter:
            return
        else:
            self.visiter.append((x,y))

        # Propagation des cases vides
        if self.getNombreMinesVoisines(x, y) == 0:
            case = self.getCase(x, y)
            self.can.itemconfig(case, fill="")
            self.can.update()
            time.sleep(0.01)  # Pause pour voir les cases disparaître une par une
            for voisin in self.getCaseVoisines(x, y):
                self.propagation(voisin[0], voisin[1])
        else:
            # Afficher le nombre de mines voisines
            minesVoisines = self.getNombreMinesVoisines(x, y)
            case = self.getCase(x, y)
            if case and not case in self.listeMines:
                self.can.itemconfig(case, fill="")
                self.can.create_text(self.can.coords(case)[0] + self.caseX / 2, self.can.coords(case)[1] + self.caseY / 2, text=str(minesVoisines), tags=f"nombre_{x}_{y}", fill="black")
    
    def getCaseVoisines(self, x, y):
        listeVoisines = []
        if x - 1 >= 0:
            listeVoisines.append((x - 1, y))
        if x + 1 < self.nbCase:
            listeVoisines.append((x + 1, y))
        if y - 1 >= 0:
            listeVoisines.append((x, y - 1))
        if y + 1 < self.nbCase:
            listeVoisines.append((x, y + 1))
        if x - 1 >= 0 and y - 1 >= 0:
            listeVoisines.append((x - 1, y - 1))
        if x + 1 < self.nbCase and y + 1 < self.nbCase:
            listeVoisines.append((x + 1, y + 1))
        if x - 1 >= 0 and y + 1 < self.nbCase:
            listeVoisines.append((x - 1, y + 1))
        if x + 1 < self.nbCase and y - 1 >= 0:
            listeVoisines.append((x + 1, y - 1))
        return listeVoisines
    
    def verifVictoire(self):
        return len(self.visiter) + len(self.listeMines) == self.nbCase * self.nbCase

    def verifVictoireDrapeau(self):
        return len(self.listeMinesTrouver) == len(self.listeMines)
            

    def getCanvas(self):
        return self.can
    
    def getCase(self, x, y):
        # Obtenir la case à la position (x, y)
        return self.can.find_withtag(f"case_{x}_{y}")
    
    def nbCase(self):
        return self.nbCase
        
