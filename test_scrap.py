import requests
from bs4 import BeautifulSoup

def get_gene_name_and_description(html):
    soup = BeautifulSoup(html.text, "html.parser")

    gene_name = None
    gene_description = None

    # Recherche des balises <th> contenant les en-têtes
    th_tags = soup.find_all("th", class_="keywidth")
    for th_tag in th_tags:
        if "Gene name" in th_tag.text:
            # Si l'en-tête contient "Gene name", obtenir la valeur de la cellule suivante
            gene_name = th_tag.find_next("td").text.strip()

    # Recherche des balises <th> contenant les en-têtes
    th_tags = soup.find_all("th", )
    for th_tag in th_tags:
        if "Gene description" in th_tag.text:
            # Si l'en-tête contient "Gene description", obtenir la valeur de la cellule suivante
            gene_description = th_tag.find_next("td").text.strip()
            break

    return gene_name, gene_description

# Exemple d'utilisation :

html = requests.get("https://www.proteinatlas.org/ENSG00000101981-F9/immune+cell")

gene_name, gene_description = get_gene_name_and_description(html)

print(gene_name)
print(gene_description)
