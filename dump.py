import pandas as pd
import numpy as np
import json

df = pd.read_pickle("data/tmp.pickle")
df/= (df.max(axis=0) - df.min(axis=0)) 

countries = df.index.tolist()


clean = df.replace({np.nan: None})

data = {
    "countries": countries,
    "matrix": clean.to_dict()
}

with open("data/data.json", "w") as f:
    json.dump(data, f, allow_nan=False)
