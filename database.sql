-- ==========================
-- TABELLA: Regista
-- ==========================
CREATE TABLE Regista (
    id INT AUTO_INCREMENT,  -- Identificatore univoco del regista (auto incrementato)
    nome VARCHAR(100) UNIQUE,           -- Nome completo del regista (univoco)
    eta INT,
    PRIMARY KEY (id)              -- Età attuale del regista
);

-- ==========================
-- TABELLA: Genere
-- ==========================
CREATE TABLE Genere (
    id INT AUTO_INCREMENT,  -- Identificatore univoco del genere (auto incrementato)
    nome VARCHAR(50),     
    PRIMARY KEY (id)               -- Nome del genere (es. Dramma, Fantascienza, ecc.)
);

-- ==========================
-- TABELLA: Piattaforma
-- ==========================
CREATE TABLE Piattaforma (
    id INT AUTO_INCREMENT,  -- Identificatore univoco della piattaforma (auto incrementato)
    nome VARCHAR(100) UNIQUE,
    PRIMARY KEY (id)            -- Nome della piattaforma (univoco)
);

-- ==========================
-- TABELLA: Film
-- ==========================
CREATE TABLE Film (
    id INT AUTO_INCREMENT,          -- Identificatore univoco del film (auto incrementato)
    titolo VARCHAR(255),                        -- Titolo del film
    anno INT,                                   -- Anno di uscita del film
    regista_id INT,                             -- Relazione: un film ha un solo regista
    genere_id INT,                              -- Relazione: un film ha un solo genere
    UNIQUE (titolo, anno),
    PRIMARY KEY (id),                      -- Un film con lo stesso titolo e anno è univoco
    FOREIGN KEY (regista_id) REFERENCES Regista(id), -- Relazione con la tabella Regista
    FOREIGN KEY (genere_id) REFERENCES Genere(id)    -- Relazione con la tabella Genere
);

-- ==========================
-- TABELLA: Film_Piattaforma
-- ==========================
CREATE TABLE Film_Piattaforma (
    id INT AUTO_INCREMENT,                 -- Identificatore univoco della riga (auto incrementato)
    film_id INT,                                       -- Film disponibile
    piattaforma_id INT,  
    PRIMARY KEY (id),                              -- Piattaforma su cui è disponibile
    FOREIGN KEY (film_id) REFERENCES Film(id),        -- Relazione con la tabella Film
    FOREIGN KEY (piattaforma_id) REFERENCES Piattaforma(id) -- Relazione con la tabella Piattaforma
);
