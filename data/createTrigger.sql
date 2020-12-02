CREATE TRIGGER IF NOT EXISTS au_moins_3_inscrits BEFORE INSERT ON LesResultats
BEGIN
    SELECT CASE
        WHEN ((SELECT COUNT(*) FROM LesInscriptions WHERE numEp = NEW.numEp) <3)
        THEN raise(abort, 'Moins de 3 inscrits dans l''épreuve')
    END;
END;
/