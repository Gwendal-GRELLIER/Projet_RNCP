#!/usr/bin/env python3

import sys
import io
import pandas as pd

# Lire les données brutes à partir de l'entrée standard (stdin)
input_data = sys.stdin.buffer.read()

# Convertir les données brutes en DataFrame Pandas
parquet_df = pd.read_parquet(io.BytesIO(input_data))

# Renommer les colonnes en remplaçant les caractères spéciaux
parquet_df.columns = [col.replace("-", "___").replace(".", "__").replace("/", "____") for col in parquet_df.columns]

# Spécifier la première et la dernière colonne dans la séquence que vous voulez convertir
start_column = 'cell_type'
end_column = 'SMILES'

# Sélectionner les colonnes entre start_column et end_column (inclus)
columns_to_convert = parquet_df.loc[:, start_column:end_column].columns

# Changer le type de données des colonnes
parquet_df[columns_to_convert] = parquet_df[columns_to_convert].astype('string')
parquet_df['control'] = parquet_df['control'].astype('boolean')

# Écrire les résultats sur la sortie standard (stdout)
sys.stdout.buffer.write(parquet_df.to_parquet())

# Assurez-vous de vider le buffer de sortie pour s'assurer que toutes les données sont écrites
sys.stdout.flush()