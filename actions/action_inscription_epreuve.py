import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic


class AppInscriptionEpreuve(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/inscription_epreuve.ui", self)
        self.data = data
        self.refreshNomEpreuve()
        self.ui.table_sp_ins_ep.setColumnCount(2)
        self.ui.table_sp_ins_ep.setHorizontalHeaderLabels(['A', 'B'])

    @pyqtSlot()
    def refreshResult(self):
        display.refreshLabel(self.ui.label_inscription_epreuve, "refesh result TODO")

    @pyqtSlot()
    def refreshNomEpreuve(self):
        try:
            query = """
            SELECT DISTINCT nomEp
            FROM LesEpreuves;
            """

            cursor = self.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            self.ui.combox_nom_ep_ins_ep.clear()
        else:
            display.refreshGenericCombo(self.ui.combox_nom_ep_ins_ep, result)

    @pyqtSlot()
    def refreshFormeEpreuve(self):
        nom = self.ui.combox_nom_ep_ins_ep.currentText()
        if nom == "None":
            nom = None
        try:
            query = """
                SELECT DISTINCT formeEp
                FROM LesEpreuves
                WHERE nomEp IS ?;
                """

            cursor = self.data.cursor()
            result = cursor.execute(query, [nom])
        except Exception as e:
            self.ui.combox_forme_ins_ep.clear()
        else:
            display.refreshGenericCombo(self.ui.combox_forme_ins_ep, result)

    @pyqtSlot()
    def refreshCategorieEpreuve(self):
        nom = self.ui.combox_nom_ep_ins_ep.currentText()
        if nom == "None":
            nom = None

        forme = self.ui.combox_forme_ins_ep.currentText()
        if forme == "None":
            forme = None

        try:
            query = """
                    SELECT DISTINCT categorieEp
                    FROM LesEpreuves
                    WHERE nomEp IS ? 
                      AND formeEp IS ?;
                    """

            cursor = self.data.cursor()
            result = cursor.execute(query, [nom, forme])
        except Exception as e:
            self.ui.combox_cat_ep_ins_ep.clear()
        else:
            display.refreshGenericCombo(self.ui.combox_cat_ep_ins_ep, result)

    @pyqtSlot()
    def refreshDateEpreuve(self):
        nom = self.ui.combox_nom_ep_ins_ep.currentText()
        if nom == "None":
            nom = None

        forme = self.ui.combox_forme_ins_ep.currentText()
        if forme == "None":
            forme = None

        categorie = self.ui.combox_cat_ep_ins_ep.currentText()
        if categorie == "None":
            categorie = None

        try:
            query = """
                        SELECT DISTINCT dateEp
                        FROM LesEpreuves
                        WHERE nomEp IS ?
                          AND formeEp IS ?
                          AND categorieEp IS ?;
                        """

            cursor = self.data.cursor()
            result = cursor.execute(query, [nom, forme, categorie])
        except Exception as e:
            self.ui.combox_date_ep_ins_ep.clear()
        else:
            display.refreshGenericCombo(self.ui.combox_date_ep_ins_ep, result)

    @pyqtSlot()
    def refreshNumEpreuve(self):
        nom = self.ui.combox_nom_ep_ins_ep.currentText()
        if nom == "None":
            nom = None

        forme = self.ui.combox_forme_ins_ep.currentText()
        if forme == "None":
            forme = None

        categorie = self.ui.combox_cat_ep_ins_ep.currentText()
        if categorie == "None":
            categorie = None

        date = self.ui.combox_date_ep_ins_ep.currentText()
        if date == "None":
            date = None

        try:
            query = """
                    SELECT DISTINCT numEp
                    FROM LesEpreuves
                    WHERE nomEp IS ?
                      AND formeEp IS ?
                      AND categorieEp IS ?
                      AND dateEp IS ?;
                    """

            cursor = self.data.cursor()
            result = cursor.execute(query, [nom, forme, categorie, date])
        except Exception as e:
            self.ui.combox_num_ep_ins_ep.clear()
        else:
            display.refreshGenericCombo(self.ui.combox_num_ep_ins_ep, result)

    @pyqtSlot()
    def register(self):
        display.refreshLabel(self.ui.label_inscription_epreuve, "refesh result TODO")
