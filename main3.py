import re
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

# =========================
# 📂 FILE PATH
# =========================
file_path = "/Users/ashish/Desktop/Blitz Scripts/data/zero_fake.txt"

# =========================
# 🧾 PARSE CHAT
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
        if data:
            data[-1][3] += " " + line

df = pd.DataFrame(data, columns=["Date", "Time", "Sender", "Message"])

# =========================
# 📅 DATE CLEANING
# =========================
df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%y")
df["Date"] = df["Date"].dt.date

# =========================
# 📆 FILTER DATE RANGE
# =========================
start_date = dt.date(2026, 1, 15)
end_date   = dt.date(2026, 4, 15)

df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

# =========================
# 👥 TEAM MEMBERS
# =========================
team_members = [
    "Sanket Office",
    "Vishnu",
    "Ashish Office",
    "Sachin Verma🐣"
]

df_team = df[df["Sender"].isin(team_members)]

# =========================
# 📊 TOTAL RESPONSES
# =========================
responses = df_team["Sender"].value_counts()

print("\n=== Total Responses Per Person ===\n")
print(responses)

# =========================
# 📈 DISTRIBUTION %
# =========================
distribution = (responses / responses.sum()) * 100

print("\n=== Contribution (%) ===\n")
print(distribution.round(2))

# =========================
# 📦 TOTAL MESSAGES
# =========================
print("\n=== Total Messages by Team ===\n")
print(len(df_team))

# =========================
# 📊 BAR CHART
# =========================
responses.plot(kind="bar")

plt.title("Total Responses by Team Members")
plt.xlabel("Team Member")
plt.ylabel("Number of Responses")

plt.tight_layout()
plt.show()

# =========================
# 🥧 PIE CHART (BEST VIEW)
# =========================
distribution.plot(kind="pie", autopct="%1.1f%%")

plt.title("Response Distribution (%)")
plt.ylabel("")

plt.show()