# Importer les modules nécessaires
import boto3
import json
from kafka import KafkaConsumer
import os

# Récupérer les clés d'accès depuis les variables d'environnement
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Créer un client pour DynamoDB
client = boto3.client(
    'dynamodb',
    region_name='eu-west-1',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Créer une table Dynamodb avec le nom, la clé primaire et le type de la clé
try:
    table = client.create_table(
        TableName='dataset',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    # Attendre que la table soit créée
    table.wait_until_exists()
except Exception as e:
    # Afficher ou logger l'erreur
    print(e)

# Créer un consommateur Kafka pour lire les messages du topic 'dataset'
consumer = KafkaConsumer('dataset', bootstrap_servers=['localhost:9092'])

# Parcourir les messages du topic
for message in consumer:
    # Décoder le message en format json
    data = json.loads(message.value)
    # Extraire l'id et le contenu du fichier
    id = data['id']
    content = data['content']
    # Insérer les données dans la table Dynamodb
    try:
        table.put_item(
            Item={
                'id': id,
                'content': content
            }
        )
    except Exception as e:
        # Afficher ou logger l'erreur
        print(e)
