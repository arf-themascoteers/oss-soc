import os
import math
import pandas as pd

spectra_file = "spectra.csv"
oc_file = "oc.csv"
out_file = "rgb.csv"

spectra_df = pd.read_csv(spectra_file)
oc_df = pd.read_csv(oc_file)
out = open(out_file, "w")
out.write(f"r,g,b,oc\n")
done_ids = []
duplicate_spectra = []
not_found_spectra = []

x = 0
for counter, row in oc_df.iterrows():
    raw_smp_id = row["uuid"]
    oc = row["oc"]
    if math.isnan(oc):
        continue
    smp_id = raw_smp_id
    if smp_id in done_ids:
        continue

    rows = (spectra_df.loc[spectra_df['uuid'] == smp_id])

    if len(rows) == 0:
        not_found_spectra.append(smp_id)
        continue
    spectra_row = rows.iloc[0]
    if len(rows) > 1:
        duplicate_spectra.append(spectra_row)


    r = spectra_row["r"]
    g = spectra_row["g"]
    b = spectra_row["b"]

    if math.isnan(r) or math.isnan(g) or math.isnan(b):
        continue

    out.write(f"{r},{g},{b},{oc}\n")

    done_ids.append(smp_id)
    x = x+1
    if x%100 == 0:
        print("Processed", x, counter)

print("total",len(done_ids))
print("not found",len(not_found_spectra))
print("duplicate",len(duplicate_spectra))

out.close()
print("done")

