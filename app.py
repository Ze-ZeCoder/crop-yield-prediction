from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load the trained model
with open('crop_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    area = request.form['area']
    item = request.form['item']
    year = int(request.form['year'])
    rainfall = float(request.form['rainfall'])
    pesticides = float(request.form['pesticides'])
    temp = float(request.form['temp'])
    
    # Create input dataframe
    input_data = pd.DataFrame([{
        'Area': area,
        'Item': item,
        'Year': year,
        'average_rain_fall_mm_per_year': rainfall,
        'pesticides_tonnes': pesticides,
        'avg_temp': temp
    }])
    
    # Make prediction
    prediction = model.predict(input_data)[0]
    
    return render_template('index.html', prediction=round(prediction, 2))

if __name__ == '__main__':
    app.run(debug=True)
