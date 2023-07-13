import pandas as pd
import numpy as np

rgb_file = "out.csv"

npdf = pd.read_csv(rgb_file).to_numpy()

# print(np.count_nonzero(np.isnan(npdf)))
print(npdf.shape)
# x = 0
# for i in range(npdf.shape[0]):
#     if np.count_nonzero(np.isnan(npdf[i])) > 0:
#         x = x + 1
#
# print(x)

print(np.count_nonzero(npdf[:,-1]==1))
print(np.count_nonzero(npdf[:,-1]==0))

print("Done")
