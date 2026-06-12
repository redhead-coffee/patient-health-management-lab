from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import List, Dict, Annotated, Literal, Optional
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='patient ID required', examples=['P001'])]
    name: Annotated[str, Field(..., description='patient Name required', examples=['Jyanti Aich'])]
    city: Annotated[str, Field(..., description='patient City required', examples=['Kolkata'])]
    age: Annotated[int, Field(..., gt=0, lt=99,description='patient Age required', examples=[30])]
    gender: Annotated[Literal['male','female','others'], Field(..., description='patient Gender required', examples=['male','female','others'])]
    height: Annotated[float, Field(..., gt=0, description='patient Height required in meters', examples=[1.75])]
    weight: Annotated[float, Field(..., gt=0, description='patient Weight required in kg', examples=[70.0])]
    #do not need here: bmi: float
    #do not need here: verdict: str

    #for bmi calculation we can use computed_field decorator to calculate bmi based on height and weight fields.
    @computed_field
    @property
    def bmi(self) -> float:
        bmi=round(self.weight / (self.height ** 2), 2)
        return bmi
    
    #for verdict calculation we can use computed_field decorator to calculate verdict based on bmi fields.
    @computed_field
    @property
    def verdict(self) -> str: #at first verdict will trigger then it will trigger bmi because verdict is dependent on bmi. So, bmi will be calculated first then verdict will be calculated.
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi<30:
            return 'Normal weight'
        elif self.bmi<30:
            return 'Normal weight'
        else:
            return 'Obese'
        
#Updating patient data, We can use Optional fields in the PatientUpdate model to allow partial updates
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    City: Annotated[Optional[str], Field(default=None,)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=99)]
    gender: Annotated[Optional[Literal['male','female','others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]





def load_data():
    with open('patient.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    print("Saving data...")
    with open('patient.json', 'w') as f:
        json.dump(data, f)

@app.get('/')
def hello():
    return {'message': 'Hello'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(
    patient_id: str = Path(..., description='patient ID required', examples='P001')
):
    data = load_data()

    patient = data.get(patient_id)

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patient

@app.get('/sort')
def sort_patients(
    sort_by: str = Query(..., description='sort basis on height, weight or bmi'),
    order: str = Query('asc', description='sort based on asc or desc')
):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field select from {valid_fields}"
        )

    if order not in ['asc', 'desc']:
        raise HTTPException(
            status_code=400,
            detail="Invalid field select between asc and desc"
        )

    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=sort_order
    )

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    #load existing data from the JSON file
    data = load_data()
    #check if patient with the same ID already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    #if not, add the new patient to the data and save it back to the JSON file
    #exclude id field from the patient model when saving to JSON file because we are using id as the key in the JSON file, so we don't need to save it as a field in the patient data.
    data[patient.id] = patient.model_dump(exclude={'id'})
    #save into JSON file
    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})


@app.put('/edit/{patient_id}')
def update_patient(
    patient_id: str,
    patient_update: PatientUpdate):

    data = load_data()
    #patient = data.get(patient_id)

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_patient_info = data[patient_id]

    #update the patient data with the provided fields
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key,value in updated_patient_info.items():
        existing_patient_info[key] = value

        #existing_patient_info -> pydantic object -> recalute bmi and verdict -> convert to dict -> save to JSON file
    existing_patient_info['id'] = patient_id 
    #recalculate bmi and verdict by creating a new Patient object with the updated data   
    patient_pyd_obj = Patient(**existing_patient_info)
    #convert the updated Patient object back to a dictionary to save it to the JSON file.
    existing_patient_info = patient_pyd_obj.model_dump(exclude={'id'})
    #adding this dict to data dict
    data[patient_id] = existing_patient_info

    #saving data back to JSON file
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})