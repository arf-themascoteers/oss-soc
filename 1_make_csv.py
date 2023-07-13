import os
import math
import pandas as pd

done_ids = []
out_file = "out.csv"
out = open(out_file, "w")
visnir_band_list = list(range(350, 2502, 2))
visnir_band_list = [str(i) + "_visnir" for i in visnir_band_list]
visnir_cols = ",".join(visnir_band_list)

mir_band_list = list(range(600, 4002, 2))
mir_band_list = [str(i) + "_mir" for i in mir_band_list]
mir_cols = ",".join(mir_band_list)

out.write(f"{visnir_cols},{mir_cols},oc,source\n")

for idx, d in enumerate(os.listdir("data")):
    print(f"**********{d}**************")
    path = os.path.join("data",d)
    visnir = os.path.join(path, "visnir.data.csv")
    mir = os.path.join(path, "mir.data.csv")
    soillab_file = os.path.join(path, "soillab.data.csv")
    visnir_df = pd.read_csv(visnir)
    mir_df = pd.read_csv(mir)
    soillab_df = pd.read_csv(soillab_file)




    x = 0
    for counter, row in soillab_df.iterrows():
        raw_smp_id = row["id.layer_uuid_c"]
        if raw_smp_id in done_ids:
            print("DUPLICATE alert")
            exit(1)
        oc = row["oc_usda.calc_wpct"]
        if math.isnan(oc):
            continue
        smp_id = raw_smp_id
        if smp_id in done_ids:
            continue

        rows = (visnir_df.loc[visnir_df['id.layer_uuid_c'] == smp_id])
        if len(rows) == 0:
            continue
        visnir_values = []
        for band in range(350, 2502, 2):
            band_str = f"scan_visnir.{band}_pcnt"
            value = sum(rows[band_str]) / len(rows)
            visnir_values.append(value)


        rows = (mir_df.loc[mir_df['id.layer_uuid_c'] == smp_id])
        if len(rows) == 0:
            continue
        mir_values = []
        for band in range(600,4002,2):
            band_str = f"scan_mir.{band}_abs"
            value = sum(rows[band_str])/len(rows)
            mir_values.append(value)

        visnir_values = [str(i) for i in visnir_values]
        visnir_str = ",".join(visnir_values)
        mir_values = [str(i) for i in mir_values]
        mir_str = ",".join(mir_values)
        out.write(f"{visnir_str},{mir_str},{oc},{idx}\n")

        done_ids.append(smp_id)
        x = x+1
        if x%100 == 0:
            print("Processed", x, counter)

out.close()
print("total",len(done_ids))
