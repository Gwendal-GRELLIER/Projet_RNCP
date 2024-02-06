# Utilisez l'image Docker officielle de MLflow
FROM python:3.8

# Installez MLflow
RUN pip install mlflow

# Exposez le port sur lequel le serveur MLflow fonctionnera
EXPOSE 5000

# Commande pour démarrer le serveur MLflow
CMD ["mlflow", "server", "--host", "0.0.0.0"]
