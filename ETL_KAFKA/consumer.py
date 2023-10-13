import boto3
import os

# Configuration AWS S3
aws_access_key_id = 'AKIA6K2ESKF7JSDV5ZHP'
aws_secret_access_key = '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'
s3_bucket_name = 's3-rncp-project-bucket'
s3_prefix = 'test'  # Optionnel

# Créer un client S3
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

for message in consumer:
    file_content = message.value

    # Déterminer le nom du fichier à partir de la clé Kafka, ou utilisez un nom de fichier généré
    file_name = 'nom-de-fichier-de-kafka'  # Remplacez par la logique pour extraire le nom du fichier

    # Envoyer le contenu du fichier vers S3
    s3_object_key = os.path.join(s3_prefix, file_name) if s3_prefix else file_name
    s3_client.put_object(Bucket=s3_bucket_name, Key=s3_object_key, Body=file_content)

    print(f"File '{file_name}' uploaded to S3")

consumer.close()