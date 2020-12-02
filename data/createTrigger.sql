CREATE TRIGGER IF NOT EXISTS update_nb_participant AFTER INSERT ON LesInscriptions
BEGIN
    UPDATE LesEpreuves SET nbSportifsEp = nbSportifsEp + 1 WHERE numEp = NEW.numEp;
END;
