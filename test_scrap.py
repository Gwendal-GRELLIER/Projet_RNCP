import requests
from bs4 import BeautifulSoup

def get_gene_name_and_description(html):
    soup = BeautifulSoup(html.text, "html.parser")

    gene_name = None
    gene_description = None
    ntpm = None

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




 # Recherche des balises <text> avec la classe "barchartlabel"
    text_tags = soup.find_all("text", class_="barchartlabel")
    print(text_tags)
    for text_tag in text_tags:
        # Vérifiez si le texte contient "nTPM:"
        if "nTPM:" in text_tag.get("title") and "Classical monocyte" in text_tag.get("title") :
            # Si oui, extrayez la valeur de nTPM
            title = text_tag.get("title")
            ntpm = title.split("nTPM:")[1].split("<br>")[0].strip()
              # Sortir de la boucle après avoir trouvé la première occurrence
            break


    return gene_name, gene_description ,ntpm


# Exemple d'utilisation :

html = requests.get("https://www.proteinatlas.org/ENSG00000101981-F9/immune+cell")

gene_name, gene_description, ntpm= get_gene_name_and_description(html)

print(ntpm)

print(gene_name)
print(gene_description)
