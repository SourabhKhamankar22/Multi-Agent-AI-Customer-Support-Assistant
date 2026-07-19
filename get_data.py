import os
import pandas as pd

# 1. Create your datasets folder required by the project structure
os.makedirs("datasets", exist_ok=True)

print("Downloading the original PolyAI dataset directly from their raw source...")

# 2. Download the original raw CSV directly from PolyAI's server using Pandas
url = "https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/master/banking_data/train.csv"
df = pd.read_csv(url)

# 3. Extract 200 random rows for your few-shot prompt
sample_df = df.sample(n=200, random_state=42)

# 4. Save the file exactly where the project requires it
sample_df.to_csv("datasets/intent_examples.csv", index=False)

print("Success! Your original PolyAI intent_examples.csv file is ready.")