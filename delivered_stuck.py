import pandas as pd
import requests
from datetime import datetime
import time

# -------- CONFIG --------
FILE_PATH = "/Users/ashish/Downloads/ofd_stuck_query_2026-04-23T16_53_23.568443346Z.xlsx"

URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/tracking/Update_shipment_status"
HEADERS = {"Content-Type": "application/json"}

LOCATION = "Bangalore"
SHIPPER_ID = 301
STATUS = "Delivered"
REMARK = ""
# ------------------------

start = time.time()

# Load Excel
df = pd.read_excel(FILE_PATH)
df = df.dropna(subset=["awb"])

# Current time
update_time = datetime.now().strftime("%m/%d/%Y %H:%M")

success_count = 0
fail_count = 0

print(f"\nProcessing {len(df)} AWBs one by one...\n")

for _, row in df.iterrows():
    awb = str(row.awb).strip()
    user_id = int(row.user_id)

    payload = [{
        "awb": awb,
        "location": LOCATION,
        "userId": user_id,
        "shipperId": SHIPPER_ID,
        "updateTime": update_time,
        "remark": REMARK,
        "shipmentStatus": STATUS
    }]

    try:
        response = requests.post(URL, headers=HEADERS, json=payload)

        if response.status_code == 200:
            print(f"✓ {awb} updated")
            success_count += 1
        else:
            print(f"✗ {awb} failed | Status: {response.status_code} | Response: {response.text}")
            fail_count += 1

    except Exception as e:
        print(f"⚠ {awb} error: {str(e)}")
        fail_count += 1

end = time.time()
runtime = round(end - start, 2)

# -------- FINAL RESULT --------
print("\n---------- SUMMARY ----------")
print(f"Total     : {len(df)}")
print(f"Success   : {success_count}")
print(f"Failed    : {fail_count}")
print(f"Runtime   : {runtime} seconds\n")