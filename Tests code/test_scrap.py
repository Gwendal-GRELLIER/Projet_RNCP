import requests
from bs4 import BeautifulSoup
import pandas as pd

df= pd.DataFrame(columns=["Gene name","Gene description","Classical monocyte", "Non-classical monocyte", "Intermediate monocyte", "T-reg",
                  "Memory CD4 T-cell", "Naive CD4 T-cell", "Memory CD8 T-cell", "Naive CD8 T-cell",
                  "Memory B-cell", "Naive B-cell", "Myeloid DC", "NK-cell"])
# print(df)

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
                
def get_gene_name_and_description(html):
    # Analyse le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(html.text, "html.parser")
    
    gene_name = None
    gene_description = None
    ntpm = None
    liste = []
    # Recherche des balises <th> contenant les en-têtes
    th_keywidth_tags = soup.find_all("th", class_="keywidth")
    
    for th_tag in th_keywidth_tags:
        if "Gene name" in th_tag.text:
            # Si l'en-tête contient "Gene name", obtenir la valeur de la cellule suivante
            gene_name = th_tag.find_next("td").text.strip()
            # df.append(["Gene name".gene_name)
            liste.append(gene_name)
    # Recherche des balises <th> contenant les en-têtes
    th_tags = soup.find_all("th")
    
    for th_tag in th_tags:
        if "Gene description" in th_tag.text:
            # Si l'en-tête contient "Gene description", obtenir la valeur de la cellule suivante
            gene_description = th_tag.find_next("td").text.strip()
            # df["Gene description"].append(gene_description)
            liste.append(gene_description)
            break

    script_tags = soup.find_all("script")
    cell_types = ["Classical monocyte", "Non-classical monocyte", "Intermediate monocyte", "T-reg",
                  "Memory CD4 T-cell", "Naive CD4 T-cell", "Memory CD8 T-cell", "Naive CD8 T-cell",
                  "Memory B-cell", "Naive B-cell", "Myeloid DC", "NK-cell"]

    # Parcourir les balises <script> pour extraire les données
    for script_tag in script_tags:
        for cell_type in cell_types:
            if f'"label":"{cell_type}"' in script_tag.text:
                # Extraire la valeur TPM
                ntpm = script_tag.text.split(f'"label":"{cell_type}"')[1].split('"value":"')[1].split('"')[0]
                # print(ntpm)
                # df[f"{cell_type}"].append(ntpm)
                liste.append(ntpm)
                # Imprimer le label et la valeur TPM

        if ntpm:
            break
    df.loc[len(df)] = liste


    
for link in links:
    
    html = requests.get(f"https://www.proteinatlas.org{link}")

    get_gene_name_and_description(html)
print(df)
df.to_csv("Scraping.csv")

# print("NTPM:", ntpm)
# print("Gene Name:", gene_name)
# print("Gene Description:", gene_description)

