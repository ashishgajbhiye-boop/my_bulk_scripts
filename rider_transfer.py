import requests

url = "https://0fs16zlyvk.execute-api.ap-south-1.amazonaws.com/V1/sarathy/ridertransfer"

headers = {
    "node_id": "20",
    "name": "ashish",
    "Content-Type": "application/json"
}

payload = {
    "nodeId": 305,
    "riderIds": [3117]
}

try:
    response = requests.put(url, json=payload, headers=headers, timeout=10)
    print("Status:", response.status_code)
    print("Response:", response.text)

except requests.exceptions.ConnectionError:
    print("Network error: Cannot reach API. Check VPN or internet connection.")