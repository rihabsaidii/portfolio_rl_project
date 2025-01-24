# 1. Choisir une image de base (ici Python 3.9)
FROM python:3.9

# 2. Définir le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# 3. Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# 4. Installer les dépendances listées dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copier tout le contenu du dossier dashboards dans /app
COPY . .

# Exposer le port utilisé par l'application Dash
EXPOSE 8050

# 6. Commande par défaut pour lancer l'application
#CMD ["python", "app.py"]
CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]
