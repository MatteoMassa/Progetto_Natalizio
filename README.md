# WalletWise – Gestione delle Spese Personali

## Introduzione

WalletWise è un progetto di sviluppo web realizzato come primo lavoro individuale durante le vacanze di Natale.  
L’obiettivo del progetto è mettere in pratica le competenze acquisite nei primi moduli del corso, in particolare:

- progettazione del database (modello ER e normalizzazione)
- sviluppo backend con Python e Flask
- utilizzo del Repository Pattern
- gestione delle sessioni e sicurezza di base
- utilizzo di template dinamici con Jinja2

L’applicazione simula un semplice software di contabilità domestica che consente di gestire entrate e uscite personali.

---

## Funzionalità implementate

### L1 – Inserimento Entrate/Uscite
L’utente può inserire un movimento specificando:
- tipo (entrata o uscita)
- descrizione
- importo
- data
- categoria

### L2 – Categorie
Le spese sono suddivise per categoria.  
Le categorie principali richieste sono:
- Cibo
- Svago
- Trasporti  

Le categorie sono memorizzate in una tabella separata del database e collegate ai movimenti tramite chiave esterna.

### L3 – Riepilogo e filtro per data
È presente una dashboard che mostra:
- totale delle entrate
- totale delle uscite
- saldo finale  

È inoltre possibile filtrare i movimenti tramite un intervallo di date.

---

## Progettazione del Database

### Modello ER

Entità principali:
- **User**
- **Category**
- **Transaction**

Relazioni:
- Un utente può avere più movimenti (1:N)
- Una categoria può essere associata a più movimenti (1:N)

### Normalizzazione
- **Prima Forma Normale (1NF)**: tutti gli attributi sono atomici
- **Seconda Forma Normale (2NF)**: le tabelle hanno chiavi primarie semplici
- **Terza Forma Normale (3NF)**: le informazioni sulle categorie non sono duplicate nella tabella dei movimenti

---

walletwise/
│
├─ run.py
├─ config.py
├─ requirements.txt
│
└─ app/
   ├─ __init__.py
   ├─ db_init.py
   │
   ├─ repositories/
   │  ├─ __init__.py
   │  ├─ user_repository.py
   │  ├─ category_repository.py
   │  └─ transaction_repository.py
   │
   ├─ blueprints/
   │  ├─ __init__.py
   │  ├─ auth/
   │  │  ├─ __init__.py
   │  │  └─ routes.py
   │  └─ main/
   │     ├─ __init__.py
   │     └─ routes.py
   │
   └─ templates/
      ├─ base.html
      ├─ auth/
      │  ├─ login.html
      │  └─ register.html
      └─ main/
         ├─ dashboard.html
         └─ add_transaction.html
