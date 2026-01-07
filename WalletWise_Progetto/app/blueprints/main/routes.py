from functools import wraps
from flask import render_template, request, redirect, url_for, session, flash, current_app
from . import main_bp
from ...repositories.transaction_repositories import TransactionRepository
from ...repositories.category_repositories import CategoryRepository

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login_page"))
        return view(*args, **kwargs)
    return wrapped

def tx_repo():
    return TransactionRepository(current_app.config["DB_PATH"])

def cat_repo():
    return CategoryRepository(current_app.config["DB_PATH"])

@main_bp.get("/")
def home():
    return redirect(url_for("main.dashboard"))

# L3: pagina riepilogo + filtro date
@main_bp.get("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]

    start = request.args.get("start", "").strip() or None
    end = request.args.get("end", "").strip() or None

    transactions = tx_repo().list_for_user(user_id, start, end)
    income, expense = tx_repo().totals_for_user(user_id, start, end)

    return render_template(
        "main/dashboard.html",
        username=session.get("username", ""),
        transactions=transactions,
        income=income,
        expense=expense,
        balance=income - expense,
        start=start or "",
        end=end or ""
    )

# L1+L2: inserimento movimento con categoria
@main_bp.get("/add")
@login_required
def add_page():
    categories = cat_repo().list_all()
    return render_template("main/add_transaction.html", categories=categories)

@main_bp.post("/add")
@login_required
def add_action():
    user_id = session["user_id"]

    tx_type = request.form.get("type", "")
    description = request.form.get("description", "").strip()
    amount_s = request.form.get("amount", "").strip()
    date = request.form.get("date", "").strip()
    category_id_s = request.form.get("category_id", "").strip()

    if tx_type not in ("income", "expense"):
        flash("Tipo non valido.")
        return redirect(url_for("main.add_page"))

    if not description or not date or not category_id_s:
        flash("Compila tutti i campi.")
        return redirect(url_for("main.add_page"))

    try:
        amount = float(amount_s)
        if amount < 0:
            raise ValueError
        category_id = int(category_id_s)
    except ValueError:
        flash("Importo o categoria non validi.")
        return redirect(url_for("main.add_page"))

    # Verifica categoria esistente (L2)
    if not cat_repo().get_by_id(category_id):
        flash("Categoria non valida.")
        return redirect(url_for("main.add_page"))

    tx_repo().add(user_id, category_id, tx_type, description, amount, date)
    return redirect(url_for("main.dashboard"))
