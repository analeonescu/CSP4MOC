'''This script queries the ChemRxiv API for entries containing
a specific term (e.g., "ammonia") within a specified date range.
It retrieves the title and DOI of each entry and saves the 
results to a CSV file. The script handles pagination by querying 
in 7-day intervals, ensuring that it does not exceed the API's 
limit of 50 entries per request.'''

import requests
from datetime import datetime, timedelta
import time
import pandas as pd

query = "ammonia"  # this is what you type in the browser to 'Search' 
# - it can appear anywhere in the entry, not necessarily in the title!!!!
start_date = datetime.strptime("2026-04-16", "%Y-%m-%d")
end_date = datetime.today()

current_date = start_date
results = []

while current_date <= end_date:
    from_date = current_date.strftime("%Y-%m-%d")
    to_date = (current_date + timedelta(days=6)).strftime("%Y-%m-%d")  # 7-day range
    print(f"\nFetching entries from {from_date} to {to_date}...")

    url = (
        f'https://chemrxiv.org/engage/chemrxiv/public-api/v1/items'
        f'?term="{query}"'
        f'&searchDateFrom={from_date}'
        f'&searchDateTo={to_date}'
        f'&limit=50' # unfortunately the api can return a maximum of 50 entries at once, 
        # but we can loop through it depending on the dates chosen
    )

    r = requests.get(url)
    data = r.json()

    hits = data.get("itemHits", [])
    print(f"  Found {len(hits)} entries (before filtering).")

    count = 0
    for hit in hits:
        item = hit.get("item", {})
        title = item.get("title", "No title")
        doi = item.get("doi", "")  # can extract more data, just look at something like data['itemHits'][0]['item']

        # filter to include only titles that contain the query term if you want:
        # if query.lower() in title.lower():
        results.append({"date": from_date, "title": title, "doi": doi})
        count += 1
        print(f"    {count}. {title}")

    current_date += timedelta(days=7)
    time.sleep(0.2) # to make sure the server doesn't crash

df = pd.DataFrame(results)
df.to_csv('Test_ammonia.csv', index=False)

