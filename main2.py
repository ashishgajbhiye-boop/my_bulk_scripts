import re
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

# =========================
# 📂 FILE PATH
# =========================
file_path = "/Users/ashish/Desktop/Blitz Scripts/data/kapthaan_quick.txt"

# =========================
# 🧾 STEP 1: PARSE CHAT
# =========================
pattern = r"\[(\d{2}/\d{2}/\d{2}), (.*?)\] (.*?): (.*)"

data = []

with open(file_path, encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    line = line.strip()

    match = re.match(pattern, line)
    
    if match:
        date, time, sender, message = match.groups()
        data.append([date, time, sender, message])
    else:
        # Handle multiline messages
        if data:
            data[-1][3] += " " + line

# Create DataFrame
df = pd.DataFrame(data, columns=["Date", "Time", "Sender", "Message"])

# =========================
# 📅 STEP 2: CLEAN DATE
# =========================
df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%y")
df["Date"] = df["Date"].dt.date  # Remove time

# =========================
# 📆 STEP 3: FILTER DATE RANGE
# =========================
start_date = dt.date(2026, 1, 15)
end_date   = dt.date(2026, 4, 15)

df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

# =========================
# 🪜 STEP 4: CREATE BUCKETS
# =========================
def assign_bucket(date):
    if dt.date(2026,1,15) <= date <= dt.date(2026,1,31):
        return "Jan 15-31"
    elif dt.date(2026,2,1) <= date <= dt.date(2026,2,15):
        return "Feb 01-15"
    elif dt.date(2026,2,16) <= date <= dt.date(2026,2,28):
        return "Feb 16-28"
    elif dt.date(2026,3,1) <= date <= dt.date(2026,3,15):
        return "Mar 01-15"
    elif dt.date(2026,3,16) <= date <= dt.date(2026,3,31):
        return "Mar 16-31"
    elif dt.date(2026,4,1) <= date <= dt.date(2026,4,15):
        return "Apr 01-15"
    else:
        return None

df["Bucket"] = df["Date"].apply(assign_bucket)

# =========================
# 👥 STEP 5: FILTER TEAM
# =========================
team_members = [
    "Sanket Office",
    "Vishnu",
    "Ashish Office",
    "Sachin Verma🐣"
]

df_team = df[df["Sender"].isin(team_members)]

# =========================
# 📊 STEP 6: RESPONSE COUNT
# =========================
responses = df_team["Sender"].value_counts()

print("\n=== Total Responses Per Person ===\n")
print(responses)

# =========================
# 📈 STEP 7: DISTRIBUTION %
# =========================
distribution = (responses / responses.sum()) * 100

print("\n=== Distribution (%) ===\n")
print(distribution.round(2))

# =========================
# 📊 STEP 8: BUCKET ANALYSIS
# =========================
bucket_counts = df_team.groupby(["Bucket", "Sender"]).size().unstack(fill_value=0)

# Order buckets properly
bucket_order = [
    "Jan 15-31",
    "Feb 01-15",
    "Feb 16-28",
    "Mar 01-15",
    "Mar 16-31",
    "Apr 01-15"
]

bucket_counts = bucket_counts.reindex(bucket_order)

print("\n=== Bi-Monthly Breakdown ===\n")
print(bucket_counts)

# =========================
# 📉 STEP 9: PLOT GRAPH
# =========================
bucket_counts.plot(kind="bar", figsize=(12,6))

plt.title("Bi-Monthly Response Distribution")
plt.xlabel("Time Period")
plt.ylabel("Number of Responses")
plt.xticks(rotation=45)
plt.legend(title="Team Members")

plt.tight_layout()
plt.show()