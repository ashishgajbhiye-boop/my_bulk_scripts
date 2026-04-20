# Extract Date

df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%y")

# Remove time
df["Date"] = df["Date"].dt.date

# Filter by date range
import datetime as dt

start_date = dt.date(2026, 1, 15)
end_date   = dt.date(2026, 4, 15)

df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

#Custom Bi-Monthly Buckets

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

#Filter Team Members

team_members = [
    "Sanket Office",
    "Vishnu",
    "Ashish Office",
    "Sachin Verma🐣"
]

df_team = df[df["Sender"].isin(team_members)]

#Group Data

bucket_counts = df_team.groupby(["Bucket", "Sender"]).size().unstack(fill_value=0)

print(bucket_counts)

#Visualization

import matplotlib.pyplot as plt

bucket_counts = bucket_counts.reindex([
    "Jan 15-31",
    "Feb 01-15",
    "Feb 16-28",
    "Mar 01-15",
    "Mar 16-31",
    "Apr 01-15"
])

bucket_counts.plot(kind="bar", figsize=(12,6))

plt.title("Bi-Monthly Response Distribution")
plt.xlabel("Time Period")
plt.ylabel("Number of Responses")
plt.xticks(rotation=45)
plt.legend(title="Team Members")

plt.show()


/Users/ashish/Downloads/ofd_stuck_query_2026-04-13T12_38_00.326186437Z.xlsx