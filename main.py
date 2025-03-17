from flask import Flask, render_template, request
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import requests
import io

app = Flask(__name__, template_folder="templates")  # Ensure Flask looks in /templates


# Load dataset from GitHub URL
CSV_URL = "https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/YOUR_REPO/main/weatherpredict.csv"

def load_data():
    response = requests.get(CSV_URL)
    data = pd.read_csv(io.StringIO(response.text))
    return data

@app.route('/')
def weather():
    return render_template("index.html")

@app.route('/weather', methods=["POST"])
def page():
    try:
        Maximum_Temp = float(request.form.get("Maximum_Temp"))
        Minimum_Temp = float(request.form.get("Minimum_Temp"))
        Wind_Speed = float(request.form.get("Wind_Speed"))

        data = load_data()
        X = data[['Maximum_Temp', 'Minimum_Temp', 'Wind_Speed']]
        y = data['weather']

        model = RandomForestClassifier()
        model.fit(X, y)

        prediction = model.predict([[Maximum_Temp, Minimum_Temp, Wind_Speed]])
        return render_template("index.html", result=prediction[0])
    except Exception as e:
        return render_template("index.html", result=f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
