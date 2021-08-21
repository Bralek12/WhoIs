import csv
import bs4
import requests


def write_to_file(input_list):
    with open("list_of_addresses.csv", "w") as csv_file:
        headers = (["IP Address", "Response", "Country", "City", "Address", "PostalCode"])
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for element in input_list:
            writer.writerow(element)


def get_element(element, res):
    try:
        searched_line = ([c for c in res if element in c][0]).split()
        if len(searched_line) > 1:
            return " ".join(searched_line[1:])
        else:
            return "No result"
    except IndexError:
        return "No result"


list_of_ads = []
with open("ip_list.txt", "r") as ip_list:
    for line in ip_list.readlines():
        list_of_ads.append(line[:-1])

result_dict = []
number = 0
for ip_ad in list_of_ads:
    my_pre = bs4.BeautifulSoup(requests.get(f"https://who.is/whois-ip/ip-address/{ip_ad}").text, "lxml").find("pre")
    print(number)
    number += 1
    if my_pre:
        result = my_pre.get_text().split("\n")
        result_dict.append({"IP Address": ip_ad,
                            "Response": "YES",
                            "Country": get_element("Country:", result),
                            "City": get_element("City:", result),
                            "Address": get_element("Address:", result),
                            "PostalCode": get_element("PostalCode:", result)})
    else:
        result_dict.append({"IP Address": ip_ad, "Response": "NO",
                            "Country": 0,
                            "City": 0,
                            "Address": 0,
                            "PostalCode": 0})

write_to_file(result_dict)

