import pandas as pd
import requests

# API URLs
pickup_url = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/Pickup_task"
trip_url = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/Trip_complete"

# Excel file path
file_path = "/Users/ashish/Downloads/pickup_task_assign_2026-05-07T11_55_07.23224484Z.xlsx"


df = pd.read_excel(file_path)


total = len(df)

print(f"\nProcessing {total} rows...\n")

for index, row in df.iterrows():

    tripId = int(row["pickup_task_trip_id"])
    taskEntityId = int(row["task_entity_id"])
    rider_id = int(row["rider_id"])

    print(f"{index+1}/{total} → Trip {tripId}")

    try:
        # ---------- API 1 : Pickup Complete ----------
        headers1 = {
            "Content-Type": "application/json",
            "rider_id": str(rider_id)
        }

        payload1 = {
            "tripId": tripId,
            "taskEntityId": taskEntityId,
            "status": "COMPLETED",          #status-  FAILED, COMPLETED
            "reason": "",
            "pickupOtp": ""
        }
        r1 = requests.post(pickup_url, headers=headers1, json=payload1)

        print("Pickup API:", r1.status_code)

        # Only continue if pickup was successful
        if r1.status_code != 200:
            print("Pickup failed → skipping Trip completion\n")
            continue

        # ---------- API 2 : Trip Complete ----------
        headers2 = {
            "Content-Type": "application/json",
            "rider_id": str(rider_id),
            "name": ""
        }

        payload2 = {
            "tripId": tripId,
            "deliveredTo": "store manager",
            "remarks": "",
            "podUrls": [""],
            "isOtpVerified": True,
            "actionLat": 12.931941,
            "actionLng": 77.622396,
            "odometer": 2100,
            "isRiderVerified": True,
            "locationType": "office"
        }

        r2 = requests.post(trip_url, headers=headers2, json=payload2)

        print("Trip API:", r2.status_code, "\n")

    except Exception as e:
        print("Error:", e, "\n")

print("Finished.")