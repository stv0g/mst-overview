# %%

token = "df8f82c719ece3df8ff58dbc6cdebc21"

# %%

import httpx

query = {
    "module": "API",
    "token_auth": token,
    "method": "Live.getLastVisitsDetails",
    "idSite": "3",
    "period": "month",
    "date": "today",
    "format": "JSON",
    "filter_limit": "-1",
}
response = httpx.get("https://matomo.schuetze.link/index.php", params=query)
response.raise_for_status()
data = response.json()

# %%

from collections import Counter
import idna
import re

all_domains = list()
all_first = list()
for i in data:
    urls = [action["url"] for action in i["actionDetails"]]
    if any(
        not re.match("https://[a-z-]+\.meine-stadt-transparent.de", url) for url in urls
    ):
        continue
    domains = [idna.decode(url.split("/")[2]).split(".")[0] for url in urls]
    all_domains.extend(domains)
    all_first.append(domains[0])
all_domains = Counter(all_domains)
all_first = Counter(all_first)
print(all_domains)
print(all_first)

#%%

import numpy
import matplotlib.pyplot as plt

labels = list(set(all_domains.keys()) | set(all_first.keys()))
labels.sort(key=lambda x: all_first.get(x, 0))
visitor_values = [all_domains.get(label, 0) for label in labels]
actions_values = [all_first.get(label, 0) for label in labels]

x = numpy.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()

rects1 = ax.barh(x - width / 2, visitor_values, width, label="By action")
rects2 = ax.barh(x + width / 2, actions_values, width, label="By visitor")

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_yticks(x)
ax.set_yticklabels(labels)
ax.legend()
fig.tight_layout()
plt.title("Visitors and actions per city in the last month")
plt.show()

#%%

import pandas

existing = pandas.read_csv("existing.csv").fillna("")
print(sorted(list(existing["name"])))
print(sorted(all_domains.keys()))
print(set(i.lower() for i in sorted(list(existing["name"]))) - all_domains.keys())
