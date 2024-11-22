import webbrowser
from flask import Flask, request, render_template, redirect, url_for, session, Blueprint
from database import UserDatabase  # Assurez-vous que ce fichier est dans le même répertoire
from werkzeug.security import generate_password_hash

form = Blueprint('form', __name__, template_folder='template', static_folder='static')

# Créer une instance de la base de données
user_db = UserDatabase()


# Route pour le traitement des résultats du formulaire d'inscription
@form.route('/inscription', methods=['GET', 'POST'])
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
            return redirect(url_for('form.index'))  # Rediriger vers la page d'accueil après l'inscription
        else:
            return render_template('inscription.html', erreur="Ce nom d'utilisateur est déjà pris.")

    return render_template('inscription.html')  # Afficher le formulaire d'inscription

@form.route('/accueil')
def acceuil():
    return render_template('accueil.html')

if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:5000')