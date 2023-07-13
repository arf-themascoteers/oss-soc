import os
import math
import pandas as pd

for d in os.listdir("data"):
    print(f"**********{d}**************")
    path = os.path.join("data",d)
    visnir = os.path.join(path, "visnir.data.csv")
    mir = os.path.join(path, "mir.data.csv")
    soillab_file = os.path.join(path, "soillab.data.csv")

    visnir_df = pd.read_csv(visnir)
    mir_df = pd.read_csv(mir)
    oc_df = pd.read_csv(soillab_file)

    not_found_oc = []
    not_found_visnir = []
    not_found_mir = []

    duplicate_oc = 0
    duplicate_visnir = 0
    duplicate_mir = 0

    x = []
    for counter, row in oc_df.iterrows():
        oc = row["oc_usda.calc_wpct"]
        raw_smp_id = row["id.layer_uuid_c"]

        if raw_smp_id in x:
            duplicate_oc = duplicate_oc + 1
            continue

        if math.isnan(oc):
            not_found_oc.append(raw_smp_id)
            continue

        smp_id = raw_smp_id
        rows = (visnir_df.loc[visnir_df['id.layer_uuid_c'] == smp_id])
        if len(rows) == 0:
            not_found_visnir.append(smp_id)
            continue

        if len(rows) > 1:
            duplicate_visnir = duplicate_visnir + 1

        rows = (mir_df.loc[mir_df['id.layer_uuid_c'] == smp_id])
        if len(rows) == 0:
            not_found_mir.append(smp_id)
            continue

        if len(rows) > 1:
            duplicate_mir = duplicate_mir + 1

        x.append(smp_id)

        if len(x)%5000 == 0:
            print("Got",len(x))

    print("Given",oc_df.shape[0])
    print("total",len(x))
    print("not found oc", len(not_found_oc))
    print("not found visnir", len(not_found_visnir))
    print("not found mir", len(not_found_mir))
    print("duplicate oc", duplicate_oc)
    print("duplicate visnir", duplicate_visnir)
    print("duplicate mir", duplicate_mir)
    print("done")

