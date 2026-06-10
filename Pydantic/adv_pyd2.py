from typing import List,Dict
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, computed_field

patient_info={'name':'Nitishh','email':'bwumca22176@icic.com','age':67,'height_in_meters': 1.75,'weight_in_kg':50,'contact_details':{'gmail':'xyz@gmail.com','phone':'2353462','emergency':'5876543210'}}

class patient(BaseModel):
    name:str
    email:EmailStr
    age:int
    height_in_meters:float
    weight_in_kg:float
    married:bool = False
    allergies:List[str]= None
    contact_details:Dict[str,str]

    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains=['hdfc.com','icic.com']
        domain_name=value.split('@')[-1]


        if domain_name not in valid_domains:
            raise ValueError('Not a Valid Domain')
        return value
    #case:2--performing a Transformation using field_validator

    @field_validator('name')
    @classmethod
    def transform_name(cls,value):
        return value.upper()

    #---exploring before mode and after mode----This means validator runs before Pydantic converts type--(not int yet)   After validator passes, Pydantic converts to int.

    @field_validator('age',mode='before')
    @classmethod
    def validate_age(cls,value):
        if 0< value <100:
            return value
        else:
            raise ValueError('age should be in between 0 & 100')
        #model validation--we can access multiple fields of the model and perform validation based on that--we can also perform cross field validation
    @model_validator(mode='after')
    def validate_emergency_contact(cls,model):
        if model.age>60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have an emergency contact')
        return model
    
    #computed field--we can define a method that computes a value based on other fields in the model and we can access that computed value as an attribute of the model instance.
    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight_in_kg/(self.height_in_meters**2),2)
        return bmi
        #height_in_meters=self.height_in_meters/100.00
        #return round(self.age/(height_in_meters**2),2)





def insert_data(patient:patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.height_in_meters)
    print(patient.weight_in_kg)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print(patient.bmi)

patient2=patient(**patient_info)

insert_data(patient2)
