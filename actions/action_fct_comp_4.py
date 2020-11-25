
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 4
class AppFctComp4(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_4.ui", self)
        self.data = data
        self.refreshCatList()
        self.refreshEquipeList()

    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
        display.refreshLabel(self.ui.label_fct_comp_4, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT numSp, nomSp, prenomSp, categorieSp, Date(dateNaisSp) FROM LesSportifs_base JOIN LesEquipiers USING (numSp) WHERE pays = ? AND numEq=?",
                [self.ui.comboBox_fct_4_pays.currentText(), self.ui.comboBox_fct_4_equipe.currentText()]
            )
        except Exception as e:
            self.ui.table_fct_comp_4.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_4, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_fct_comp_4, result)
            if i == 0:
                display.refreshLabel(self.ui.label_fct_comp_4, "Aucun résultat")

    # Fonction de mise à jour des catégories
    @pyqtSlot()
    def refreshCatList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT pays FROM LesSportifs_base ORDER BY pays")
        except Exception as e:
            self.ui.comboBox_fct_4_pays.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_fct_4_pays, result)

    @pyqtSlot()
    def refreshEquipeList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT numEq FROM LesSportifs_base JOIN lesEquipiers USING(numSp) WHERE pays = ? ORDER BY numEq", [self.ui.comboBox_fct_4_pays.currentText()])
        except Exception as e:
            self.ui.comboBox_fct_4_equipe.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_fct_4_equipe, result)
