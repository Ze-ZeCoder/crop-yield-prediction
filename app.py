from flask import Flask, request
import pickle
import pandas as pd
import os

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
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 600px;
            width: 100%;
        }
        h1 { color: #667eea; text-align: center; margin-bottom: 30px; font-size: 28px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; color: #333; font-weight: 600; }
        input, select {
            width: 100%; padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px; font-size: 14px; transition: border 0.3s;
        }
        input:focus, select:focus { outline: none; border-color: #667eea; }
        button {
            width: 100%; padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; border: none; border-radius: 8px;
            font-size: 16px; font-weight: 600; cursor: pointer; transition: transform 0.2s;
        }
        button:hover { transform: translateY(-2px); }
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
                <label for="state">State</label>
                <select id="state" name="state" required>
                    <option value="">-- Select State --</option>
                    <option value="Andhra Pradesh">Andhra Pradesh</option>
                    <option value="Arunachal Pradesh">Arunachal Pradesh</option>
                    <option value="Assam">Assam</option>
                    <option value="Bihar">Bihar</option>
                    <option value="Chhattisgarh">Chhattisgarh</option>
                    <option value="Delhi">Delhi</option>
                    <option value="Goa">Goa</option>
                    <option value="Gujarat">Gujarat</option>
                    <option value="Haryana">Haryana</option>
                    <option value="Himachal Pradesh">Himachal Pradesh</option>
                    <option value="Jammu and Kashmir">Jammu and Kashmir</option>
                    <option value="Jharkhand">Jharkhand</option>
                    <option value="Karnataka">Karnataka</option>
                    <option value="Kerala">Kerala</option>
                    <option value="Madhya Pradesh">Madhya Pradesh</option>
                    <option value="Maharashtra">Maharashtra</option>
                    <option value="Manipur">Manipur</option>
                    <option value="Meghalaya">Meghalaya</option>
                    <option value="Mizoram">Mizoram</option>
                    <option value="Nagaland">Nagaland</option>
                    <option value="Odisha">Odisha</option>
                    <option value="Puducherry">Puducherry</option>
                    <option value="Punjab">Punjab</option>
                    <option value="Sikkim">Sikkim</option>
                    <option value="Tamil Nadu">Tamil Nadu</option>
                    <option value="Telangana">Telangana</option>
                    <option value="Tripura">Tripura</option>
                    <option value="Uttar Pradesh">Uttar Pradesh</option>
                    <option value="Uttarakhand">Uttarakhand</option>
                    <option value="West Bengal">West Bengal</option>
                </select>
            </div>
            <div class="form-group">
                <label for="crop">Crop</label>
                <select id="crop" name="crop" required>
                    <option value="">-- Select Crop --</option>
                    <option value="Arecanut">Arecanut</option>
                    <option value="Arhar/Tur">Arhar/Tur</option>
                    <option value="Bajra">Bajra</option>
                    <option value="Banana">Banana</option>
                    <option value="Barley">Barley</option>
                    <option value="Black pepper">Black pepper</option>
                    <option value="Cardamom">Cardamom</option>
                    <option value="Cashewnut">Cashewnut</option>
                    <option value="Castor seed">Castor seed</option>
                    <option value="Coconut ">Coconut</option>
                    <option value="Coriander">Coriander</option>
                    <option value="Cotton(lint)">Cotton(lint)</option>
                    <option value="Cowpea(Lobia)">Cowpea(Lobia)</option>
                    <option value="Dry chillies">Dry chillies</option>
                    <option value="Garlic">Garlic</option>
                    <option value="Ginger">Ginger</option>
                    <option value="Gram">Gram</option>
                    <option value="Groundnut">Groundnut</option>
                    <option value="Guar seed">Guar seed</option>
                    <option value="Horse-gram">Horse-gram</option>
                    <option value="Jowar">Jowar</option>
                    <option value="Jute">Jute</option>
                    <option value="Khesari">Khesari</option>
                    <option value="Linseed">Linseed</option>
                    <option value="Maize">Maize</option>
                    <option value="Masoor">Masoor</option>
                    <option value="Mesta">Mesta</option>
                    <option value="Moong(Green Gram)">Moong(Green Gram)</option>
                    <option value="Moth">Moth</option>
                    <option value="Niger seed">Niger seed</option>
                    <option value="Oilseeds total">Oilseeds total</option>
                    <option value="Onion">Onion</option>
                    <option value="Other  Rabi pulses">Other Rabi pulses</option>
                    <option value="Other Cereals">Other Cereals</option>
                    <option value="Other Kharif pulses">Other Kharif pulses</option>
                    <option value="Other Summer Pulses">Other Summer Pulses</option>
                    <option value="Peas &amp; beans (Pulses)">Peas &amp; beans (Pulses)</option>
                    <option value="Potato">Potato</option>
                    <option value="Ragi">Ragi</option>
                    <option value="Rapeseed &amp;Mustard">Rapeseed &amp;Mustard</option>
                    <option value="Rice">Rice</option>
                    <option value="Safflower">Safflower</option>
                    <option value="Sannhamp">Sannhamp</option>
                    <option value="Sesamum">Sesamum</option>
                    <option value="Small millets">Small millets</option>
                    <option value="Soyabean">Soyabean</option>
                    <option value="Sugarcane">Sugarcane</option>
                    <option value="Sunflower">Sunflower</option>
                    <option value="Sweet potato">Sweet potato</option>
                    <option value="Tapioca">Tapioca</option>
                    <option value="Tobacco">Tobacco</option>
                    <option value="Turmeric">Turmeric</option>
                    <option value="Urad">Urad</option>
                    <option value="Wheat">Wheat</option>
                    <option value="other oilseeds">other oilseeds</option>
                </select>
            </div>
            <div class="form-group">
                <label for="season">Season</label>
                <select id="season" name="season" required>
                    <option value="">-- Select Season --</option>
                    <option value="Kharif     ">Kharif</option>
                    <option value="Rabi       ">Rabi</option>
                    <option value="Whole Year ">Whole Year</option>
                    <option value="Summer     ">Summer</option>
                    <option value="Winter     ">Winter</option>
                    <option value="Autumn     ">Autumn</option>
                </select>
            </div>
            <div class="form-group">
                <label for="crop_year">Year</label>
                <input type="number" id="crop_year" name="crop_year" required min="1990" max="2030" value="2020">
            </div>
            <div class="form-group">
                <label for="rainfall">Annual Rainfall (mm)</label>
                <input type="number" step="0.01" id="rainfall" name="rainfall" required placeholder="e.g., 1200.5">
            </div>
            <div class="form-group">
                <label for="fertilizer">Fertilizer (kg)</label>
                <input type="number" step="0.01" id="fertilizer" name="fertilizer" required placeholder="e.g., 50000.0">
            </div>
            <div class="form-group">
                <label for="pesticide">Pesticide (kg)</label>
                <input type="number" step="0.01" id="pesticide" name="pesticide" required placeholder="e.g., 150.75">
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
    crop = request.form['crop']
    crop_year = int(request.form['crop_year'])
    season = request.form['season']
    state = request.form['state']
    rainfall = float(request.form['rainfall'])
    fertilizer = float(request.form['fertilizer'])
    pesticide = float(request.form['pesticide'])

    input_data = pd.DataFrame([{
        'Crop': crop,
        'Crop_Year': crop_year,
        'Season': season,
        'State': state,
        'Annual_Rainfall': rainfall,
        'Fertilizer': fertilizer,
        'Pesticide': pesticide
    }])

    prediction = model.predict(input_data)[0]

    result = f"""
    <div class="result">
        <h2>Predicted Crop Yield</h2>
        <p>{round(prediction, 4)} tonnes/hectare</p>
    </div>"""
    return HTML.replace('{result_block}', result)

if __name__ == '__main__':
    app.run(debug=False)
