import pandas as pd
import numpy as np

rgb_file = "out.csv"

npdf = pd.read_csv(rgb_file).to_numpy()

print(np.count_nonzero(np.isnan(npdf)))

print("Done")