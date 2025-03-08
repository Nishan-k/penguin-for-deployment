from fastapi import FastAPI
import joblib
from pydantic import BaseModel
import pandas as pd
import uvicorn

# Load the  model:
penguin_clf = joblib.load("./notebook/penguin_clf.pkl")

# Define the input features:
class Input_features(BaseModel):
    island: str
    sex: str
    bill_length_mm: float
    bill_depth_mm: float
    flipper_length_mm: int
    body_mass_g: int



app = FastAPI()




@app.post("/")
def prediction(input_features:Input_features):
    input_data = pd.DataFrame([input_features.model_dump()])
    result = penguin_clf.predict(input_data)
    return {"prediction": result.tolist()}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000)) 
    uvicorn.run(app, host="0.0.0.0", port=port)