# Utiliser l'image NiFi provenant de Docker Hub (utilise l'utilisateur nifi !!)
FROM apache/nifi:1.23.2

# Revenir à l'utilisateur racine (nécessaire pour les lignes 8 et 20)
USER root

# Mettre à jour et installer Python 3 et pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Installer le module boto3
RUN pip3 install boto3

# Afficher le chemin de l'interpréteur Python
RUN which python3

# Copier les scripts Python dans l'image
COPY ./scripts /opt/nifi/python_scripts

# Rendre les scripts exécutables
RUN chmod +x /opt/nifi/python_scripts/*

# Définir la variable d'environnement pour le port HTTP de NiFi
ENV NIFI_WEB_HTTP_PORT 8080

# Revenir à l'utilisateur nifi pour la sécurité
USER nifi