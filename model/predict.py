import pickle
import pandas as pd

# Load the trained model
with open('model\model.pkl', 'rb') as f: #rb means read binary mode because we are loading a binary file
    model = pickle.load(f)

#MLFlow model versioning to keep track of the model version and changes made to the model 
#not manually but through MLFlow model versioning to keep track of the model version and changes made to the model
MODEL_VERSION = "1.0.0"


def predict_charges(user_input: dict):

    input_df = pd.DataFrame([user_input])
    prediction = model.predict(input_df)[0]
    return prediction