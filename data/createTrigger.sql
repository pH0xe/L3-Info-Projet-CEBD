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

-- Verifier que l'on de l'inscription a une équipe le sportif fait bien partie du bon pays
CREATE TRIGGER IF NOT EXISTS bon_pays_equipe
    BEFORE INSERT ON LesEquipiers
BEGIN
    SELECT CASE
        WHEN ((SELECT pays FROM LesSportifs_base WHERE numSp = NEW.numSp) <> (SELECT pays FROM LesEquipes WHERE numEq = NEW.numEq))
        THEN RAISE(ABORT, 'Le nouveau membre ne fait pas partie du bon pays.')
    END;
END;
/

-- verifier que le sportif a bien un num entre 1000 et 1500
CREATE TRIGGER IF NOT EXISTS sportif_num
    BEFORE INSERT ON LesSportifs_base
BEGIN
    SELECT CASE
        WHEN(NEW.numSp > 1500 OR NEW.numSp < 1000)
        THEN RAISE(ABORT, 'Numéros du sportif invalide. Doit etre entre 1000 et 1500.')
    END;
END;
/

-- verifier que l'équipe a bien un num entre 1 et 100
CREATE TRIGGER IF NOT EXISTS equipe_num
    BEFORE INSERT ON LesEquipiers
BEGIN
    SELECT CASE
        WHEN (NEW.numEq > 100 OR NEW.numEq < 1)
        THEN RAISE(ABORT, 'Numéros d''équipe invalide. Doit être entre 1 et 100.')
    END;
END;
/