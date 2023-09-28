import requests
from bs4 import BeautifulSoup

def get_gene_name_and_description(html):
    soup = BeautifulSoup(html.text, "html.parser")
    #print(soup)
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




#  # Recherche des balises <text> avec la classe "barchartlabel"
#     text_tags = soup.find_all("text", class_="barchartlabel")
#     print(text_tags)
#     for text_tag in text_tags:
#         # Vérifiez si le texte contient "nTPM:"
#         if "nTPM:" in text_tag.get("title") and "Classical monocyte" in text_tag.get("title") :
#             # Si oui, extrayez la valeur de nTPM
#             title = text_tag.get("title")
#             ntpm = title.split("nTPM:")[1].split("<br>")[0].strip()
#               # Sortir de la boucle après avoir trouvé la première occurrence
#             break
    script_tags = soup.find_all("script")
    cell_types = ["Classical monocyte", "Non-classical monocyte", "Intermediate monocyte", "T-reg", "Memory CD4 T-cell", "Naive CD4 T-cell", "Memory CD8 T-cell", "Naive CD8 T-cell", "Memory B-cell", "Naive B-cell", "Myeloid DC", "NK-cell"]
    # Parcourir les balises <script> pour extraire les données
    for script_tag in script_tags:
        
        for cell_type in cell_types :
            if f'"label":"{cell_type}"' in script_tag.text:
                # Si "Classical monocyte" est trouvé dans la balise <script>
                # Extraire le texte entre <b> et </b> pour obtenir le label
                label_start = script_tag.text.find("<b>") + len("<b>")
                label_end = script_tag.text.find("</b>")
                label = script_tag.text[label_start:label_end]

                # Extraire la valeur TPM
                ntpm = script_tag.text.split(f'"label":"{cell_type}"')[1].split('"value":"')[1].split('"')[0]
                # tpm_end = script_tag.text.find("<br>", tpm_start)
                # tpm = script_tag.text[tpm_start:tpm_end].strip()
                print(ntpm)
                # Imprimer le label et la valeur TPM


        if f'"label":"{cell_type}"' in script_tag.text:
            break
            
            
            
        


    return gene_name , gene_description ,ntpm


# Exemple d'utilisation :

html = requests.get("https://www.proteinatlas.org/ENSG00000161610-HCRT/immune+cell")

gene_name, gene_description, ntpm= get_gene_name_and_description(html)

print(ntpm)

print(gene_name)
print(gene_description)
