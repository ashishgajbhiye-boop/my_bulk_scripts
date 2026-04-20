import requests
import time

API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/Index_order_scan"

ORG_ID = "1"

suborder_ids = [
34449413,
38033365,
37612161,
37712668,
38034506
]

DELAY = 0.3

success = 0
failed = 0

headers = {
    "Content-Type": "application/json",
    "orgId": ORG_ID
}

for suborder_id in suborder_ids:

    payload = {
        "orderIds": [],
        "suborderIds": [suborder_id]
    }

    try:
        response = requests.patch(API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            print(f"✔ Indexed: {suborder_id}")
            success += 1
        else:
            print(f"✖ Failed: {suborder_id} | Status {response.status_code}")
            failed += 1

    except Exception as e:
        print(f"Error: {suborder_id} → {e}")
        failed += 1

    time.sleep(DELAY)


print("\n------ SUMMARY ------")
print("Total:", len(suborder_ids))
print("Indexed:", success)
print("Failed:", failed)