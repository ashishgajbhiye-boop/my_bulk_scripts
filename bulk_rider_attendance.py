import requests
import time

# -------- CONFIG --------

API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/KYC/Rider_Attendance"

# Paste rider IDs here (comma separated)
rider_ids = [
    25959, 26170, 25958, 26270, 24702, 24689, 23797, 24724, 26180, 26269, 24557, 25970, 25960, 24620, 25964

]

DELAY = 0.3
MAX_RETRY = 3

# ------------------------

success = 0
failed = 0
results = []

for rider_id in rider_ids:

    url = f"{API_URL}?rider_ids={rider_id}"

    retry = 0
    status = "failed"

    while retry < MAX_RETRY:

        try:
            response = requests.post(url)

            if response.status_code == 200:
                print(f"Attendance marked for Rider {rider_id}")
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
        print(f"Failed for Rider {rider_id}")
        failed += 1

    results.append({
        "rider_id": rider_id,
        "status": status
    })

    time.sleep(DELAY)

print("\n------ SUMMARY ------")
print("Total Riders:", len(rider_ids))
print("Success:", success)
print("Failed:", failed)