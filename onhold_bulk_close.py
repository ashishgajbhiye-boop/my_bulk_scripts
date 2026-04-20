import pandas as pd
import requests
import time

# -------- CONFIG --------
TRIP_FILE = "Users/ashish/Downloads/pickup_task_assign_2026-03-22T13_23_25.752575578Z.xlsx"
REMARK_FILE = "Users/ashish/Downloads/pickup_task_assign_2026-03-22T13_23_25.752575578Z.xlsx"

API_URL = "https://35idc7phd7.execute-api.ap-south-1.amazonaws.com/V1/sarathyupdate/manualtripclose"

HEADERS = {
    "Content-Type": "application/json"
}

DEFAULT_REASON = "Customer not answering calls"
DELAY = 0.3
# ------------------------


# Load files
trip_df = pd.read_excel(TRIP_FILE)
remark_df = pd.read_excel(REMARK_FILE)


# Get trip IDs
trip_ids = trip_df["Trip ID"].unique()


# Filter remark table for those trips
remark_filtered = remark_df[remark_df["Trip ID"].isin(trip_ids)]


# Pick one reason per trip
remark_one_reason = remark_filtered.groupby("Trip ID").first().reset_index()


success = 0
failed = 0
results = []


for _, row in remark_one_reason.iterrows():

    trip_id = int(row["Trip ID"])
    rider_reason = str(row["Rider Reason"])

    if "cancel" in rider_reason.lower():
        final_reason = DEFAULT_REASON
    else:
        final_reason = rider_reason

    payload = {
        "tripId": trip_id,
        "riderReason": final_reason,
        "failedDeliveryReason": final_reason,
        "currentMedium": "manual",
        "isFake": False
    }

    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS)

        if response.status_code == 200:
            print(f"Closed Trip {trip_id}")
            success += 1
            status = "success"
        else:
            print(f"Failed {trip_id} | {response.text}")
            failed += 1
            status = "failed"

    except Exception as e:
        print(f"Error {trip_id} | {e}")
        failed += 1
        status = "error"

    results.append({
        "tripId": trip_id,
        "reason_used": final_reason,
        "status": status
    })

    time.sleep(DELAY)


# Save report
pd.DataFrame(results).to_csv("trip_closure_report.csv", index=False)

print("------ SUMMARY ------")
print("Success:", success)
print("Failed:", failed)