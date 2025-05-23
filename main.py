from tkinter import *
from tkinter import ttk

import random
import time

from layout.grille import Grille
from data.gestionUser import get_user, set_user, hash_password, get_highscore, add_score_to_history, update_highscore

def param():
    # Create the main window
    root = Tk()
    root.title("Paramètres")

    frm = ttk.Frame(root, padding=10)
    frm.grid()

    connected = False

    # Function to validate the input and start the main function
    def onValidate(xEntry, yEntry, nbMinesEntry, caseEntry, userEntry):
        # Initialiser les variables avec des valeurs par défaut
        nonlocal connected
        longueurX = 0
        largeurY = 0
        nbMines = 0
        nbCase = 0
        user = ""
        nbErreur = 0

        try:
            # Récupérer et valider la longueur
            longueurX = int(xEntry.get())
            if longueurX <= 0:
                raise ValueError("La longueur doit être supérieure à zéro.")
            xLabel.config(foreground="green")
        except ValueError:
            longueurX = 0
            errorLabel.config(text="La longueur doit être un entier supérieur à zéro.")
            xLabel.config(foreground="red")
            nbErreur += 1

        try:
            # Récupérer et valider la largeur
            largeurY = int(yEntry.get())
            if largeurY <= 0:
                raise ValueError("La largeur doit être supérieure à zéro.")
            yLabel.config(foreground="green")
        except ValueError:
            largeurY = 0
            errorLabel.config(text="La largeur doit être un entier supérieur à zéro.")
            yLabel.config(foreground="red")
            nbErreur += 1

        try:
            # Récupérer et valider le nombre de mines
            nbMines = int(nbMinesEntry.get())
            if nbMines <= 0:
                raise ValueError("Le nombre de mines doit être supérieur à zéro.")
            nbMinesLabel.config(foreground="green")
        except ValueError:
            nbMines = 0
            errorLabel.config(text="Le nombre de mines doit être un entier supérieur à zéro.")
            nbMinesLabel.config(foreground="red")
            nbErreur += 1

        try:
            # Récupérer et valider le nombre de cases
            nbCase = int(caseEntry.get())
            if nbCase <= 0:
                raise ValueError("Le nombre de cases doit être supérieur à zéro.")
            caseEntryLabel.config(foreground="green")
        except ValueError:
            nbCase = 0
            errorLabel.config(text="Le nombre de cases doit être un entier supérieur à zéro.")
            caseEntryLabel.config(foreground="red")
            nbErreur += 1

        # Récupérer le nom d'utilisateur
        user = userEntry.get()

        if nbErreur == 1:
            return
        elif nbErreur > 1:
            errorLabel.config(text="Plusieurs erreurs détectées, veuillez vérifier vos entrées.")
            return

        # Si tout est valide, effacer les messages d'erreur
        xLabel.config(foreground="green")
        xEntry.config(state="disabled")
        yLabel.config(foreground="green")
        yEntry.config(state="disabled")
        nbMinesLabel.config(foreground="green")
        nbMinesEntry.config(state="disabled")
        caseEntryLabel.config(foreground="green")
        caseEntry.config(state="disabled")
        if userEntry.get() == "Anonyme" or userEntry.get() == "":
            userLabel.config(foreground="orange")
        else:
            userLabel.config(foreground="green")
        errorLabel.config(text="")

        # Passer à la fonction principale
        def proceedToGame():
            nonlocal connected
            nonlocal longueurX
            nonlocal largeurY
            nonlocal nbMines
            nonlocal nbCase
            nonlocal user
            # Créer une barre de chargement
            loading_label = ttk.Label(frm, text="Chargement...")
            loading_label.grid(column=0, row=7, columnspan=4)
            progress = ttk.Progressbar(frm, orient=HORIZONTAL, length=200, mode='determinate')
            progress.grid(column=0, row=8, columnspan=4)

            # Simuler une progression de chargement
            for i in range(101):
                root.update_idletasks()
                progress['value'] = i
                root.after(40)

            # Fermer la fenêtre des paramètres et appeler la fonction principale avec les paramètres
            root.unbind("<Return>")
            root.unbind("<Escape>")
            root.destroy()
            main(longueurX, largeurY, nbMines, nbCase, user, connected)

        # Vérifier si l'utilisateur existe déjà
        user = userEntry.get()
        if user == "Anonyme" or user == "" or connected:
            userEntry.config(state="disabled")
            proceedToGame()
        else:
            existing_user = get_user(user)
            if existing_user is None:
                # Si l'utilisateur n'existe pas, le créer
                root2 = Tk()
                root2.title("Création de compte")
                frm2 = ttk.Frame(root2, padding=10)
                frm2.grid()
                ttk.Label(frm2, text="Entrez un mot de passe:").grid(column=0, row=0)
                passwordEntry = ttk.Entry(frm2, show="*", justify=CENTER)
                passwordEntry.grid(column=0, row=1)
                errorLabel2 = ttk.Label(frm2, text="", foreground="red")
                errorLabel2.grid(column=0, row=2)
                def onValidatePassword():
                    nonlocal connected
                    password = passwordEntry.get()
                    if password == "":
                        errorLabel2.config(text="Le mot de passe ne peut pas être vide.")
                        return
                    # Créer l'utilisateur dans la base de données
                    set_user(user, password)
                    root2.unbind("<Return>")
                    root2.unbind("<Escape>")
                    root2.destroy()
                    onValidate(xEntry, yEntry, nbMinesEntry, caseEntry, userEntry)
                root2.bind("<Return>", lambda event: onValidatePassword())
                # Bind the Escape key to close the window
                root2.bind("<Escape>", lambda event: root2.destroy())
                # Create a label to display instructions
                ttk.Label(frm2, text="Appuyez sur Entrée pour valider ou Échap pour quitter", font=("TkDefaultFont", 10, "italic")).grid(column=0, row=3)
                passwordEntry.focus_force()  # Set focus to the password entry field
                root2.mainloop()
            else:
                # Si l'utilisateur existe déjà, vérifier le mot de passe
                root2 = Tk()
                root2.title("Connexion")
                frm2 = ttk.Frame(root2, padding=10)
                frm2.grid()
                ttk.Label(frm2, text="Entrez votre mot de passe:").grid(column=0, row=0)
                passwordEntry = ttk.Entry(frm2, show="*", justify=CENTER)
                passwordEntry.grid(column=0, row=1)
                errorLabel2 = ttk.Label(frm2, text="", foreground="red")
                errorLabel2.grid(column=0, row=2)
                def onValidatePassword():
                    nonlocal connected
                    password = passwordEntry.get()
                    if password == "":
                        errorLabel2.config(text="Le mot de passe ne peut pas être vide.")
                        return
                    if existing_user["password"] != hash_password(password):
                        errorLabel2.config(text="Mot de passe incorrect.")
                        passwordEntry.focus_force()
                        passwordEntry.delete(0, END)
                        return
                    # Si le mot de passe est correct, se connecter
                    connected = True
                    userEntry.config(state="disabled")
                    root2.unbind("<Return>")
                    root2.unbind("<Escape>")
                    root2.destroy()
                    proceedToGame()
                root2.bind("<Return>", lambda event: onValidatePassword())
                # Bind the Escape key to close the window
                root2.bind("<Escape>", lambda event: root2.destroy())
                # Create a label to display instructions
                ttk.Label(frm2, text="Appuyez sur Entrée pour valider ou Échap pour quitter", font=("TkDefaultFont", 10, "italic")).grid(column=0, row=3)
                passwordEntry.focus_force()  # Set focus to the password entry field
                root2.mainloop()

    # Création des labels et champs d'entrée
    xLabel = ttk.Label(frm, text="Longueur")
    xLabel.grid(column=0, row=0)
    yLabel = ttk.Label(frm, text="Largeur")
    yLabel.grid(column=1, row=0)
    nbMinesLabel = ttk.Label(frm, text="Nombre de mines")
    nbMinesLabel.grid(column=2, row=0)
    caseEntryLabel = ttk.Label(frm, text="Nombre de cases")
    caseEntryLabel.grid(column=3, row=0)
    errorLabel = ttk.Label(frm, text="", foreground="red")
    errorLabel.grid(column=0, row=6, columnspan=4)
    userLabel = ttk.Label(frm, text="Entrez un nom d'utilisateur")
    userLabel.grid(column=0, row=3, columnspan=4)

    # Champs d'entrée
    xEntry = ttk.Entry(frm, name="xEntry", justify=CENTER)
    xEntry.grid(column=0, row=1)
    yEntry = ttk.Entry(frm, name="yEntry", justify=CENTER)
    yEntry.grid(column=1, row=1)
    nbMinesEntry = ttk.Entry(frm, name="nbMinesEntry", justify=CENTER)
    nbMinesEntry.grid(column=2, row=1)
    caseEntry = ttk.Entry(frm, name="caseEntry", justify=CENTER)
    caseEntry.grid(column=3, row=1)
    userEntry = ttk.Entry(frm, name="userEntry", justify=CENTER)
    userEntry.grid(column=0, row=4, columnspan=4)

    # Valeurs par défaut
    xEntry.insert(0, "600")
    yEntry.insert(0, "600")
    nbMinesEntry.insert(0, "40")
    caseEntry.insert(0, "15")
    userEntry.insert(0, "Anonyme")

    root.bind("<Return>", lambda event: onValidate(xEntry, yEntry, nbMinesEntry, caseEntry, userEntry))
    root.bind("<Escape>", lambda event: root.destroy())
    ttk.Label(frm, text="Appuyez sur Entrée pour valider ou Échap pour quitter", font=("TkDefaultFont", 10, "italic")).grid(column=0, row=5, columnspan=4)

    root.mainloop()

