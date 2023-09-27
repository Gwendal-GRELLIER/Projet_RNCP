# Importer les modules nécessaires
from pyspark.sql import SparkSession
import os



# Initialiser une session Spark
spark = SparkSession.builder.appName("Exploration de Dataset").getOrCreate()
# Spécifiez le chemin du dossier que vous souhaitez explorer
dossier = "/workspaces/Projet_RNCP/downloads"

# Utilisez os.listdir pour obtenir la liste des fichiers dans le dossier
fichiers = os.listdir(dossier)

# Parcourez la liste des fichiers et affichez leurs noms
for fichier in fichiers:
    
    # Charger un fichier CSV dans un DataFrame
    data_path = f"/workspaces/Projet_RNCP/downloads/{fichier}"
    nom_fichier, extension = os.path.splitext(fichier)
    
    # Vérifiez si l'extension est .csv ou .parquet et affichez le nom du fichier
    if extension.lower() == ".csv" :
        df = spark.read.csv(data_path, header=True, inferSchema=True)
        print("Afficher les premières lignes du DataFrame :")
        df.show(5)

    elif extension.lower() == ".parquet":
        df = spark.read.parquet(data_path, header=True, inferSchema=True)
        print("Afficher les premières lignes du DataFrame :")
        df.show(5)

  


# # Afficher le schéma du DataFrame
# print("Schéma du DataFrame :")
# df.printSchema()

# # Afficher les statistiques sommaires des colonnes numériques
# print("Statistiques sommaires des colonnes numériques :")
# df.describe().show()

# # Compter le nombre total de lignes dans le DataFrame
# print("Nombre total de lignes dans le DataFrame :")
# print(df.count())

# # Filtrer les données pour ne montrer que les lignes répondant à une condition
# filtered_df = df.filter(df['age'] > 30)
# print("Nombre de lignes où l'âge est supérieur à 30 :")
# print(filtered_df.count())

# # Regrouper les données par une colonne et effectuer une opération d'agrégation
# grouped_df = df.groupBy("genre").agg({"revenu": "mean", "age": "max"})
# print("Revenu moyen et âge maximum par genre :")
# grouped_df.show()

# Fermer la session Spark
spark.stop()
