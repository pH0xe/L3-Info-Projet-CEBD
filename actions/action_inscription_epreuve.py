
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic


class AppInscriptionEpreuve(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
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
        try:
            query = """
                SELECT DISTINCT formeEp
                FROM LesEpreuves
                WHERE nomEp = ?;
                """

            cursor = self.data.cursor()
            result = cursor.execute(query, [self.ui.combox_nom_ep_ins_ep.currentText()])
        except Exception as e:
            self.ui.combox_forme_ins_ep.clear()
        else:
            display.refreshGenericCombo(self.ui.combox_forme_ins_ep, result)

    @pyqtSlot()
    def refreshCategorieEpreuve(self):
        try:
            query = """
                    SELECT DISTINCT categorieEp
                    FROM LesEpreuves
                    WHERE nomEp = ? 
                      AND formeEp = ?;
                    """

            cursor = self.data.cursor()
            result = cursor.execute(query, [self.ui.combox_nom_ep_ins_ep.currentText(), self.ui.combox_forme_ins_ep.currentText()])
        except Exception as e:
            self.ui.combox_cat_ep_ins_ep.clear()
        else:
            display.refreshGenericCombo(self.ui.combox_cat_ep_ins_ep, result)

    @pyqtSlot()
    def refreshDateEpreuve(self):
        try:
            query = """
                        SELECT DISTINCT dateEp
                        FROM LesEpreuves
                        WHERE nomEp = ?
                          AND formeEp = ?
                          AND categorieEp = ?;
                        """

            cursor = self.data.cursor()
            result = cursor.execute(query, [self.ui.combox_nom_ep_ins_ep.currentText(),
                                            self.ui.combox_forme_ins_ep.currentText(),
                                            self.ui.combox_cat_ep_ins_ep.currentText()
                                            ])
        except Exception as e:
            self.ui.combox_date_ep_ins_ep.clear()
        else:
            display.refreshGenericCombo(self.ui.combox_date_ep_ins_ep, result)

    @pyqtSlot()
    def refreshNumEpreuve(self):
        try:
            query = """
                    SELECT DISTINCT numEp
                    FROM LesEpreuves
                    WHERE nomEp = ?
                      AND formeEp = ?
                      AND categorieEp = ?
                      AND dateEp = ?;
                    """

            cursor = self.data.cursor()
            result = cursor.execute(query, [self.ui.combox_nom_ep_ins_ep.currentText(),
                                            self.ui.combox_forme_ins_ep.currentText(),
                                            self.ui.combox_cat_ep_ins_ep.currentText(),
                                            self.ui.combox_date_ep_ins_ep.currentText(),
                                            ])
        except Exception as e:
            self.ui.combox_num_ep_ins_ep.clear()
        else:
            display.refreshGenericCombo(self.ui.combox_num_ep_ins_ep, result)

    @pyqtSlot()
    def register(self):
        display.refreshLabel(self.ui.label_inscription_epreuve, "refesh result TODO")