def main(longueurX, largeurY, nbMines, nbCase, user, connected):
    print("Longueur:", longueurX)
    print("Largeur:", largeurY)
    print("Nombre de mines:", nbMines)
    print("Nombre de cases:", nbCase)
    print("Utilisateur:", user)
    print("Connecté:", connected)

    # Création de l'app
    root = Tk()
    root.title("Démineur")

    # Créer la frame principale
    frm = ttk.Frame(root, padding=10)
    frm.grid()

    # Créer le canevas
    can = Canvas(frm, width=longueurX, height=largeurY, bg="#f0f0f0")
    can.grid(column=0, row=0, columnspan=4)

    # Créer la grille
    grille = Grille(can, longueurX, largeurY, nbCase)
    grille.initialiserGrille()

    # Label
    drapeauLabel = ttk.Label(frm, text=f"Drapeau restant : {nbMines}")
    drapeauLabel.grid(column=0, row=1, columnspan=2)
    nbClickLabel = ttk.Label(frm, text=f"Nombre de clics: {0}")
    nbClickLabel.grid(column=2, row=1, columnspan=2)
    infoLabel = ttk.Label(frm, text="Clic gauche pour découvrir une case, clic droit pour placer un drapeau, Espace pour finir la partie")
    infoLabel.grid(column=0, row=2, columnspan=4)
    userLabel = ttk.Label(frm, text="")
    userLabel.grid(column=0, row=3, columnspan=4)
    finLabel = ttk.Label(frm, text="", foreground="red")
    finLabel.grid(column=0, row=4, columnspan=4)

    # Afficher le nom d'utilisateur
    if connected:
        userLabel.config(text=f"Connecté en tant que {user}, Highscore: {get_highscore(user)}", foreground="blue")
    else:
        userLabel.config(text="Connecté en tant qu'invité", foreground="orange")
    root.title(f"Démineur ({user})")

    # Variable Globale
    NBCLICK = 0
    STARTTIME = time.time()

    def onClick(event):
        # nonlocal
        nonlocal NBCLICK

        if NBCLICK == 0:
            # Obtenir les coordonnées de la case cliquée
            x = int((event.x - grille.padding) // grille.caseX)
            y = int((event.y - grille.padding) // grille.caseY)

            grille.placerMines(nbMines, x, y)
            grille.propagation(x, y)
            NBCLICK += 1

        else:
            NBCLICK += 1

            # Obtenir les coordonnées de la case cliquée
            x = int((event.x - grille.padding) // grille.caseX)
            y = int((event.y - grille.padding) // grille.caseY)
            

            if (x, y) in grille.listeMines:
                # Si c'est une mine, afficher un message
                can.unbind("<Button-1>")
                can.unbind("<Button-3>")
                root.unbind("<space>")
                grille.endGame(False)
                infoLabel.config(text="Partie terminée, appuyez sur R pour recommencer ou Échap pour quitter", foreground="purple")
                print("Défaite")
            else:
                grille.propagation(x, y)

        # Mettre à jour le label du nombre de clics
        nbClickLabel.config(text=f"Nombre de clics: {NBCLICK}")
                

    def onClick2(event):
        # nonlocal
        nonlocal NBCLICK

        if NBCLICK == 0:
            return
        # Obtenir les coordonnées de la case cliquée
        x = int((event.x - grille.padding) // grille.caseX)
        y = int((event.y - grille.padding) // grille.caseY)

        grille.placerRetirerDrapeau(x, y)
        drapeauLabel.config(text=f"Drapeau restant : {nbMines - len(grille.listeDrapeau)}")


    def debug():
        if user != "admin":
            return
        grille.listeMinesTrouver = []
        infoLabel.config(text="Debug: toutes les mines sont révélées", foreground="red")
        root.title(f"Démineur - DEV MODE ({user})")
        for i in range(len(grille.listeMines)):
            x, y = grille.listeMines[i]
            grille.listeMinesTrouver.append((x, y))

    def restartGame():
        root.destroy()
        main(longueurX, largeurY, nbMines, nbCase, user, connected)

    def endByUser():
        # nonlocal
        nonlocal NBCLICK
        nonlocal STARTTIME

        if NBCLICK == 0:
            return
        
        endTime = time.time()
        elapsedTime = round(endTime - STARTTIME, 2)

        can.unbind("<Button-1>")
        can.unbind("<Button-3>")
        root.unbind("<space>")
        victoire = grille.verifVictoireDrapeau()
        competitive = longueurX == 600 and largeurY == 600 and nbCase == 15 and nbMines == 40

        if victoire and connected and competitive:
            highscoreUser = get_highscore(user)
            if highscoreUser is None or NBCLICK < highscoreUser:
                # Mettre à jour le highscore
                add_score_to_history(user, NBCLICK, elapsedTime, competitive)
                update_highscore(user, NBCLICK)
                userLabel.config(text="Nouveau Highscore !", foreground="blue")
            else:
                # Ajouter le score à l'historique
                add_score_to_history(user, NBCLICK, elapsedTime, competitive)
                userLabel.config(text="Pas de nouveau Highscore", foreground="orange")

        elif victoire and connected and not competitive:
            userLabel.config(text="Victoire !, attention les highscore ne sont pas enregistré si vous changez les paramètres", foreground="green")
            add_score_to_history(user, NBCLICK, elapsedTime, competitive)

        finLabel.config(text="Victoire" if victoire else "Défaite", foreground="green" if victoire else "red")
        infoLabel.config(text="Partie terminée, appuyez sur R pour recommencer ou Échap pour quitter", foreground="purple")
        grille.endGame(victoire)

    

    # Bind les événements
    can.bind("<Button-1>", onClick)
    can.bind("<Button-3>", onClick2) 
    root.bind("<Escape>", lambda event: root.destroy())
    root.bind("<space>", lambda event: endByUser())
    root.bind("<r>", lambda event: restartGame())
    root.bind("<e>", lambda event: debug())

    root.mainloop()

print("Ceci est le projet de Maxime Czegledi, TG1(2024-2025)")
param()