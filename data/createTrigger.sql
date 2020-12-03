-- Verifie qu'une équipe contient le bon nombre d'equipier pour l'epreuve cible
CREATE TRIGGER IF NOT EXISTS check_nb_participant
    BEFORE INSERT ON LesInscriptions
    WHEN (NEW.numIn <= 100)
BEGIN
    SELECT CASE
        WHEN ((SELECT nbEquipiersEq FROM LesEquipes WHERE numEq = NEW.numIn) <> (SELECT nbSportifsEp FROM LesEpreuves WHERE LesEpreuves.numEp = NEW.numEp)
            )
            THEN RAISE(ABORT, 'L''équipe doit contenir le bon nombre de sportif')
    END;
END;
/

-- verifie la presence de 3 inscrits minimum avant l'insertion de resultat (normalement catch par l'app avant)
CREATE TRIGGER IF NOT EXISTS au_moins_3_inscrits
    BEFORE INSERT ON LesResultats
BEGIN
    SELECT CASE
        WHEN ((SELECT COUNT(*) FROM LesInscriptions WHERE numEp = NEW.numEp) <3)
        THEN raise(ABORT, 'Moins de 3 inscrits dans l''épreuve')
    END;
END;
/

-- Verifie que l'epreuve concerve bien 3 sportifs en cas de delete
CREATE TRIGGER IF NOT EXISTS au_moins_3_inscrits_delete
    BEFORE DELETE ON LesInscriptions
BEGIN
    SELECT CASE
        WHEN ((SELECT nombreInscrit FROM LesEpreuvesView WHERE numEp = OLD.numEp) < 4)
        THEN RAISE(ABORT, 'Moins de 3 inscrit en cas de suppression. Supprimer l''épreuve ou inscrivez d''autre personnes.')
    end;
end;
/

-- Verifier que l'on de l'inscription a une équipe le sportif fait bien partie du bon pays
CREATE TRIGGER IF NOT EXISTS bon_pays_equipe
    BEFORE INSERT ON LesEquipiers
BEGIN
    SELECT CASE
        WHEN ((SELECT pays FROM LesSportifs_base WHERE numSp = NEW.numSp) = (SELECT pays FROM LesEquipes WHERE numEq = 1))
        THEN RAISE(ABORT, 'Le nouveau membre ne fait pas partie du bon pays.')
    END;
end;
/