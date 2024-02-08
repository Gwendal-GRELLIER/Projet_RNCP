from flask import Flask, request, jsonify
import mlflow.pyfunc
import pandas as pd
from flask import render_template
import os



app = Flask(__name__, template_folder='templates')


# Définir l'URI de MLflow à partir de la variable d'environnement MLFLOW_TRACKING_URI
mlflow_tracking_uri =  "http://0.0.0.0:5000"

# Charger le modèle MLflow en utilisant l'URI de suivi spécifié
mlflow.set_tracking_uri(mlflow_tracking_uri)
logged_model = 'runs:/0284e699ee3b466fa80ce8391a8d9967/NN_classic_base_final'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)


@app.route('/')
def index():
    return render_template('index.html')

# Endpoint pour effectuer les prédictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Vérifiez si un fichier a été envoyé
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        # Obtenez le fichier envoyé
        file = request.files['file']

        # Assurez-vous que le fichier est bien un fichier JSON
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        # Charger les données JSON à partir du fichier
        #data = file.read()
        print("Received data:", file)  # Ajoutez cette ligne pour débogage
        
        # Convertir les données JSON en DataFrame ou en format compatible avec votre modèle
        # Par exemple, si vous utilisez Pandas pour charger le fichier JSON :
        
        df = pd.read_json(file)
        #df = pd.DataFrame(data)
        
        
        
        print("DataFrame:", df)  # Ajoutez cette ligne pour débogage
        # Effectuer la prédiction sur les données
        predictions = loaded_model.predict(df)

        print(predictions)
        # Convertir les prédictions en JSON
        predictions_json = predictions.to_json(orient='values')

        # Renvoyer les prédictions au format JSON
        return jsonify({'predictions': predictions_json})

    except Exception as e:
        return jsonify({'error': str(e)})




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

