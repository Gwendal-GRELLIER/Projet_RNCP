#!/usr/bin/env python3

import boto3
import csv
import sys

# Informations de connexion AWS
AWS_ACCESS_KEY_ID = "AKIARO7QSX7O3KCKTIML"
AWS_SECRET_ACCESS_KEY = "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"
AWS_REGION = "us-east-1"

# Lisez le nom du fichier à partir du flux NiFi
file_name = sys.argv[1]

# Supprimez l'extension .csv du nom du fichier pour créer le nom de la table
table_name = file_name.split(".csv")[0]

# Créez un client DynamoDB
dynamodb = boto3.client("dynamodb", region_name=AWS_REGION,
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# Créez la table DynamoDB (si elle n'existe pas déjà)
try:
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "obs_id", "KeyType": "HASH"}  # Clé primaire
        ],
        AttributeDefinitions=[
            {"AttributeName": "obs_id", "AttributeType": "S"},  # Attribut obs_id de type chaîne
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 25,
            "WriteCapacityUnits": 25
        }
    )
except dynamodb.exceptions.ResourceInUseException:
    pass

# Attendez que la table soit disponible
dynamodb_resource = boto3.resource("dynamodb", region_name=AWS_REGION,
                                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
table = dynamodb_resource.Table(table_name)
table.wait_until_exists()

# Lisez le fichier CSV et insérez les données dans DynamoDB en lots
batch_size = 25  # Nombre d'éléments à insérer par lot
batch = []
nombre_lignes = 0

def insert_batch(batch):
    dynamodb.batch_write_item(
        RequestItems={
            table_name: batch
        }
    )

reader = csv.DictReader(sys.stdin)
for row in reader:
    item = {
        "PutRequest": {
            "Item": {
                "obs_id": {'S': row["obs_id"]},
                "cell_type": {'S': row["cell_type"]},
                "donor_id": {'S': row["donor_id"]}
            }
        }
    }

    batch.append(item)
    nombre_lignes += 1

    if len(batch) == batch_size:
        insert_batch(batch)
        batch = []

# Insérer les éléments restants s'il en reste
if batch:
    insert_batch(batch)

print(f"Les {nombre_lignes} lignes du fichier {file_name} ont été insérées dans la table {table_name} de DynamoDB.")