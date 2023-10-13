import boto3
import os

# Configuration AWS S3
aws_access_key_id = 'fill-here'
aws_secret_access_key = 'fill-here'
s3_bucket_name = 's3-rncp-project-bucket'
#s3_prefix = 'test'  # Optionnel

# Créer un client S3
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Chemin vers le répertoire contenant les fichiers à envoyer
local_directory = '/workspaces/Projet_RNCP/downloads'

# Lister les fichiers dans le répertoire
files = os.listdir(local_directory)

for file_name in files:
    local_file_path = os.path.join(local_directory, file_name)

    # Lire le contenu du fichier
    with open(local_file_path, 'rb') as file_content:
        # Envoyer le contenu complet du fichier en tant que corps de l'objet S3
        s3_client.put_object(Bucket=s3_bucket_name, Key=file_name, Body=file_content)
