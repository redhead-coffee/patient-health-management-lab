from pydantic import BaseModel

class Address(BaseModel):
    city:str
    state:str
    pin_code:str

class Patient(BaseModel):
    name:str
    gender:str
    age:int
    address:Address


address_info={'city':'Bangalore','state':'Karnataka','pin_code':'560001'}

address1=Address(**address_info)

patient_dict={'name':'Nitishh','gender':'Male','age':67,'address':address1} 

patient1=Patient(**patient_dict)

#print(patient1)
print(patient1.name)
print(patient1.address.city)
print(patient1.address.state)
print(patient1.address.pin_code)