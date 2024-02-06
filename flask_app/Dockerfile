# Utilisez une image de base avec Python
FROM python:3.8

# Copiez le code de votre application Flask dans le conteneur
COPY . /app
WORKDIR /app

# Installez les dépendances nécessaires
RUN pip install flask requests

# Exposez le port sur lequel votre application Flask fonctionnera
EXPOSE 5000

# Commande pour démarrer l'application Flask
CMD ["python", "flask_app.py"]