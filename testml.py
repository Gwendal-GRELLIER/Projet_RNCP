import tensorflow as tf
from tensorflow.keras import layers, models
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import mlflow
import mlflow.tensorflow

# Définir l'URI de MLflow à partir de la variable d'environnement MLFLOW_TRACKING_URI
mlflow_tracking_uri =  "http://0.0.0.0:5000"

# Charger le modèle MLflow en utilisant l'URI de suivi spécifié
mlflow.set_tracking_uri(mlflow_tracking_uri)
# Charge les données
data = pd.read_parquet("/workspaces/Projet_RNCP/Data_training/de_train.parquet")

# Sépare les caractéristiques (X) et les étiquettes de classe (y)
X = data[['cell_type', 'sm_name', 'sm_lincs_id', 'control', 'SMILES']]
y = data.drop(columns=['cell_type', 'sm_name', 'sm_lincs_id', 'control', 'SMILES'])

# Encodage one-hot pour toutes les colonnes catégoriques
categorical_columns = ['cell_type', 'sm_name', 'sm_lincs_id', 'control', 'SMILES']
X_encoded = pd.get_dummies(X[categorical_columns], drop_first=True)

# Fusionne les données encodées avec les données originales
X = pd.concat([X.drop(categorical_columns, axis=1), X_encoded], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Applique le prétraitement sur les ensembles d'entraînement et de test
X_train_processed = X_train
X_test_processed = X_test

logged_model = 'runs:/50c428d16b5e403fbd9c4ba76219adcc/NN_classic_base'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)

# Predict on a Pandas DataFrame.

print(loaded_model.predict(pd.DataFrame(X_test)))
