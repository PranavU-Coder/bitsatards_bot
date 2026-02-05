from bs4 import BeautifulSoup
import requests
import urllib3
import pandas as pd

# the site has some insecure/incomplete SSL certificate chain
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# change URL each year in accordance to new cutoff-data
URL = "https://admissions.bits-pilani.ac.in/FD/BITSAT_cutOffs.html?FQwp43qOeKhayi8LEQVUtJn3QNZ0TciWLP4NKxNMfcgzQdzcqZCCLqDBZRDnjcsHWFGgSC&yr=2025-2026&eKhayi8LEQwp4NKxN+CfCh+3qOVUtJn3QNZ0TciWLP4"

# static value for year chosen
year = 2025

html_text = requests.get(URL, verify=False).text
soup = BeautifulSoup(html_text, "lxml")

# to modify accordingly
div = soup.find("div", id="2025-2026")

data = []
tables = div.find_all("table")

for table in tables:
    rows = table.find_all("tr")

    # skip any tiny-tables in the way
    if len(rows) < 3:
        continue

    for row in rows[1:]:
        cols = row.find_all("td")

        if len(cols) >= 4:
            campus = cols[0].get_text(strip=True)
            program = cols[1].get_text(strip=True)
            cutoff = cols[2].get_text(strip=True)

            if "Goa" in campus:
                campus = "Goa"
            elif campus not in ["Pilani", "Goa", "Hyderabad"]:
                continue

            # validating if data row
            if cutoff.isdigit() and program.lower() != "program":
                data.append(
                    {
                        "campus": campus,
                        "branch": program,
                        "marks": int(cutoff),
                        "year": year,
                    }
                )

if data:
    df = pd.DataFrame(data)
    df = df.drop_duplicates()
    df.to_csv("bitsat_cutoffs.csv", index=False)
    print(df.head(10))
else:
    print("\ntask failed")
