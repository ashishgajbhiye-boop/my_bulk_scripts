import requests
import time

# -------- CONFIG --------

API_URL = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/ndr"

# Enter AWBs here (comma separated)
awb_numbers = "GNN758222277"

# New Address
NEW_ADDRESS = "11th Floor, Flat No. 1118, Panchsheel Building, Opposite Gautam Nagar, Mumbai"

DELAY = 0.3

# ------------------------

headers = {
    "Content-Type": "application/json"
}

awb_list = [x.strip() for x in awb_numbers.split(",")]

success = 0
failed = 0

for awb in awb_list:

    payload = {
        "ndrRequests": [
            {
                "awbNumber": awb,
                "shipmentId": None,
                "ndrKey": None,
                "action": "Reattempt",
                "fakeAttempt": False,
                "shipperId": None,
                "ndrInitiatedBy": "Shipper",
                "createdAt": None,
                "remarks": "Address updated by support",
                "newAddress": NEW_ADDRESS,
                "newContact": None,
                "newName": None,
                "newDate": None,
                "newpin": None,
                "newLat": None,
                "newLong": None,
                "newEmail": None,
                "googleMapAddressLink": None,
                "proofAttachmentLink": None,
                "reAttemptSlot": None,
                "deliveryInstruction": None
            }
        ]
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            print(f"✔ Address Updated: {awb}")
            success += 1
        else:
            print(f"✖ Failed: {awb} | Status: {response.status_code}")
            print(response.text)
            failed += 1

    except Exception as e:
        print(f"Error for {awb}: {e}")
        failed += 1

    time.sleep(DELAY)

print("\n------ SUMMARY ------")
print("Total AWBs:", len(awb_list))
print("Success:", success)
print("Failed:", failed)