
import requests
from bs4 import BeautifulSoup

def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a", title=lambda title: title != None and "Immune cell" in title)
    return [link["href"] for link in links]

links = get_links("https://www.proteinatlas.org/search/cell_type_category_rna%3AT-cells%2CB-cells%2CPlasma+cells%2CNK-cells%2Cgranulocytes%2Cmonocytes%2CMacrophages%2CHofbauer+cells%2CKupffer+cells%2Cdendritic+cells%2CLangerhans+cells%2CErythroid+cells%3BCell+type+enriched%2CGroup+enriched%2CCell+type+enhanced+AND+show_columns%3Atissuespecificity+AND+sort_by%3Atissue+specific+score")

for link in links:
    print(link)