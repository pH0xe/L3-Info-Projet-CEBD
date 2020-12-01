
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic


class UpdateResultatsEquipes(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/update_resultats_equipes.ui", self)
        self.data = data
        self.refreshResult()
        self.refreshEpreuvesList()
        self.refresh1ereplaceList()
        self.refresh2emeplaceList()
        self.refresh3emeplaceList()
    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
        try:
            query = """
            SELECT DISTINCT pays FROM LesSportifs 
            """
            cursor = self.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            self.ui.table_Update_Resultats_Equipes.setRowCount(0)
            display.refreshLabel(self.ui.label_Update_Resultats_Equipes, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_Update_Resultats_Equipes, result)
            if i == 0:
                display.refreshLabel(self.ui.table_Update_Resultats_Equipes, "Aucun résultat")

    @pyqtSlot()
    def refreshEpreuvesList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                """SELECT numEp 
                FROM LesEpreuves
                MINUS
                SELECT numEp
                FROM LesResultats
                ORDER BY numEp
                """)
        except Exception as e:
            self.ui.comboBox_noEp.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_noEp, result)

    @pyqtSlot()
    def refresh1ereplaceList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT DISTINCT numIn FROM LesInscriptions WHERE numEp = ? ORDER BY numIn",
                [self.ui.comboBox_noEp.currentText()])
        except Exception as e:
            self.ui.comboBox_1ere_place.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_1ere_place, result)

    @pyqtSlot()
    def refresh2emeplaceList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT DISTINCT numIn FROM LesInscriptions WHERE numEp = ? ORDER BY numIn",
                [self.ui.comboBox_noEp.currentText()])
        except Exception as e:
            self.ui.comboBox_2eme_place.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_2eme_place, result)

    @pyqtSlot()
    def refresh3emeplaceList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT DISTINCT numIn FROM LesInscriptions WHERE numEp = ? ORDER BY numIn",
                [self.ui.comboBox_noEp.currentText()])
        except Exception as e:
            self.ui.comboBox_3eme_place.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_3eme_place, result)