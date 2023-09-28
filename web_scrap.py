
# import requests
# from bs4 import BeautifulSoup

# def get_links(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")
#     links = soup.find_all("a", title=lambda title: title != None and "Immune cell" in title)
#     return [link["href"] for link in links]

# links = get_links("https://www.proteinatlas.org/search/cell_type_category_rna%3AT-cells%2CB-cells%2CPlasma+cells%2CNK-cells%2Cgranulocytes%2Cmonocytes%2CMacrophages%2CHofbauer+cells%2CKupffer+cells%2Cdendritic+cells%2CLangerhans+cells%2CErythroid+cells%3BCell+type+enriched%2CGroup+enriched%2CCell+type+enhanced+AND+show_columns%3Atissuespecificity+AND+sort_by%3Atissue+specific+score")

# for link in links:
#     print(link)


import requests
from bs4 import BeautifulSoup

def get_links(url):
    response = requests.get(url)
    global soup
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a", title=lambda title: title != None and "Immune cell" in title)
    return [link["href"] for link in links]

def get_all_links(url):
    links = []
    page_num = 1
    while True:
        url_page = url + f"/{page_num}"
        new_links = get_links(url_page)
        links.extend(new_links)
        next_page_link = soup.find("a", string="next »")
        if next_page_link is None:
            break
        page_num += 1
    return links

links = get_all_links("https://www.proteinatlas.org/search/cell_type_category_rna%3AT-cells%2CB-cells%2CPlasma+cells%2CNK-cells%2Cgranulocytes%2Cmonocytes%2CMacrophages%2CHofbauer+cells%2CKupffer+cells%2Cdendritic+cells%2CLangerhans+cells%2CErythroid+cells%3BCell+type+enriched%2CGroup+enriched%2CCell+type+enhanced+AND+sort_by%3Atissue+specific+score")
print(len(links))
for link in links:
    target_page = requests.get(f"https://www.proteinatlas.org{link}")
    source = BeautifulSoup(target_page.content, "html.parser")
    infos = source.find


    
