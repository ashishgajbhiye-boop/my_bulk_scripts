import requests

url = "https://35idc7phd7.execute-api.ap-south-1.amazonaws.com/V1/sarathyupdate/ridertransfer"

headers = {
    "node_id": "84",
    "name": "ashish",
    "Content-Type": "application/json"
}

payload = {
    "nodeId": 125,
    "riderIds": [26143]
}

try:
    response = requests.put(url, json=payload, headers=headers, timeout=10)
    print("Status:", response.status_code)
    print("Response:", response.text)

except requests.exceptions.ConnectionError:
    print("Network error: Cannot reach API. Check VPN or internet connection.")