from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from auth import login_required, get_google_auth_url, get_google_user
from sheets import get_or_create_user_sheet, add_transaction, get_transactions

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure key

@app.route("/")
@login_required
def index():
    """Dashboard displaying user transactions from Google Sheets."""
    email = session["email"]
    sheet_id = get_or_create_user_sheet(email)
    transactions = get_transactions(sheet_id)
    return render_template("index.html", transactions=transactions, user=session["name"])

@app.route("/login")
def login():
    """Redirect user to Google OAuth login."""
    return redirect(get_google_auth_url())

@app.route("/logout")
def logout():
    """Logout user and clear session."""
    session.clear()
    return redirect(url_for("index"))

@app.route("/auth/callback")
def auth_callback():
    """Handles Google OAuth callback."""
    get_google_user()
    return redirect(url_for("index"))

@app.route("/transactions", methods=["GET", "POST"])
@login_required
def transactions():
    email = session["email"]
    sheet_id = get_or_create_user_sheet(email)

    if request.method == "POST":
        data = request.json
        add_transaction(sheet_id, data)
        return jsonify({"message": "Transaction added successfully!"})

    transactions = get_transactions(sheet_id)
    return jsonify(transactions)


if __name__ == "__main__":
    app.run(debug=True)
