import webbrowser
from flask import Flask, render_template, redirect, url_for, session, request, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from database import UserDatabase  # Assurez-vous que ce fichier est dans le même répertoire

app = Flask(__name__, template_folder='template', static_folder='static')
app.secret_key = 'votre_clé_secrète'

# Créer une instance de la base de données
user_db = UserDatabase()

# Décorateur pour vérifier le rôle de l'utilisateur
def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session or session['user_role'] != role:
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@app.route('/')
def index():
    return render_template('accueil.html')  # Modifié pour pointer vers la bonne page d'accueil

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = user_db.get_user(username)  # Méthode à créer dans UserDatabase
        if user and check_password_hash(user['password'], password):
            session['user_role'] = user['role']
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', role=session.get('user_role'))

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        
        # Vérifier si les mots de passe correspondent
        if password != password_confirm:
            return render_template('inscription.html', erreur="Les mots de passe ne correspondent pas.")
        
        # Essayer d'insérer l'utilisateur dans la base de données
        if user_db.insert_user(username, password):
            return redirect(url_for('index'))  # Rediriger vers la page d'accueil après l'inscription
        else:
            return render_template('inscription.html', erreur="Ce nom d'utilisateur est déjà pris.")

    return render_template('inscription.html')  # Afficher le formulaire d'inscription

@app.route('/public_stats')
@role_required('public')
def public_stats():
    # Logique pour afficher les statistiques publiques
    return render_template('public_stats.html')

@app.route('/sports_betting')
@role_required('parieur')
def sports_betting():
    # Logique pour les paris sportifs
    return render_template('sports_betting.html')

@app.route('/federation')
@role_required('federation')
def federation():
    # Logique pour la gestion des clubs
    return render_template('federation.html')

@app.route('/api/stats')
def get_stats():
    # Logique pour retourner les statistiques en format JSON
    return jsonify(stats={})

@app.route('/api/news')
def get_news():
    # Logique pour retourner les actualités
    return jsonify(news=[])

@app.route('/api/bets', methods=['POST'])
def place_bet():
    # Logique pour placer un pari
    return jsonify(success=True)

@app.route('/tuto_app')
def tuto_app():
    return send_file('Tuto_application.pdf', as_attachment=False)

@app.route('/tuto_xls')
def tuto_xls():
    return send_file('Tuto_fichiers_xls.pdf', as_attachment=False)

if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:5500')
    app.run(debug=True, port=5500)