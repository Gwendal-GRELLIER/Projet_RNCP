#!/usr/bin/env python3

import boto3
import csv
import json
import sys

# Charger la configuration depuis le fichier config.json
with open('/opt/nifi/rncp_files/config.json', 'r') as config_file:
    config = json.load(config_file)

# Récupérer les informations de connexion AWS
AWS_REGION = config['region_name']
AWS_ACCESS_KEY_ID = config['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = config['aws_secret_access_key']

# Lire le nom du fichier à partir du flux NiFi
file_name = sys.argv[1]

# Supprimer l'extension .csv du nom du fichier pour créer le nom de la table
table_name = file_name.split(".csv")[0]

# Créer un client DynamoDB
dynamodb = boto3.client("dynamodb", region_name=AWS_REGION,
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# Créer la table DynamoDB (si elle n'existe pas déjà)
try:
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "location", "KeyType": "HASH"},  # Clé primaire
            {"AttributeName": "gene_id", "KeyType": "RANGE"}  # Clé de tri
        ],
        AttributeDefinitions=[
            {"AttributeName": "location", "AttributeType": "S"},  # Attribut location de type chaîne
            {"AttributeName": "gene_id", "AttributeType": "S"}  # Attribut gene_id de type chaîne
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 25,
            "WriteCapacityUnits": 25
        }
    )
except dynamodb.exceptions.ResourceInUseException:
    pass

# Attendre que la table soit disponible
dynamodb_resource = boto3.resource("dynamodb", region_name=AWS_REGION,
                                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
table = dynamodb_resource.Table(table_name)
table.wait_until_exists()

# Lire le fichier CSV et insérer les données dans DynamoDB
reader = csv.DictReader(sys.stdin)
nombre_lignes = 0
for row in reader:
    item = {
        "location": {'S': row["location"]},
        "gene_id": {'S': row["gene_id"]},
        "feature_type": {'S': row["feature_type"]},
        "genome": {'S': row["genome"]},
        "interval": {'S': row["interval"]}
    }

    dynamodb.put_item(TableName=table_name, Item=item)

    nombre_lignes += 1

print(f"Les {nombre_lignes} lignes du fichier {file_name} ont été insérées dans la table {table_name} de DynamoDB.")