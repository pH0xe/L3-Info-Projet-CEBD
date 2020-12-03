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

CREATE TRIGGER IF NOT EXISTS au_moins_3_inscrits BEFORE INSERT ON LesResultats
BEGIN
    SELECT CASE
        WHEN ((SELECT COUNT(*) FROM LesInscriptions WHERE numEp = NEW.numEp) <3)
        THEN raise(abort, 'Moins de 3 inscrits dans l''épreuve')
    END;
END;
/