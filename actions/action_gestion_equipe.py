import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5 import uic


class AppGestionEquipe(QDialog):
    # Constructeur
    def __init__(self, data: sqlite3.Connection, changedValue):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/gestion_equipe.ui", self)
        self.data = data
        self.changedValue = changedValue
        self.refreshTables()

    @pyqtSlot()
    def refreshTables(self):
        tableDelete = self.ui.table_delete
        labelDelete = self.ui.label_delete

        comboUpdateAddEq = self.ui.combo_update_add_eq
        comboUpdateRemoveEq = self.ui.combo_update_remove_eq
        labelUpdateAdd = self.ui.label_update_add
        labelUpdateRemove = self.ui.label_update_remove

        cbCreateSp1 = self.ui.cb_premier_sp
        labelCreate = self.ui.label_create

        # PAGE DELETE
        try:
            query = """
                    SELECT numEq, nbEquipiersEq, pays, nomEquipier
                    FROM LesEquipes
                    WHERE numEq NOT IN (SELECT gold FROM LesResultats)
                      AND numEq NOT IN (SELECT silver FROM LesResultats)
                      AND numEq NOT IN (SELECT bronze FROM LesResultats)
                    """
            cursor = self.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            tableDelete.setRowCount(0)
            display.refreshLabel(labelDelete, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(tableDelete, result)
            if i == 0:
                display.refreshLabel(labelDelete, "Aucune équipe ne peut être supprimmé.")

        # PAGE UPDATE
        ## ADD
        try:
            query = """
                    SELECT numEq || '- ' || nbEquipiersEq || '- ' || pays || '- ' || nomEquipier
                    FROM LesEquipes
                    """
            cursor = self.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            comboUpdateAddEq.clear()
            display.refreshLabel(labelUpdateAdd, "Impossible de trouver les équipes : " + repr(e))
        else:
            display.refreshGenericCombo(comboUpdateAddEq, result)

        ## REMOVE
        try:
            query = """
                    SELECT numEq || '- ' || nbEquipiersEq || '- ' || pays || '- ' || nomEquipier
                    FROM LesEquipes
                    WHERE nbEquipiersEq > 2
                    """
            cursor = self.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            comboUpdateRemoveEq.clear()
            display.refreshLabel(labelUpdateRemove, "Impossible de trouver les équipes : " + repr(e))
        else:
            display.refreshGenericCombo(comboUpdateRemoveEq, result)

        # PAGE CREATE
        try:
            query = """
                    SELECT numSp || '- ' || nomSp || ' ' || prenomSp 
                    FROM LesSportifs
                    """
            cursor = self.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            cbCreateSp1.clear()
            display.refreshLabel(labelCreate, "Impossible de trouver les sportifs : " + repr(e))
        else:
            display.refreshGenericCombo(cbCreateSp1, result)

    @pyqtSlot()
    def updateSportifList(self):
        eqAdd = self.ui.combo_update_add_eq.currentText().split("-")[0]
        eqRemove = self.ui.combo_update_remove_eq.currentText().split("-")[0]

        labelUpdateAdd = self.ui.label_update_add
        labelUpdateRemove = self.ui.label_update_remove

        cbSpAdd = self.ui.combo_update_add_sp
        cbSpRemove = self.ui.combo_update_remove_sp

        # ADD
        try:
            query = """
                    SELECT numSp || ' - ' || nomSp || ' - ' || prenomSp
                    FROM LesSportifs_base
                    WHERE pays = (SELECT pays FROM LesEquipes WHERE numEq = ?)
                      AND numSp NOT IN (SELECT numSp FROM LesEquipiers WHERE numEq = ?)
                    """
            cursor = self.data.cursor()
            result = cursor.execute(query, [eqAdd, eqAdd])
        except Exception as e:
            cbSpAdd.clear()
            display.refreshLabel(labelUpdateAdd, "Impossible de trouver les sportifs : " + repr(e))
        else:
            display.refreshGenericCombo(cbSpAdd, result)

        # REMOVE
        try:
            query = """
                    SELECT numSp || ' - ' || nomSp || ' - ' || prenomSp
                    FROM LesSportifs_base
                    WHERE numSp IN (SELECT numSp FROM LesEquipiers WHERE numEq = ?)
                    """
            cursor = self.data.cursor()
            result = cursor.execute(query, [eqRemove])
        except Exception as e:
            cbSpRemove.clear()
            display.refreshLabel(labelUpdateRemove, "Impossible de trouver les sportifs : " + repr(e))
        else:
            display.refreshGenericCombo(cbSpRemove, result)

    @pyqtSlot()
    def updateSp2List(self):
        sp = self.ui.cb_premier_sp.currentText().split("-")[0]
        cb = self.ui.cb_second_sp
        label = self.ui.label_create
        try:
            query = """
                    SELECT numSp || '- ' || nomSp || ' ' || prenomSp 
                    FROM LesSportifs
                    WHERE numSp <> ?
                      AND pays = (SELECT pays FROM LesSportifs_base WHERE numSp = ?)
                    """
            cursor = self.data.cursor()
            result = cursor.execute(query, [sp, sp])
        except Exception as e:
            cb.clear()
            display.refreshLabel(label, "Impossible de trouver les sportifs : " + repr(e))
        else:
            display.refreshGenericCombo(cb, result)

    @pyqtSlot()
    def deleteEquipe(self):
        tableDelete = self.ui.table_delete
        labelDelete = self.ui.label_delete
        if tableDelete.selectionModel().hasSelection():
            row = tableDelete.currentRow()
            num = tableDelete.item(row, 0).text()

            try:
                query = """
                        DELETE FROM LesInscriptions WHERE numIn = ?
                        """
                cursor = self.data.cursor()
                cursor.execute(query, [num])

                query = """
                        DELETE FROM LesEquipiers WHERE numEq = ?
                        """
                cursor = self.data.cursor()
                cursor.execute(query, [num])
            except Exception as e:
                display.refreshLabel(labelDelete, "Impossible de supprimer l'équipe : " + repr(e))
            else:
                display.refreshLabel(labelDelete, "Equipe n°" + str(num) + " supprimer avec succés")
                self.data.commit()
                self.changedValue.emit()
        else:
            display.refreshLabel(labelDelete, 'Commencer par sélection une équipe a supprimmer.')

    @pyqtSlot()
    def updateEquipeRemove(self):
        eqRemove = self.ui.combo_update_remove_eq.currentText().split("-")[0]
        spRemove = self.ui.combo_update_remove_sp.currentText().split("-")[0]
        labelRemove = self.ui.label_update_remove

        try:
            cursor = self.data.cursor()
            # On supprimme le sportif de la bd
            query = """
                    DELETE FROM LesEquipiers WHERE numSp = ? AND numEq = ?;
                    """
            cursor.execute(query, [spRemove, eqRemove])

        except Exception as e:
            labelRemove.setText('Impossible de supprimer le sportif n°' + str(spRemove) + '. ' + repr(e))
        else:
            labelRemove.setText("Sportif n°" + str(spRemove) + " supprimé avec succès de l'équipe n°" + str(eqRemove) + ".")
            self.data.commit()
            self.changedValue.emit()


    @pyqtSlot()
    def updateEquipeAdd(self):
        eq = self.ui.combo_update_add_eq.currentText().split("-")[0]
        sp = self.ui.combo_update_add_sp.currentText().split("-")[0]
        label = self.ui.label_update_add

        try:
            cursor = self.data.cursor()
            query = """
                    INSERT INTO LesEquipiers (numEq, numSp) VALUES (?, ?)
                    """
            cursor.execute(query, [eq, sp])

        except Exception as e:
            label.setText("Impossible d'ajouter le sportif n°" + str(sp) + '. ' + repr(e))
        else:
            label.setText(
                "Sportif n°" + str(sp) + " ajouté avec succès à l'équipe n°" + str(eq) + ".")
            self.data.commit()
            self.changedValue.emit()

    @pyqtSlot()
    def createEquipe(self):
        num = self.ui.spin_create_num.value()
        sp1 = self.ui.cb_premier_sp.currentText().split("-")[0]
        sp2 = self.ui.cb_second_sp.currentText().split("-")[0]
        label = self.ui.label_create
        try:
            cursor = self.data.cursor()
            query = """
                    INSERT INTO LesEquipiers (numEq, numSp) VALUES (?, ?)
                    """
            cursor.execute(query, [num, sp1])
            cursor.execute(query, [num, sp2])

        except Exception as e:
            label.setText("Impossible d'ajouter l'équipe n°" + str(num) + '. ' + repr(e))
        else:
            label.setText(
                "Equipe n°" + str(num) + " ajouté avec succès.")
            self.data.commit()
            self.changedValue.emit()