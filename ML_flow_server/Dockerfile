# Utilisez l'image Docker officielle de MLflow
FROM python:3.8

# Installez MLflow
RUN pip install mlflow

# Créez le groupe et l'utilisateur docker
RUN groupadd -r docker && useradd -r -g docker docker

# Créez le dossier /data/ et changez son propriétaire et ses droits
RUN mkdir /data/ && chown docker:docker /data/ && chmod 755 /data/

# Exposez le port sur lequel le serveur MLflow fonctionnera
EXPOSE 5000

# Changez d'utilisateur
USER docker

# Commande pour démarrer le serveur MLflow
CMD ["mlflow", "server", "--host", "0.0.0.0", "--backend-store-uri", "/data/", "--default-artifact-root", "/data/"]

