import requests
import time

# -------- CONFIG --------

API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/Manualtripclose"

# Enter Trip IDs here (comma separated inside string)
trip_ids = "36939519"

DELAY = 0.3   # small delay between API calls

# ------------------------

headers = {
    "Content-Type": "application/json"
}

trip_list = [int(x.strip()) for x in trip_ids.split(",")]

success = 0
failed = 0

for trip_id in trip_list:

    payload = {
        "tripId": trip_id,
        "riderReason": "Wrong PIN Code",  # Customer not answering calls
        "failedDeliveryReason": "Wrong PIN Code",
        "currentMedium": "manual",
        "isFake": False
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            print(f"✔ Closed Trip: {trip_id}")
            success += 1
        else:
            print(f"✖ Failed Trip: {trip_id} | Status: {response.status_code}")
            failed += 1

    except Exception as e:
        print(f"Error for Trip {trip_id}: {e}")
        failed += 1

    time.sleep(DELAY)

print("\n------ SUMMARY ------")
print("Total Trips:", len(trip_list))
print("Closed:", success)
print("Failed:", failed)