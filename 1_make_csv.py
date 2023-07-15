import os
import math
import pandas as pd
import numpy as np

done_ids = []
out_file = "out.csv"
out = open(out_file, "w")

visnir_cols = [f"scan_visnir.{band}_pcnt" for band in range(350, 2502, 2)]
visnir_cols_str = ",".join(visnir_cols)
visnir_no_full_row_found = 0
visnir_col_out = ",".join([str(band)+"_v" for band in range(350, 2502, 2)])

mir_cols = [f"scan_mir.{band}_abs" for band in range(600,4002,2)]
mir_cols_str = ",".join(mir_cols)
mir_no_full_row_found = 0
mir_col_out = ",".join([str(band)+"_m" for band in range(600,4002,2)])

out.write(f"{uuid},{visnir_col_out},{mir_col_out},oc,source\n")

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

        df = rows[visnir_cols]
        selected_rows = []
        for i in range(len(rows)):
            a_row = df.iloc[i].to_numpy()
            if np.count_nonzero(np.isnan(a_row)) == 0:
                selected_rows.append(i)

        if len(selected_rows) == 0:
            visnir_no_full_row_found = visnir_no_full_row_found + 1
            continue

        visnir_data = df.iloc[selected_rows]
        visnir_data = np.mean(visnir_data.to_numpy(), axis=0)
        if np.count_nonzero(np.isnan(visnir_data)) != 0:
            print("ALERT")
        visnir_data_str = ",".join([str(i) for i in visnir_data])

        rows = (mir_df.loc[mir_df['id.layer_uuid_c'] == smp_id])
        if len(rows) == 0:
            continue

        df = rows[mir_cols]
        selected_rows = []
        for i in range(len(rows)):
            a_row = df.iloc[i].to_numpy()
            if np.count_nonzero(np.isnan(a_row)) == 0:
                selected_rows.append(i)

        if len(selected_rows) == 0:
            mir_no_full_row_found = mir_no_full_row_found + 1
            continue

        mir_data = df.iloc[selected_rows]
        mir_data = np.mean(mir_data.to_numpy(), axis=0)
        if np.count_nonzero(np.isnan(mir_data)) != 0:
            print("ALERT")
        mir_data_str = ",".join([str(i) for i in mir_data])

        out.write(f"{smp_id},{visnir_data_str},{mir_data_str},{oc},{idx}\n")

        done_ids.append(smp_id)
        x = x+1
        if x%100 == 0:
            print("Processed", x, counter)

out.close()
print("total",len(done_ids))
print("visnir_no_full_row_found",visnir_no_full_row_found)
print("mir_no_full_row_found",mir_no_full_row_found)