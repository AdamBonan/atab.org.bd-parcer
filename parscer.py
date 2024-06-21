import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


def decode_cf_email(encoded_string):
    r = int(encoded_string[:2], 16)
    email = ''.join([chr(int(encoded_string[i:i+2], 16) ^ r) for i in range(2, len(encoded_string), 2)])
    return email


url = "https://www.atab.org.bd/membership-directory"
content = requests.get(url).content
soup = bs(content, "lxml")
tables = soup.find("table", {"id": "example"}).find("tbody").find_all("tr")

data_csv = {
    "Owner name": [],
    "Agency name": [],
    "Email": [],
    "Address": [],
    "Telephone": [],
    "Telephone 2": [],
    "Thumbnail image URL": []
}

for table in tables:

    data = table.find_all("td")
    info = data[2]

    avatar_img = data[0].find("img")["src"]
    owner = data[1].text.replace("Owner:", "").strip()
    agency_name = info.text.split(":")[1].replace("Email", "").strip()
    email = decode_cf_email(info.find("a")["data-cfemail"])
    number = info.text.split(":")[3].strip().split(",")
    address = data[3].text.replace("Address:", "").strip()

    if len(number) == 2:
        number1 = number[0]
        number2 = number[1]
    else:
        number1 = number
        number2 = None

    data_csv["Owner name"].append(owner)
    data_csv["Agency name"].append(agency_name)
    data_csv["Email"].append(email)
    data_csv["Address"].append(address)
    data_csv["Telephone"].append(number1)
    data_csv["Telephone 2"].append(number2)
    data_csv["Thumbnail image URL"].append(avatar_img)


df = pd.DataFrame(data_csv)
df.to_csv('data.csv', index=False)