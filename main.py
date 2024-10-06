from flask import Flask, render_template, request
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

app = Flask(_name_)


@app.route('/')
def weather():
    return render_template("index.html")
  
@app.route('/weather',methods=["Post"])
def page():
  Maximum_Temp = eval(request.form.get("Maximum_Temp"))
  Minimum_Temp = eval(request.form.get("Minimum_Temp"))
  Wind_Speed = eval(request.form.get("Wind_Speed"))
  
  url = "weatherpredict.csv"
  data = pd.read_csv(url)
  X = data[['Maximum_Temp', 'Minimum_Temp', 'Wind_Speed']]
  y = data['weather']
  
  model = RandomForestClassifier()
  model.fit(X ,y)
  
  arr = model.predict([[Maximum_Temp, Minimum_Temp, Wind_Speed]])
  return render_template("index.html", result=arr[0])

if _name_ == '_main_':
    app.run()
