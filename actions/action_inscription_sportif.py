
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5 import uic


class AppInscriptionSportif(QDialog):
    # Constructeur
    def __init__(self, data:sqlite3.Connection, changedValue):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/inscription_sportif.ui", self)
        self.data = data
        self.setGoodLayout()
        self.changedValue = changedValue
        self.insert = self.ui.radioInsert.isChecked()

    def setGoodLayout(self):
        self.ui.insert = self.ui.radioInsert.isChecked()
        self.setVisibilityDelete(self.insert)
        self.setVisibilityInsert(not self.insert)
        if not self.insert:
            self.refreshTable()

    def setVisibilityInsert(self, hidden):
        self.ui.label_insert_num.setHidden(hidden)
        self.ui.spin_insert_num.setHidden(hidden)

        self.ui.label_insert_nom.setHidden(hidden)
        self.ui.line_insert_nom.setHidden(hidden)

        self.ui.label_insert_prenom.setHidden(hidden)
        self.ui.line_insert_prenom.setHidden(hidden)

        self.ui.line_insert_pays.setHidden(hidden)
        self.ui.label_insert_pays.setHidden(hidden)

        self.ui.label_insert_categorie.setHidden(hidden)
        self.ui.combo_insert_categorie.setHidden(hidden)

        self.ui.label_insert_date_nais.setHidden(hidden)
        self.ui.date_insert_naissance.setHidden(hidden)

        self.ui.label_Error.setText(' ')

    def setVisibilityDelete(self, hidden):
        self.ui.label_delete.setHidden(hidden)
        self.ui.table_delete.setHidden(hidden)
        self.ui.label_delete_recap.setHidden(hidden)
        self.ui.label_delete_recap.setText(' ')
        self.ui.label_Error.setText(' ')

    @pyqtSlot()
    def refreshTable(self):
        try:
            query = """
                    SELECT numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp, ageSp
                    FROM LesSportifs
                    WHERE numSp not in (SELECT gold FROM LesResultats)
                      AND numSp not in (SELECT silver FROM LesResultats)
                      AND numSp not in (SELECT bronze FROM LesResultats)
                    """
            cursor = self.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            self.ui.table_delete.setRowCount(0)
            display.refreshLabel(self.ui.label_Error, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_delete, result)
            if i == 0:
                display.refreshLabel(self.ui.label_Error, "Aucun sportif dans la base")

    @pyqtSlot()
    def setLabelRecap(self):
        if self.ui.table_delete.selectionModel().hasSelection():
            row = self.ui.table_delete.currentRow()
            num = self.ui.table_delete.item(row, 0).text()
            nom = self.ui.table_delete.item(row, 1).text()
            prenom = self.ui.table_delete.item(row, 2).text()
            self.ui.label_delete_recap.setText('Sportif n°' + str(num) + ', ' + str(nom) + ' ' + str(prenom))

    @pyqtSlot()
    def validate(self):
        if self.insert:
            self.insertSportif()
        else:
            self.deleteSportif()

    def insertSportif(self):
        num = self.ui.spin_insert_num.value()
        nom = self.ui.line_insert_nom.text()
        prenom = self.ui.line_insert_prenom.text()
        date = self.ui.date_insert_naissance.date().toString("yyyy-MM-dd") + ' 00:00:00'
        pays = self.ui.line_insert_pays.text()
        cat = self.ui.combo_insert_categorie.currentText()
        if nom and prenom and pays and cat:
            try:
                cursor = self.data.cursor()

                # On peux inserer le sportif dans la BD
                query = """
                        INSERT INTO LesSportifs_base VALUES (?, ?, ?, ?, ?, ?)
                        """
                cursor.execute(query, [num, nom, prenom, pays, cat, date])

            except Exception as e:
                self.ui.label_Error.setText('Impossible d\'ajouter le sportif n°' + str(num) + '. ' + repr(e))
            else:
                self.ui.label_Error.setText('Sportif n°' + str(num) + ' ajouter avec succée. ')
                self.data.commit()
                self.changedValue.emit()
        else:
            self.ui.label_Error.setText('Merci de d\'abord remplir les valeur requise.')

    def deleteSportif(self):
        if self.ui.table_delete.selectionModel().hasSelection():
            row = self.ui.table_delete.currentRow()
            num = self.ui.table_delete.item(row, 0).text()
            try:
                cursor = self.data.cursor()

                # On supprime le sportif des epreuves ou il est inscrit.
                query = """
                DELETE FROM LesInscriptions WHERE numIn = ?;
                """
                cursor.execute(query, [num])

                # On supprime le sportif des équipe ou il est inscrit
                query = """
                DELETE FROM LesEquipiers WHERE numSp = ?;
                """
                cursor.execute(query, [num])

                # On supprimme le sportif de la bd
                query = """
                        DELETE FROM LesSportifs_base WHERE numSp = ?;
                        """
                cursor.execute(query, [num])

            except Exception as e:
                # SI il y a eu une erreur on rollback les delete qui on deja eu lieux
                self.data.rollback()
                self.ui.label_Error.setText('Impossible de supprimer le sportif n°' + str(num) + '. ' + repr(e))
            else:
                self.ui.label_Error.setText('Sportif n°' + str(num) + ' supprimmer avec succée. ')
                self.refreshTable()
                self.data.commit()
                self.changedValue.emit()
        else:
            self.ui.label_Error.setText('Séléctionner d\'abord un sportif.')