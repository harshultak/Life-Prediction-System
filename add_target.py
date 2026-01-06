import pandas as pd
import numpy as np

# Load existing dataset
df = pd.read_csv("life_expectancy_preprocessed.csv")

# Add a dummy target column
df["Life expectancy"] = np.random.randint(50, 86, size=len(df))

# Save the updated dataset
df.to_csv("life_expectancy_preprocessed_with_target.csv", index=False)

print("Life expectancy column added successfully.")
