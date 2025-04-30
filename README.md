# 🎬 Sistema Web Interattivo per la Gestione di Film

> **Progetto di Alessandro Arellano**  
> Università degli Studi di Roma  
> 📧 arellanoaltuna.2050207@studenti.uniroma1.it

---

## 📌 Introduzione

Il progetto consiste nello sviluppo di un'applicazione **web interattiva** per la gestione e consultazione di un database di film, con:

- Importazione di dati da file TSV o CSV
- Interrogazioni in linguaggio naturale (NLQ ➝ SQL)
- Visualizzazione dinamica dello schema del database

L'app è costruita su un'architettura **modulare e moderna**:

- ⚙️ Backend: **FastAPI (Python)**
- 💻 Frontend: **React + Bootstrap**

---

## ⚙️ Tecnologie Utilizzate

| Componente | Tecnologia              |
|------------|--------------------------|
| Backend    | Python + FastAPI         |
| Frontend   | React + React-Bootstrap  |
| Database   | MariaDB                  |
| ORM        | SQLAlchemy               |
| Librerie   | Pydantic, Pandas         |

---

## 🚀 Funzionalità del Sistema

### 📂 1. Importazione Dati

- `POST /inserimento-tsv` → importa un file TSV
- `POST /add` → inserisce una singola riga CSV

🛡️ Controlli anti-duplicati per:
- Film: `titolo + anno`
- Registi: `nome`
- Generi e piattaforme

---

### 🧠 2. Interrogazioni in Linguaggio Naturale

`GET /search/{question}`  
Domande supportate:

- "Elenca i film del 2020"
- "Quali sono i registi presenti su Netflix?"
- "Tutti i film di fantascienza"

🔁 Il backend converte dinamicamente la domanda in una query SQL.

---

### 🧩 3. Visualizzazione dello Schema

- `GET /schema/summary`  
Mostra tutte le tabelle, colonne e relazioni presenti nel database.

---

## 🗃️ Struttura del Database

**Tabelle principali:**

- `Film(id, titolo, anno, regista_id, genere_id)`
- `Regista(id, nome, eta)`
- `Genere(id, nome)`
- `Piattaforma(id, nome)`
- `Film_Piattaforma(id, film_id, piattaforma_id)`

**Relazioni:**

- 1:N tra `Film` → `Regista` e `Genere`
- N:N tra `Film` e `Piattaforma` (via `Film_Piattaforma`)

---

## 🎨 Frontend: React + Bootstrap

### 📋 Funzionalità principali

- Form per invio domande testuali (NLQ)
- Inserimento manuale di righe CSV
- Visualizzazione dinamica della struttura del database

### 🧭 Dashboard Principale

Il componente `Dashboard.js` utilizza **Tabs** per tre viste:

1. 🔍 **Search** – interrogazione testuale
2. ➕ **Add** – inserimento nuovo film
3. 🧬 **Get Schema** – visualizza schema database

---

## 💻 Esempi di Codice Frontend

### 🔎 Interrogazione Naturale

```javascript
const inviaDomanda = async (e) => {
  e.preventDefault();
  const response = await fetch(
    `http://127.0.0.1:8005/search/${encodeURIComponent(messaggio)}`
  );
  const data = await response.json();
  setNomiRegisti(data.map(item => item.nome));
};
