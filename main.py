from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
import pickle
import pandas as pd

# Load the trained model
with open('model\model.pkl', 'rb') as f: #rb means read binary mode because we are loading a binary file
    model = pickle.load(f)

tier_1_cities = ['southwest','southeast']
tier_2_cities = ['northwest','northeast']

app = FastAPI()

#pydantic model to validate the input data
#as per model training dataset 	age	sex	bmi	children	smoker	region
class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=99, description='Age of the user', examples=[30])]
    sex: Annotated[Literal['male', 'female'], Field(..., description='Sex of the user', examples=['male'])]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the user in kg', examples=[70.0])]
    height: Annotated[float, Field(..., gt=0, description='Height of the user in cm', examples=[170.0])]
    children: Annotated[int, Field(..., ge=0, description='Number of children', examples=[0])]
    smoker: Annotated[Literal['yes', 'no'], Field(..., description='Whether the user smokes', examples=['yes/no'])] 
    region: Annotated[Literal['northeast', 'northwest', 'southeast', 'southwest'], Field(..., description='Region of the user', examples=['northeast'])]

    @field_validator('region')
    @classmethod
    def validate_region(cls, v:str) -> str:
        v = v.strip().title()
        return v


    @computed_field
    @property
    def bmi(self) -> float:
        bmi=round(self.weight / (self.height ** 2), 2)
        return bmi
    
    @computed_field
    @property
    #lifestyle risk through smoking
    def lifestyle_risk(self) -> str:
        if self.smoker == 'yes' and self.bmi > 30:
            return "High"
        elif self.smoker == 'yes' or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 35:
            return "adult"
        elif self.age < 55:
            return "middle_aged"
        else:
              return "senior"
        
    @computed_field
    @property
    def city_tier(self) -> str:
        if self.region in tier_1_cities:
            return 1
        elif self.region in tier_2_cities:
            return 2
        else:
            return 3

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

    prediction = model.predict(input_data)
    return JSONResponse(content={"predicted_charge": float(prediction[0])})
