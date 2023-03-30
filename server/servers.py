# Import flask and datetime module for showing date and time
from flask import Flask
from flask import current_app,jsonify,request
import datetime
import os
import jsonpickle

from flask_cors import CORS, cross_origin
from appriori import Apriori
import json
import joblib
import csv
import pandas as pd

import numpy as np



itemsetserver = []

# Initializing flask app
app = Flask(__name__)
CORS(app, support_credentials=True)
  




@cross_origin(supports_credentials=True)


@app.route("/getbord", methods=["POST"], strict_slashes=False)
def do_comp11():
    print("hi bord")
   
   
    

    
    return [pl.game.state.bord,t]
  






# Route for seeing a data
@app.route('/data')
def get_time():
    
    # Returning an api for showing in  reactjs
    return pl.game.state.bord


""""""
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



@app.route('/get-minsup', methods=['POST'])
def get_minsup():
    global itemsetserver
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400

        file = request.files['file']

        if file.filename == '':
            return 'No selected file', 400

        if file:
            # Save the file in the specified folder
            
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            print(file)
            df = []
            try :
               if file.filename.endswith(".xlsx") :
                df = pd.read_excel(file_path, low_memory=False)
               else :
                df = pd.read_csv(file_path, low_memory=False)
            except:
              print("Error")

            transListSet = []
           
            print(df)
            df = df.where(pd.notnull(df), None)
            df = df.dropna()
            

        


            for index, row in df.iterrows():


                 transListSet.append(set(row))

            priority = request.form.get("prio")  # Get minsup value
            print(priority)
            objApriori = Apriori()
            prioritys = priority.split(',')
            
            minsup = objApriori.adaptive_support_threshold(transListSet,prioritys) 
            
            return jsonify(minsup)

@app.route('/upload', methods=['POST'])
def upload_file():
    global itemsetserver
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400

        file = request.files['file']

        if file.filename == '':
            return 'No selected file', 400

        if file:
            # Save the file in the specified folder
            
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            print(file)
            df = []
            try :
               if file.filename.endswith(".xlsx") :
                df = pd.read_excel(file_path, low_memory=False)
               else :
                df = pd.read_csv(file_path, low_memory=False)
            except:
              print("Error")

            transListSet = []
           
            print(df)
            df = df.where(pd.notnull(df), None)
            df = df.dropna()
            

        


            for index, row in df.iterrows():


                 transListSet.append(set(row))

            minsup = float(request.form.get("minsup", 0.1))  # Get minsup value

            objApriori = Apriori()

            freq_items2 = objApriori.apriori(transListSet, minsup) 
            itemsetserver = freq_items2
            print(freq_items2)
            
            json_data = jsonpickle.encode(freq_items2)
            json_data = json.loads(json_data)  


            cleaned_data = [
    {
        "itemset": list(itemset_support["py/tuple"][0]["py/reduce"][1]["py/tuple"][0])  ,
        "support": itemset_support["py/tuple"][1],
    }
    for itemset_support in json_data
             ]
            print("/////////////////////")
            print(cleaned_data)
            return jsonify(cleaned_data)


model = joblib.load('random_forest_regressor.pkl')
@app.route('/predict', methods=['POST'])
def predict():

    
    global itemsetserver
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400

        file = request.files['file']

        if file.filename == '':
            return 'No selected file', 400

        if file:
            # Save the file in the specified folder
            
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            print(file)
            df = []
            try :
               if file.filename.endswith(".xlsx") :
                df = pd.read_excel(file_path, low_memory=False)
               else :
                df = pd.read_csv(file_path, low_memory=False)
            except:
              print("Error")
           
            
           
            print(df)
            print("test")
            # Get number of rows
            num_rows = len(df)

            # Get number of columns
            num_cols = len(df.columns)

            # Get number of columns with dtype 'object'
            obj_cols = len(df.select_dtypes(include=['object']).columns)

            # Get number of columns with dtype 'float64'
            float_cols = len(df.select_dtypes(include=['float64']).columns)

            # Get number of columns with dtype 'int64'
            int_cols = len(df.select_dtypes(include=['int64']).columns)

            # Get number of columns with dtype 'bool'
            bool_cols = len(df.select_dtypes(include=['bool']).columns)

          
            print("test")
            numitems = request.form.get("numitems")
            print("numitems" ,numitems)
            input_data = [[num_rows, num_cols, numitems, obj_cols, float_cols, int_cols, bool_cols]]
            dfs = pd.DataFrame(input_data, columns=['num_rows','num_cols','num_frequent_itemsets','object','float64','int64','bool'])
            print(dfs)
            prediction = model.predict(dfs)
            print(prediction)
            return jsonify( prediction[0])
    

@app.route('/get_rules', methods=['POST'])
def get_rules():
    global itemsetserver
    data = request.json
    num_rules = data['num_rules']
    confidence = data['confidence']
    print(itemsetserver)
    objApriori = Apriori()
    rules = objApriori.generate_rules(itemsetserver, confidence)
    print(rules)
    cleaned_data = []
    sorted_rules = sorted(rules, key=lambda rule: rule[3], reverse=True)

    # Get the top 10 rules
    top_10_rules = sorted_rules[:int(num_rules)] 
    for  row in top_10_rules:
        antecedents = list(row[0])
        consequents = list(row[1])

        support =str(round(float(row[2]), 3))
        lift = str(round(float(row[4]), 3))
        leverage = str(round(float(row[5]), 3))
        conviction = str(round(float(row[6]), 3))

        confidence = str(round(float(row[3]), 3) )
        cleaned_data.append({
        "antecedents": antecedents,
        "consequents": consequents,
        "support": support,
        "lift": lift,
        "conviction": conviction,
        "confidence": support,
        
    })


           

    return jsonify(cleaned_data)



if __name__ == '__main__':
    app.run()