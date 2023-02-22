import os
import math
import pandas as pd

spectra_file = "spectra.csv"
oc_file = "oc.csv"

spectra_df = pd.read_csv(spectra_file)
oc_df = pd.read_csv(oc_file)

not_found = []
x = 0
for counter, row in spectra_df.iterrows():
    raw_smp_id = row["uuid"]
    smp_id = raw_smp_id
    rows = (oc_df.loc[oc_df['uuid'] == smp_id])

    if len(rows) == 0:
        not_found.append(smp_id)
        continue

    if len(rows) > 1:
        print("duplicate",raw_smp_id)
        continue


    x = x+1

    if x%10 == 0:
        print("Got",x)

print("total",x)
print("not found",len(not_found))
print("done")

