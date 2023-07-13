import pandas as pd
import numpy as np

rgb_file = "out2.csv"

npdf = pd.read_csv(rgb_file).to_numpy()

print(np.count_nonzero(np.isnan(npdf)))
print(npdf.shape)
x = 0
for i in range(npdf.shape[0]):
    if np.count_nonzero(np.isnan(npdf[i])) > 0:
        for j in range(npdf.shape[1]):
            if np.count_nonzero(np.isnan(npdf[i][j])) > 0:
                print(i,j)
                break
print(x)
print("Done")