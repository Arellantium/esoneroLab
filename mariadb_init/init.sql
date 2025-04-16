-- ==========================
-- TABELLA: Regista
-- ==========================
CREATE TABLE Regista (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    eta INT
);

-- ==========================
-- TABELLA: Genere
-- ==========================
CREATE TABLE Genere (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50)
);

-- ==========================
-- TABELLA: Piattaforma
-- ==========================
CREATE TABLE Piattaforma (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100)
);

-- ==========================
-- TABELLA: Film
-- ==========================
CREATE TABLE Film (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titolo VARCHAR(255),
    anno INT,
    regista_id INT,
    genere_id INT,
    FOREIGN KEY (regista_id) REFERENCES Regista(id),
    FOREIGN KEY (genere_id) REFERENCES Genere(id)
);

-- ==========================
-- TABELLA: Film_Piattaforma
-- ==========================
CREATE TABLE Film_Piattaforma (
    id INT AUTO_INCREMENT PRIMARY KEY,
    film_id INT,
    piattaforma_id INT,
    FOREIGN KEY (film_id) REFERENCES Film(id),
    FOREIGN KEY (piattaforma_id) REFERENCES Piattaforma(id)
);