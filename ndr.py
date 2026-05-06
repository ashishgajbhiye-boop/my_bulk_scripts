import pandas as pd
import requests
import time
import os

# =========================
# CONFIGURATION
# =========================

# Input file path (CSV or Excel)
INPUT_FILE = "/Users/ashish/Downloads/Workbook1.xlsx"   # change this

# API URL
URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/logistic/initiateNDR"

# Headers
HEADERS = {
    "Content-Type": "application/json"
}

# Delay between requests (seconds)
DELAY = 1


# =========================
# READ FILE
# =========================

def read_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(file_path)
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)
    else:
        raise Exception("Unsupported file format. Use CSV or Excel.")

    return df


# =========================
# API CALL FUNCTION
# =========================

def send_ndr_request(awb, lat, long):
    payload = {
        "ndrRequests": [
            {
                "awbNumber": str(awb),
                "ndrKey": "awbNumber",
                "googleMapAddressLink": None,
                "newAddress": None,
                "newContact": None,
                "newName": None,
                "newDate": None,
                "newpin": None,
                "newLat": str(lat),
                "newLong": str(long),
                "action": "Reattempt",
                "fakeAttempt": None,
                "proofAttachmentLink": None,
                "deliveryInstruction": None,
                "reAttemptSlot": None,
                "ndrInitiatedBy": "Support",
                "remarks": "ALS reRUN"
            }
        ]
    }

    try:
        response = requests.post(URL, json=payload, headers=HEADERS)

        if response.status_code == 200:
            print(f"SUCCESS → {awb}")
        else:
            print(f"FAILED → {awb} | Status: {response.status_code} | {response.text}")

    except Exception as e:
        print(f"ERROR → {awb} | {e}")


# =========================
# MAIN EXECUTION
# =========================

def main():
    df = read_file(INPUT_FILE)

    print(f"Total records found: {len(df)}")
    print("Starting bulk NDR requests...\n")

    for index, row in df.iterrows():

        awb = row["awb"]
        lat = row["latitude"]
        long = row["longitude"]

        send_ndr_request(awb, lat, long)

        # delay
        time.sleep(DELAY)

    print("\nCompleted.")


# =========================

if __name__ == "__main__":
    main()

    # awb	latitude	longitude