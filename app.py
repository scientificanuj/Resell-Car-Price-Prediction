from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open(r'car_price.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    Owner_1=0
    if request.method == 'POST':
        Car_Age = int(request.form['Car_Age'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Owner_0=request.form['Owner_0']
        if(Owner_0=='0'):
                Owner_0=0
        elif( Owner_0=='1'):
            Owner_0=1
        else:
            Owner_0=2
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=0
        elif( Fuel_Type_Petrol=='Diesel'):
            Fuel_Type_Petrol=1
        else:
            Fuel_Type_Petrol=2
        Car_Age=2021-Car_Age
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=0
        else:
            Transmission_Mannual=1

        prediction= model.predict([[Car_Age,Present_Price,Kms_Driven,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual,Owner_0]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('after.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('after.html',prediction_text="You Can Sell The Car at {} lac".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
