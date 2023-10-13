import boto3
import os
from kafka import KafkaConsumer

# Configuration AWS S3
aws_access_key_id = 'fill-here'
aws_secret_access_key = 'fill-here'
s3_bucket_name = 's3-rncp-project-bucket'
s3_prefix = 'test'  # Optionnel

# Kafka bootstrap servers
bootstrap_servers = ['localhost:9092']

# Topic Kafka
topic = 'file-stream'

# Création d'un consumer Kafka
consumer = KafkaConsumer(topic,
                         bootstrap_servers=bootstrap_servers)

# Créer un client S3
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

for message in consumer:
   
    file_content = message.value
    print(file_content)
    # Déterminer le nom du fichier à partir de la clé Kafka, ou utilisez un nom de fichier généré
    file_name = 'nom-de-fichier-de-kafka'  # Remplacez par la logique pour extraire le nom du fichier

    # Envoyer le contenu du fichier vers S3
    s3_object_key = os.path.join(s3_prefix, file_name) if s3_prefix else file_name
    
    # Ajouter un compteur et une valeur maximale pour les tentatives de connexion
    max_attempts = 10
    attempts = 0
    
    while True:
        try:
            s3_client.put_object(Bucket=s3_bucket_name, Key=s3_object_key, Body=file_content)
            print(f"File '{file_name}' uploaded to S3")
            break # Sortir de la boucle si la connexion réussit
        except Exception as e: # Remplacer Exception par quelque chose de plus spécifique
            attempts += 1 # Incrémenter le compteur
            if attempts >= max_attempts: # Vérifier si le compteur atteint la valeur maximale
                print(f"Failed to upload file '{file_name}' to S3 after {max_attempts} attempts")
                print(e) # Afficher l'exception
                break # Sortir de la boucle si le compteur atteint la valeur maximale
            else:
                print(f"Retrying to upload file '{file_name}' to S3")
                continue # Continuer la boucle si le compteur n'atteint pas la valeur maximale

consumer.close()
