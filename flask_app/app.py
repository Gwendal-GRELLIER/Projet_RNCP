<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MLflow Flask App</title>
</head>
<body>
    <h1>MLflow Flask App</h1>
    <form id="prediction-form">
        <label for="feature1">Feature 1:</label>
        <input type="number" id="feature1" name="feature1" required><br><br>
        <label for="feature2">Feature 2:</label>
        <input type="number" id="feature2" name="feature2" required><br><br>
        <button type="submit">Predict</button>
    </form>
    <div id="prediction-result"></div>

    <script>
        document.getElementById('prediction-form').addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(this);
            fetch('/predict', {
                method: 'POST',
                body: JSON.stringify(Object.fromEntries(formData)),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('prediction-result').innerText = 'Predicted output: ' + data.predictions;
            });
        });
    </script>
</body>
</html>
