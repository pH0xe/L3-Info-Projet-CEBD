
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic


class AppOrEquipe(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/age_or_equipe.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
        try:
            query = """
            WITH goldEquipe AS (
                SELECT gold, numEp 
                FROM LesResultats JOIN LesEpreuves USING (numep) 
                WHERE formeEp='par equipe'
            ) 
            SELECT DISTINCT numEq, AVG(ageSp) AS AgeMoyen 
            FROM goldEquipe G JOIN LesEquipiers E ON (G.gold = E.numEq) JOIN LesSportifs USING (numSp) 
            GROUP BY numEq, numEp;
            """


            cursor = self.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            self.ui.table_age_or_equipe.setRowCount(0)
            display.refreshLabel(self.ui.label_age_or_equipe, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_age_or_equipe, result)
            if i == 0:
                display.refreshLabel(self.ui.table_age_or_equipe, "Aucun résultat")
