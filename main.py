
import sys, sqlite3

from utils import db
from utils import display
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
from actions.action_tablesData import AppTablesData
from actions.action_fct_fournie_1 import AppFctFournie1
from actions.action_fct_fournie_2 import AppFctFournie2
from actions.action_fct_comp_1 import AppFctComp1
from actions.action_fct_comp_2 import AppFctComp2
from actions.action_fct_comp_3 import AppFctComp3
from actions.action_fct_comp_4 import AppFctComp4
from actions.action_age_or_equipe import AppOrEquipe
from actions.action_classement_pays import AppClassementPays
from actions.action_inscription_epreuve import AppInscriptionEpreuve
from actions.action_update_resultats_equipes import AppUpdateResultatsEquipes
from actions.action_inscription_sportif import AppInscriptionSportif
from actions.action_gestion_equipe import AppGestionEquipe


# Classe utilisée pour lancer la fenêtre principale de l'application et définir ses actions
class AppWindow(QMainWindow):

    # Création d'un signal destiné à être émis lorsque la table est modifiée
    changedValue = pyqtSignal()

    # TODO 2 : ajouter les fenetres (répertoire gui) et les actions (répertoire actions) correspondant aux 2 items de la partie 2.
    # TODO 3 : ajouter les fenetres (rep. gui) et les actions (rep. actions) correspondant aux 2 items de la partie 3.

    # On prévoit des variables pour accueillir les fenêtres supplémentaires
    tablesDataDialog = None
    fct_fournie_1_dialog = None
    fct_fournie_2_dialog = None
    fct_comp_1_dialog = None
    fct_comp_2_dialog = None
    fct_comp_3_dialog = None
    fct_comp_4_dialog = None
    age_or_equipe_dialog = None
    classement_pays_dialog = None
    Update_Resultats_Equipes_dialog = None
    insciption_epreuve_dialog = None
    insciption_sportif_dialog = None
    gestion_equipe_dialog = None

    # Constructeur
    def __init__(self):

        # On appelle le constructeur de la classe dont on hérite
        super(AppWindow, self).__init__()

        # On charge le gui de la fenêtre
        self.ui = uic.loadUi("gui/mainWindow.ui", self)

        # On se connecte à la base de données
        self.data = sqlite3.connect("data/jo.db")

    ####################################################################################################################
    # Définition des actions
    ####################################################################################################################

    # Action en cas de clic sur le bouton de création de base de données
    def createDB(self):

        try:
            # On exécute les requêtes du fichier de création
            db.updateDBfile(self.data, "data/createDB.sql")

        except Exception as e:
            # En cas d'erreur, on affiche un message
            display.refreshLabel(self.ui.label_2, "L'erreur suivante s'est produite pendant lors de la création de la base : "+repr(e)+".")

        else:
            # Si tout s'est bien passé, on affiche le message de succès et on commit
            display.refreshLabel(self.ui.label_2, "La base de données a été créée avec succès.")
            self.data.commit()
            # On émet le signal indiquant la modification de la table
            self.changedValue.emit()

    # En cas de clic sur le bouton d'insertion de données
    def insertDB(self):
        try:
            # On exécute les requêtes du fichier d'insertion
            db.updateDBfile(self.data, "data/insertDB.sql")

        except Exception as e:
            # En cas d'erreur, on affiche un message
            display.refreshLabel(self.ui.label_2, "L'erreur suivante s'est produite lors de l'insertion des données : "+repr(e)+".")

        else:
            # Si tout s'est bien passé, on affiche le message de succès et on commit
            display.refreshLabel(self.ui.label_2, "Un jeu de test a été inséré dans la base avec succès.")
            self.data.commit()
            # On émet le signal indiquant la modification de la table
            self.changedValue.emit()

    def createTrigger(self):
        try:
            # On exécute les requêtes du fichier d'insertion
            db.updateTriggerfile(self.data, "data/createTrigger.sql")

        except Exception as e:
            # En cas d'erreur, on affiche un message
            print(e)
            display.refreshLabel(self.ui.label_2,
                                 "L'erreur suivante s'est produite lors de la creation des triggers : " + repr(e) + ".")

        else:
            # Si tout s'est bien passé, on affiche le message de succès et on commit
            display.refreshLabel(self.ui.label_2, "Trigger créé avec succès.")
            self.data.commit()
            # On émet le signal indiquant la modification de la table
            self.changedValue.emit()

    # En cas de clic sur le bouton de suppression de la base
    def deleteDB(self):

        try:
            # On exécute les requêtes du fichier de suppression
            db.updateDBfile(self.data, "data/deleteDB.sql")

        except Exception as e:
            # En cas d'erreur, on affiche un message
            display.refreshLabel(self.ui.label_2, "Erreur lors de la suppression de la base de données : " + repr(e)+".")

        else:
            # Si tout s'est bien passé, on affiche le message de succès (le commit est automatique pour un DROP TABLE)
            display.refreshLabel(self.ui.label_2, "La base de données a été supprimée avec succès.")
            # On émet le signal indiquant la modification de la table
            self.changedValue.emit()

    ####################################################################################################################
    # Ouverture des autres fenêtres de l'application
    ####################################################################################################################

    # TODO 2 : ajouter la définition des méthodes déclenchées lors des clicks sur les boutons de la partie 2
    # TODO 3 : ajouter la définition des méthodes déclenchées lors des clicks sur les boutons de la partie 3

    # En cas de clic sur le bouton de visualisation des données
    def openData(self):
        if self.tablesDataDialog is not None:
            self.tablesDataDialog.close()
        self.tablesDataDialog = AppTablesData(self.data)
        self.tablesDataDialog.show()
        self.changedValue.connect(self.tablesDataDialog.refreshAllTables)

    # En cas de clic sur la fonction fournie 1
    def open_fct_fournie_1(self):
        if self.fct_fournie_1_dialog is not None:
            self.fct_fournie_1_dialog.close()
        self.fct_fournie_1_dialog = AppFctFournie1(self.data)
        self.fct_fournie_1_dialog.show()
        self.changedValue.connect(self.fct_fournie_1_dialog.refreshResult)

    # En cas de clic sur la fonction fournie 2
    def open_fct_fournie_2(self):
        if self.fct_fournie_2_dialog is not None:
            self.fct_fournie_2_dialog.close()
        self.fct_fournie_2_dialog = AppFctFournie2(self.data)
        self.fct_fournie_2_dialog.show()
        self.changedValue.connect(self.fct_fournie_2_dialog.refreshResult)

    # En cas de clic sur la fonction à compléter 1
    def open_fct_comp_1(self):
        if self.fct_comp_1_dialog is not None:
            self.fct_comp_1_dialog.close()
        self.fct_comp_1_dialog = AppFctComp1(self.data)
        self.fct_comp_1_dialog.show()
        self.changedValue.connect(self.fct_comp_1_dialog.refreshResult)

    # En cas de clic sur la fonction à compléter 2
    def open_fct_comp_2(self):
        if self.fct_comp_2_dialog is not None:
            self.fct_comp_2_dialog.close()
        self.fct_comp_2_dialog = AppFctComp2(self.data)
        self.fct_comp_2_dialog.show()
        self.changedValue.connect(self.fct_comp_2_dialog.refreshResult)

    # En cas de clic sur la fonction à compléter 3
    def open_fct_comp_3(self):
        if self.fct_comp_3_dialog is not None:
            self.fct_comp_3_dialog.close()
        self.fct_comp_3_dialog = AppFctComp3(self.data)
        self.fct_comp_3_dialog.show()
        self.changedValue.connect(self.fct_comp_3_dialog.refreshResult)

    # En cas de clic sur la fonction à compléter 4
    def open_fct_comp_4(self):
        if self.fct_comp_4_dialog is not None:
            self.fct_comp_4_dialog.close()
        self.fct_comp_4_dialog = AppFctComp4(self.data)
        self.fct_comp_4_dialog.show()
        self.changedValue.connect(self.fct_comp_4_dialog.refreshCatList)

    # En cas de clic sur la fonction 2.1
    def open_age_or_equipe(self):
        if self.age_or_equipe_dialog is not None:
            self.age_or_equipe_dialog.close()
        self.age_or_equipe_dialog = AppOrEquipe(self.data)
        self.age_or_equipe_dialog.show()
        self.changedValue.connect(self.age_or_equipe_dialog.refreshResult)

    # En cas de clic sur la fonction 2.2
    def open_classement_pays(self):
        if self.classement_pays_dialog is not None:
            self.classement_pays_dialog.close()
        self.classement_pays_dialog = AppClassementPays(self.data)
        self.classement_pays_dialog.show()
        self.changedValue.connect(self.classement_pays_dialog.refreshResult)

    def open_inscription_epreuve(self):
        if self.insciption_epreuve_dialog is not None:
            self.insciption_epreuve_dialog.close()
        self.insciption_epreuve_dialog = AppInscriptionEpreuve(self.data, self.changedValue)
        self.insciption_epreuve_dialog.show()
        self.changedValue.connect(self.insciption_epreuve_dialog.refreshResult)

    def open_Update_Resultats_Equipes(self):
        if self.Update_Resultats_Equipes_dialog is not None:
            self.Update_Resultats_Equipes_dialog.close()
        self.Update_Resultats_Equipes_dialog = AppUpdateResultatsEquipes(self.data, self.changedValue)
        self.Update_Resultats_Equipes_dialog.show()
        self.changedValue.connect(self.Update_Resultats_Equipes_dialog.refreshEpreuvesList)

    def open_inscription_sportif(self):
        if self.insciption_sportif_dialog is not None:
            self.insciption_sportif_dialog.close()
        self.insciption_sportif_dialog = AppInscriptionSportif(self.data, self.changedValue)
        self.insciption_sportif_dialog.show()
        self.changedValue.connect(self.insciption_sportif_dialog.setGoodLayout)

    def open_gestion_equipe(self):
        if self.gestion_equipe_dialog is not None:
            self.gestion_equipe_dialog.close()
        self.gestion_equipe_dialog = AppGestionEquipe(self.data, self.changedValue)
        self.gestion_equipe_dialog.show()
        self.changedValue.connect(self.gestion_equipe_dialog.refreshTables)

    ####################################################################################################################
    # Fonctions liées aux évènements (signal/slot/event)
    ####################################################################################################################

    # TODO 2 : penser à fermer comme il faut les fenêtres de la partie 2
    # TODO 3 : penser à fermer comme il faut les fenêtres de la partie 3

    # On intercepte l'évènement de cloture de la fenêtre principale pour intercaler quelques actions avant sa fermeture
    def closeEvent(self, event):

        # On ferme les éventuelles fenêtres encore ouvertes
        if self.tablesDataDialog is not None:
            self.tablesDataDialog.close()
        if self.fct_fournie_1_dialog is not None:
            self.fct_fournie_1_dialog.close()
        if self.fct_fournie_2_dialog is not None:
            self.fct_fournie_2_dialog.close()
        if self.fct_comp_1_dialog is not None:
            self.fct_comp_1_dialog.close()
        if self.fct_comp_2_dialog is not None:
            self.fct_comp_2_dialog.close()
        if self.fct_comp_3_dialog is not None:
            self.fct_comp_3_dialog.close()
        if self.fct_comp_4_dialog is not None:
            self.fct_comp_4_dialog.close()
        if self.age_or_equipe_dialog is not None:
            self.age_or_equipe_dialog.close()
        if self.classement_pays_dialog is not None:
            self.classement_pays_dialog.close()
        if self.Update_Resultats_Equipes_dialog is not None:
            self.Update_Resultats_Equipes_dialog.close()
        if self.insciption_epreuve_dialog is not None:
            self.insciption_epreuve_dialog.close()
        if self.insciption_sportif_dialog is not None:
            self.insciption_sportif_dialog.close()
        if self.gestion_equipe_dialog is not None:
            self.gestion_equipe_dialog.close()

        # On ferme proprement la base de données
        self.data.close()

        # On laisse l'évènement de clôture se terminer normalement
        event.accept()

# Lancement de la fenêtre principale
app = QApplication(sys.argv)
MainWindow = AppWindow()
MainWindow.show()
sys.exit(app.exec_())