from flask import Flask, request
import pickle
import pandas as pd

app = Flask(__name__)

with open('crop_model.pkl', 'rb') as f:
    model = pickle.load(f)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crop Yield Prediction</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-image: url('/static/images/farming-image.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
        }
        h1 { color: #667eea; text-align: center; margin-bottom: 30px; font-size: 28px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; color: #333; font-weight: 600; }
        input, select {
            width: 100%; padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px; font-size: 14px;
        }
        input:focus, select:focus { outline: none; border-color: #667eea; }
        button {
            width: 100%; padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; border: none; border-radius: 8px;
            font-size: 16px; font-weight: 600; cursor: pointer;
        }
        button:hover { opacity: 0.9; }
        .result {
            margin-top: 30px; padding: 20px;
            background: #f0f4ff; border-radius: 8px; text-align: center;
        }
        .result h2 { color: #667eea; font-size: 20px; margin-bottom: 10px; }
        .result p { font-size: 32px; color: #333; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>&#127806; Crop Yield Prediction System</h1>
        <form method="POST" action="/predict">
            <div class="form-group">
                <label>Year</label>
                <input type="number" name="year" required min="1990" max="2030" value="2020">
            </div>
            <div class="form-group">
                <label>Country/Area</label>
                <input type="text" name="area" required placeholder="e.g., India">
            </div>
            <div class="form-group">
                <label>Crop Item</label>
                <select name="item" required>
                    <option value="Maize">Maize</option>
                    <option value="Potatoes">Potatoes</option>
                    <option value="Rice, paddy">Rice, paddy</option>
                    <option value="Sorghum">Sorghum</option>
                    <option value="Soybeans">Soybeans</option>
                    <option value="Wheat">Wheat</option>
                    <option value="Cassava">Cassava</option>
                    <option value="Sweet potatoes">Sweet potatoes</option>
                    <option value="Plantains and others">Plantains and others</option>
                    <option value="Yams">Yams</option>
                </select>
            </div>
            <div class="form-group">
                <label>Average Rainfall (mm/year)</label>
                <input type="number" step="0.01" name="rainfall" required placeholder="e.g., 1200.5">
            </div>
            <div class="form-group">
                <label>Pesticides (tonnes)</label>
                <input type="number" step="0.01" name="pesticides" required placeholder="e.g., 150.75">
            </div>
            <div class="form-group">
                <label>Average Temperature (°C)</label>
                <input type="number" step="0.01" name="temp" required placeholder="e.g., 25.5">
            </div>
            <button type="submit">Predict Yield</button>
        </form>
        {result_block}
    </div>
</body>
</html>"""

@app.route('/')
def home():
    return HTML.replace('{result_block}', '')

@app.route('/predict', methods=['POST'])
def predict():
    area = request.form['area']
    item = request.form['item']
    year = int(request.form['year'])
    rainfall = float(request.form['rainfall'])
    pesticides = float(request.form['pesticides'])
    temp = float(request.form['temp'])

    input_data = pd.DataFrame([{
        'Area': area, 'Item': item, 'Year': year,
        'average_rain_fall_mm_per_year': rainfall,
        'pesticides_tonnes': pesticides,
        'avg_temp': temp
    }])

    prediction = model.predict(input_data)[0]
    result = f"""
    <div class="result">
        <h2>Predicted Crop Yield</h2>
        <p>{round(prediction, 2)} hg/ha</p>
    </div>"""
    return HTML.replace('{result_block}', result)

if __name__ == '__main__':
    app.run(debug=False)
