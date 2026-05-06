import pandas as pd
import requests
import time

# ------------ CONFIG ------------

INPUT_FILE = "/Users/ashish/Downloads/pickup_task_assign_2026-05-03T05_31_28.075789218Z.xlsx"

API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/Trip_complete"

DELAY = 0.3
MAX_RETRY = 3

# Default payload values
ACTION_LAT = 12.931941
ACTION_LNG = 77.622396
ODOMETER = 2100

# --------------------------------


# Load Excel file
df = pd.read_excel(INPUT_FILE)

success = 0
failed = 0
results = []


for _, row in df.iterrows():

    trip_id = int(row["drop_task_trip_id"])
    rider_id = int(row["rider_id"])

    payload = {
        "tripId": trip_id,
        "deliveredTo": "Buyer",
        "remarks": "",
        "podUrls": [""],
        "isOtpVerified": True,
        "actionLat": ACTION_LAT,
        "actionLng": ACTION_LNG,
        "odometer": ODOMETER,
        "isRiderVerified": True,
        "locationType": "office"
    }

    headers = {
        "rider_id": str(rider_id),
        "name": "",
        "Content-Type": "application/json"
    }

    retry = 0
    status = "failed"

    while retry < MAX_RETRY:

        try:
            response = requests.post(API_URL, json=payload, headers=headers)

            if response.status_code == 200:
                print(f"Trip Completed: {trip_id}")
                success += 1
                status = "success"
                break
            else:
                retry += 1
                time.sleep(1)

        except Exception as e:
            retry += 1
            time.sleep(1)

    if status != "success":
        print(f"Failed Trip: {trip_id}")
        failed += 1

    results.append({
        "trip_id": trip_id,
        "rider_id": rider_id,
        "status": status
    })

    time.sleep(DELAY)


# Save report
report = pd.DataFrame(results)
report.to_csv("trip_complete_report.csv", index=False)

print("--------- SUMMARY ---------")
print("Total Trips:", len(df))
print("Success:", success)
print("Failed:", failed)