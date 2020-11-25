
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


class AppClassementPays(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/classement_pays.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "WITH EquipePays AS (SELECT numEq, pays FROM LesEquipiers JOIN LesSportifs USING (numSp) GROUP BY numEq, pays), allPays AS (SELECT DISTINCT pays FROM LesSportifs_base), GoldPaysUnion AS (SELECT COUNT(numEp) AS nbOr, pays FROM LesResultats JOIN LesSportifs_base ON (gold = numSp)         GROUP BY pays         UNION ALL         SELECT COUNT(numEp) AS nbOr, pays         FROM EquipePays JOIN LesResultats ON (gold = numEq)         GROUP BY pays     ),      GoldPays AS (          SELECT pays, IFNULL(SUM(nbOr), 0) as nbOr          FROM allPays LEFT OUTER JOIN GoldPaysUnion USING (pays)          GROUP BY pays      ),      SilverPaysUnion AS (         SELECT COUNT(numEp) AS nbArgent, pays         FROM LesResultats JOIN LesSportifs_base ON (silver = numSp)         GROUP BY pays         UNION ALL         SELECT COUNT(numEp) AS nbArgent, pays         FROM EquipePays JOIN LesResultats ON (silver = numEq)         GROUP BY pays     ),      SilverPays AS (          SELECT pays, IFNULL(SUM(nbArgent), 0) as nbArgent          FROM allPays LEFT OUTER JOIN SilverPaysUnion USING (pays)          GROUP BY pays      ),      BronzePaysUnion AS (         SELECT COUNT(numEp) AS nbBronze, pays         FROM LesResultats JOIN LesSportifs_base ON (bronze = numSp)         GROUP BY pays         UNION ALL         SELECT COUNT(numEp) AS nbBronze, pays         FROM EquipePays JOIN LesResultats ON (bronze = numEq)         GROUP BY pays     ),      BronzePays AS (          SELECT pays, IFNULL(SUM(nbBronze), 0) as nbBronze          FROM allPays LEFT OUTER JOIN BronzePaysUnion USING (pays)          GROUP BY pays      ) SELECT * FROM  GoldPays JOIN SilverPays USING (pays) JOIN BronzePays USING (pays) ORDER BY nbOr DESC, nbArgent DESC, nbBronze DESC;"
            )
        except Exception as e:
            self.ui.table_classement_pays.setRowCount(0)
            display.refreshLabel(self.ui.label_classement_pays, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_classement_pays, result)
            if i == 0:
                display.refreshLabel(self.ui.label_classement_pays, "Aucun résultat")
