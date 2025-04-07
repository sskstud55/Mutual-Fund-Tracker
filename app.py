from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from auth import login_required, get_google_auth_url, get_google_user
from sheets import get_or_create_user_sheet, add_transaction, get_transactions
from config import Config #import config class.

app = Flask(__name__)
app.config.from_object(Config) #use config class.

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
    """Handle displaying and adding transactions."""
    email = session["email"]
    sheet_id = get_or_create_user_sheet(email)

    if request.method == "POST":
        try:
            data = request.json
            add_transaction(sheet_id, data)
            return jsonify({"message": "Transaction added successfully!"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500 #return error.

    # GET method: Retrieve transactions from the sheet
    transactions1 = get_transactions(sheet_id)
    return render_template("transactions.html", transactions=transactions1, user=session["name"])

if __name__ == "__main__":
    app.run(debug=True)