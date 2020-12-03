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
        self.refreshResult()

    @pyqtSlot()
    def refreshResult(self):
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

        num = self.ui.combox_num_ep_ins_ep.currentText()
        if num == "None":
            num = None

        try:
            if forme == "individuelle":
                query = """
                        SELECT numSp, nomSp, prenomSp, pays, categorieSp, date(dateNaisSp), agesp
                        FROM LesSportifs
                        EXCEPT 
                        SELECT numSp, nomSp, prenomSp, pays, categorieSp, date(dateNaisSp), agesp
                        FROM LesSportifs JOIN LesInscriptions ON (numIn = numSp)
                        WHERE numEp = ?
                        """
            elif forme == "par couple":
                query = """
                        SELECT numEq, nbEquipiersEq, pays, nomEquipier 
                        FROM LesEquipes
                        WHERE nbEquipiersEq = 2
                        EXCEPT 
                        SELECT numEq, nbEquipiersEq, pays, nomEquipier
                        FROM LesEquipes JOIN LesInscriptions  ON (numIn = numEq)
                        WHERE numEp = ?;
                        """
            else:
                query = """
                        SELECT numEq, nbEquipiersEq, pays, nomEquipier 
                        FROM LesEquipes
                        EXCEPT 
                        SELECT numEq, nbEquipiersEq, pays, nomEquipier
                        FROM LesEquipes JOIN LesInscriptions  ON (numIn = numEq)
                        WHERE numEp = ?;
                        """
            cursor = self.data.cursor()
            result = cursor.execute(query, [num])
        except Exception as e:
            self.ui.table_sp_ins_ep.setRowCount(0)
            display.refreshLabel(self.ui.label_inscription_epreuve, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_sp_ins_ep, result)
            if i == 0:
                display.refreshLabel(self.ui.label_inscription_epreuve, "Aucun résultat")

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
            self.adaptTableByType(forme)

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
        if self.ui.radio_inscription.isChecked():
            select = self.ui.table_sp_ins_ep.selectionModel().selectedRows()
            num = self.ui.combox_num_ep_ins_ep.currentText()
            for row in sorted(select):
                try:
                    sportif = row.data()
                    query = """
                            INSERT INTO LesInscriptions(numIn, numEp) VALUES (?, ?);
                            """
                    cursor = self.data.cursor()
                    cursor.execute(query, [sportif, num])
                except Exception as e:
                    print(e)
                else:
                    self.refreshResult()
                    self.data.commit()
        else:
            select = self.ui.table_sp_ins_ep.selectionModel().selectedRows()
            num = self.ui.combox_num_ep_ins_ep.currentText()
            for row in sorted(select):
                try:
                    sportif = row.data()
                    query = """
                            DELETE FROM LesInscriptions WHERE numIn = ? AND numEp = ?;
                            """
                    cursor = self.data.cursor()
                    cursor.execute(query, [sportif, num])
                except Exception as e:
                    print(e)
                else:
                    self.refreshResult()
                    self.data.commit()



    def adaptTableByType(self, typeEpreuve):
        if typeEpreuve == "individuelle":
            self.ui.table_sp_ins_ep.setColumnCount(7)
            self.ui.table_sp_ins_ep.setHorizontalHeaderLabels(['numSp', 'nomSp', 'prenomSp', 'pays', 'categorieSp', 'dateNaisSp', 'agesp'])
        else:
            self.ui.table_sp_ins_ep.setColumnCount(4)
            self.ui.table_sp_ins_ep.setHorizontalHeaderLabels(['numEq', 'nbEquipiersEq', 'pays', 'nomEquipier'])

    @pyqtSlot()
    def changeObjectif(self):
        if self.ui.radio_inscription.isChecked():
            self.ui.validate_ins_ep.setText('Inscrire')
        else:
            self.ui.validate_ins_ep.setText('Désinscrire')


