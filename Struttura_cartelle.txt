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
