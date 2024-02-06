# import subprocess

# # Liste des dépendances à installer
# dependencies = ['tensorflow', 'pandas', 'scikit-learn', 'mlflow']

# # Installe chaque dépendance
# for package in dependencies:
#     subprocess.check_call(["pip", "install", package])



import tensorflow as tf
from tensorflow.keras import layers, models
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import mlflow
import mlflow.tensorflow

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

#print(X.head)




# Prétraitement des données
def preprocess_data(X):
    # Normalisation des caractéristiques numériques
    scaler = StandardScaler()
    numerical_columns = y.select_dtypes(include='number').columns
    X[numerical_columns] = scaler.fit_transform(X[numerical_columns])

    return X

# Applique le prétraitement sur les ensembles d'entraînement et de test
#X_train_processed = preprocess_data(X_train)
#X_test_processed = preprocess_data(X_test)
# Divise les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Applique le prétraitement sur les ensembles d'entraînement et de test
X_train_processed = X_train
X_test_processed = X_test
# Création du modèle
model = models.Sequential()
model.add(layers.Dense(128, activation='relu', input_shape=(X_train_processed.shape[1],)))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(18211, activation='linear'))  # Utilisez une activation linéaire pour la régression


# Démarrez une session MLflow
mlflow.set_tracking_uri("/local/path:/data/")  # URI du serveur MLflow 
mlflow.set_experiment("Deep_learning")

import mlflow.tensorflow

with mlflow.start_run(run_name='NN_classic_default'):
    # Log des hyperparamètres
    mlflow.log_param("optimizer", "adam")
    mlflow.log_param("epochs", 10)
    mlflow.log_param("batch_size", None)  # Remplacez None par la valeur que vous utilisez

    # Compiler le modèle
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    # Entraîner le modèle
    history = model.fit(X_train_processed, y_train, epochs=10, validation_data=(X_test_processed, y_test))

    # Enregistrer les métriques
    mlflow.log_metric("train_loss", history.history['loss'][-1])
    mlflow.log_metric("train_mae", history.history['mae'][-1])
    mlflow.log_metric("val_loss", history.history['val_loss'][-1])
    mlflow.log_metric("val_mae", history.history['val_mae'][-1])

    # Enregistrer le modèle
    mlflow.tensorflow.log_model(model, "NN_classic_base")

# Arrête le run en cours
mlflow.end_run()

