# Utiliser l'image NiFi provenant de Docker Hub (utilise l'utilisateur nifi !!)
FROM apache/nifi:1.23.2

# Revenir à l'utilisateur racine (nécessaire pour certaines commandes ci-dessous)
USER root

# Mettre à jour et installer Python 3, pip et dos2unix
RUN apt-get update && apt-get install -y python3 python3-pip dos2unix

# Installer le module boto3
RUN pip3 install boto3

# Installer les modules pandas et pyarrow
RUN pip3 install pandas pyarrow

# Afficher le chemin de l'interpréteur Python
RUN which python3

# Copier les scripts Python et le fichier de configuration dans l'image
COPY ./scripts /opt/nifi/rncp_files
COPY ./config.json /opt/nifi/rncp_files

# Convertir les scripts au format Unix
RUN dos2unix /opt/nifi/rncp_files/*

# Rendre les scripts exécutables
RUN chmod +x /opt/nifi/rncp_files/*

# Définir la variable d'environnement pour le port HTTP de NiFi
ENV NIFI_WEB_HTTP_PORT 8080

# Revenir à l'utilisateur nifi pour la sécurité
USER nifi