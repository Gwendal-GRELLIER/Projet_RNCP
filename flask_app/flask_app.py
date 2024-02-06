from flask import Flask, render_template, request
import numpy as np
import mlflow.pyfunc

app = Flask(__name__)

# Chargement du modèle pré-entrainé à partir de MLflow
def load_mlflow_model(model_uri):
    mlflow_model = mlflow.pyfunc.load_model(model_uri)
    return mlflow_model

model_uri = "your_model_uri_here"  # Remplacez "your_model_uri_here" par l'URI de votre modèle MLflow
model = load_mlflow_model(model_uri)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        features = [float(x) for x in request.form.values()]
        features = np.array(features).reshape(1, -1)
        prediction = model.predict(features)
        return render_template('index.html', prediction_text='Le résultat de la prédiction est {}'.format(prediction[0]))

if __name__ == '__main__':
    app.run(debug=True)
