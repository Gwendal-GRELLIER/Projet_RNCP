from kafka import KafkaProducer
import os

# Serveurs Kafka bootstrap
bootstrap_servers = ['localhost:9092']

# Topic Kafka pour produire des données
topic = 'file-stream'

# Création d'un producer Kafka
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

# Chemin vers le répertoire contenant les fichiers à envoyer
local_directory = '/workspaces/Projet_RNCP/testdir'

# Lister les fichiers dans le répertoire
files = os.listdir(local_directory)

for file_name in files:
    # Construire le chemin complet du fichier
    file_path = os.path.join(local_directory, file_name)

    with open(file_path, 'rb') as file:
        # Lire le contenu du fichier
        file_content = file.read()

        # Publier le contenu du fichier dans Kafka
        producer.send(topic, value=file_content)

        print(f"File '{file_name}' sent to Kafka")

producer.close()



# from kafka import KafkaProducer
# from time import sleep
# import requests
# import json


# Serveurs Kafka bootstrap
#bootstrap_servers = ['localhost:9092']

# Topic Kafka pour produire des données
#topic = 'data-stream'

# Création d'un producer Kafka
# producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
#                          value_serializer=lambda m: json.dumps(m).encode('utf-8'))

                
# # Convertir le dictionnaire en JSON et l'envoyer à Kafka
# producer.send(topic, value=price_data)

# print("Price data sent to Kafka")
        
