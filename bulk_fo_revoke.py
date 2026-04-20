import pandas as pd
import requests
import time

# -------- CONFIG --------

INPUT_FILE = "/Users/ashish/Downloads/query_result_2026-04-05T09_09_10.954363939Z.xlsx"

API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/Auth/FO_Access"

POOL = "ap-south-1_2nXMZRCaO"

DELAY = 0.4
MAX_RETRY = 3

# ------------------------


df = pd.read_excel(INPUT_FILE)

success = 0
failed = 0
results = []

for _, row in df.iterrows():

    org_id = str(row["org_id"])
    username = str(row["username"])

    headers = {
        "pool": POOL,
        "orgId": org_id,
        "Content-Type": "application/json"
    }

    payload = {
        "request_type": "delete_user_account",
        "payload": {
            "username": username
        }
    }

    retry = 0
    status = "failed"

    while retry < MAX_RETRY:
        try:
            response = requests.post(API_URL, json=payload, headers=headers)

            if response.status_code == 200:
                print(f"Access revoked for {username} (Org {org_id})")
                success += 1
                status = "success"
                break
            else:
                retry += 1
                time.sleep(1)

        except Exception:
            retry += 1
            time.sleep(1)

    if status != "success":
        print(f"Failed for {username} (Org {org_id})")
        failed += 1

    results.append({
        "org_id": org_id,
        "username": username,
        "status": status
    })

    time.sleep(DELAY)


report = pd.DataFrame(results)
report.to_csv("fo_access_revoke_report.csv", index=False)

print("----------- SUMMARY -----------")
print("Total:", len(df))
print("Success:", success)
print("Failed:", failed)