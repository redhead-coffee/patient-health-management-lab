from pydantic import BaseModel

class Address(BaseModel):
    city:str
    state:str
    pin_code:str

class Patient(BaseModel):
    name:str
    gender:str
    age:int
    address:Address #nested model--we can use another Pydantic model as a field in our main model. This allows us to create complex data structures and validate them effectively.



#this should be at first to avoid circular import issues
address_info={'city':'Bangalore','state':'Karnataka','pin_code':'560001'}

address1=Address(**address_info)

#and then we can use this address1 object to create our patient object. This way we can ensure that the address details are valid before creating the patient object.
patient_dict={'name':'Nitishh','gender':'Male','age':67,'address':address1}

patient1=Patient(**patient_dict)

#print(patient1)
print(patient1.name)
print(patient1.address.city)
print(patient1.address.state)
print(patient1.address.pin_code)