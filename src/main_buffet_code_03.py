import pandas as pd

processed_df = []
# ticker_data = input() #7974,9983,1547
ticker_data = ["7974"]

processed_data = pd.read_csv(f"./csv/{ticker_data[0]}_processedData.csv")
print(processed_data.isnull().sum())
print(processed_data)