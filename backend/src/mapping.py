query_map = {
    "Elenca i film del <ANNO>.":
        "SELECT titolo FROM Film WHERE anno = {ANNO};",

    "Quali sono i registi presenti su Netflix?":
        """
        SELECT DISTINCT r.nome
        FROM Regista r
        JOIN Film f ON f.regista_id = r.id
        JOIN Film_Piattaforma fp ON fp.film_id = f.id
        JOIN Piattaforma p ON p.id = fp.piattaforma_id
        WHERE LOWER(p.nome) = 'netflix';
        """,

    "Elenca tutti i film di fantascienza.":
        """
        SELECT f.titolo
        FROM Film f
        JOIN Genere g ON f.genere_id = g.id
        WHERE LOWER(g.nome) = 'fantascienza';
        """,

    "Quali film sono stati fatti da un regista di almeno <ANNI> anni?":
        """
        SELECT f.titolo
        FROM Film f
        JOIN Regista r ON r.id = f.regista_id
        WHERE r.eta >= {ANNI};
        """,

    "Quali registi hanno fatto più di un film?":
        """
        SELECT r.nome
        FROM Regista r
        JOIN Film f ON r.id = f.regista_id
        GROUP BY r.id
        HAVING COUNT(f.id) > 1;
        """
}