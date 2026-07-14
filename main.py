from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import pickle
import pandas as pd
from schema.user_input import UserInput

# Load the trained model
with open('model\model.pkl', 'rb') as f: #rb means read binary mode because we are loading a binary file
    model = pickle.load(f)

#MLFlow model versioning to keep track of the model version and changes made to the model 
#not manually but through MLFlow model versioning to keep track of the model version and changes made to the model
MODEL_VERSION = "1.0.0"



app = FastAPI()


@app.get('/')
def home():
    return {"message": "Welcome to the Insurance Charges Prediction API. Use the /predict endpoint to get predictions."}


#health check endpoint to check if the API is running
#machine readable status check for the API to check if the API is running or not in aws or kubernetes 
#cloud native applications can use this endpoint to check the health of the API and take necessary actions if the API is not running
#and they force to follow this health check endpoint to check the health of the API and take necessary actions if the API is not running
@app.get('/health')
def health_check():
    return {
        "status": "API is running",
        "model_version": MODEL_VERSION, 
        "model_status": model is not None #this are the rules to make industry standard check endpoint
    }

@app.post('/predict')
def predict_charges(data: UserInput):

    input_data = pd.DataFrame([{

        'age': data.age,
        'sex': data.sex,
        'bmi': data.bmi,
        'children': data.children,
        'smoker': data.smoker,
        'region': data.region,
        'lifestyle_risk': data.lifestyle_risk,
        'age_group': data.age_group,
        'city_tier': data.city_tier

    }])

    
    
    
    #yo! 
    print(input_data)
    print(input_data.dtypes)


    prediction = model.predict(input_data)
    return JSONResponse(content={
        "predicted_charge": float(prediction[0])})
