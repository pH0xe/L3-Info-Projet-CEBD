
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic


class AppUpdateResultatsEquipes(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/update_resultats_equipes.ui", self)
        self.data = data
        self.refreshEpreuvesList()


    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
        try:
            cursor = self.data.cursor()
            if self.ui.radioInsert.isChecked():
                query="""
                INSERT INTO LesResultats (numEp, gold, silver, bronze) VALUES (?, ?, ?, ?);
                """
                cursor.execute(query,
                               [self.ui.comboBox_noEp.currentText(),
                                self.ui.comboBox_1ere_place.currentText(),
                                self.ui.comboBox_2eme_place.currentText(),
                                self.ui.comboBox_3eme_place.currentText()])
            else:
                query="""
                UPDATE LesResultats SET gold = ?, silver = ?, bronze = ? WHERE numEp = ?;
                """
                cursor.execute(query,
                               [self.ui.comboBox_1ere_place.currentText(),
                                self.ui.comboBox_2eme_place.currentText(),
                                self.ui.comboBox_3eme_place.currentText(),
                                self.ui.comboBox_noEp.currentText()])
        except Exception as e:
            display.refreshLabel(self.ui.label_Error, "Impossible d'afficher les résultats : " + repr(e))
        else:
            self.refreshEpreuvesList()


    @pyqtSlot()
    def refreshEpreuvesList(self):
        try:
            if self.ui.radioInsert.isChecked():
                query = """SELECT numEp
                FROM LesEpreuves
                EXCEPT
                SELECT numEp
                FROM LesResultats
                ORDER BY numEp
                """
            else:
                query="""
                SELECT numEp FROM LesResultats
                """
            cursor = self.data.cursor()
            result = cursor.execute(query)
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
                "SELECT DISTINCT numIn FROM LesInscriptions WHERE numEp = ? AND numIn <> ? ORDER BY numIn",
                [self.ui.comboBox_noEp.currentText(),self.ui.comboBox_1ere_place.currentText()])
        except Exception as e:
            self.ui.comboBox_2eme_place.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_2eme_place, result)

    @pyqtSlot()
    def refresh3emeplaceList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT DISTINCT numIn FROM LesInscriptions WHERE numEp = ? AND numIn <> ? AND numIn <> ? ORDER BY numIn",
                [self.ui.comboBox_noEp.currentText(),self.ui.comboBox_1ere_place.currentText(),self.ui.comboBox_2eme_place.currentText()])
        except Exception as e:
            self.ui.comboBox_3eme_place.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_3eme_place, result)
    @pyqtSlot()
    def refreshEquipesList(self):
        self.refresh1ereplaceList()
        self.refresh2emeplaceList()
        self.refresh3emeplaceList()