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
