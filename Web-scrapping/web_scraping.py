# Importation des bibliothèques nécessaires
import requests  
from bs4 import BeautifulSoup  
import pandas as pd  

# Initialisation d'un DataFrame pandas avec les colonnes nécessaires
df = pd.DataFrame(columns=["Gene name", "Gene description", "Classical monocyte", "Non-classical monocyte",
                           "Intermediate monocyte", "T-reg", "Memory CD4 T-cell", "Naive CD4 T-cell",
                           "Memory CD8 T-cell", "Naive CD8 T-cell", "Memory B-cell", "Naive B-cell",
                           "Myeloid DC", "NK-cell"])

# Fonction pour extraire les liens des cellules immunitaires à partir d'une URL donnée
def get_links(url):
    # Envoyer une requête GET à l'URL spécifiée
    response = requests.get(url)
    # Analyser la réponse HTML avec BeautifulSoup
    global soup
    soup = BeautifulSoup(response.content, "html.parser")
    # Trouver tous les liens contenant "Immune cell" dans leur attribut title
    links = soup.find_all("a", title=lambda title: title != None and "Immune cell" in title)
    # Retourner une liste des liens trouvés
    return [link["href"] for link in links]

# Fonction pour obtenir tous les liens des pages contenant des informations sur les cellules immunitaires
def get_all_links(url):
    # Initialiser une liste pour stocker les liens
    links = []
    # Numéro de page initial
    page_num = 1
    # Boucler jusqu'à ce qu'il n'y ait plus de page suivante
    while True:
        # Construire l'URL de la page actuelle
        url_page = url + f"/{page_num}"
        # Obtenir les liens de la page actuelle
        new_links = get_links(url_page)
        # Ajouter les nouveaux liens à la liste principale
        links.extend(new_links)
        # Trouver le lien vers la page suivante
        next_page_link = soup.find("a", string="next »")
        # Sortir de la boucle si aucun lien vers la page suivante n'est trouvé
        if next_page_link is None:
            break
        # Passer à la page suivante
        page_num += 1
    # Retourner la liste complète des liens
    return links

# Appeler la fonction pour obtenir tous les liens des pages contenant des informations sur les cellules immunitaires
links = get_all_links("https://www.proteinatlas.org/search/cell_type_category_rna%3AT-cells%2CB-cells%2CPlasma+cells%2CNK-cells%2Cgranulocytes%2Cmonocytes%2CMacrophages%2CHofbauer+cells%2CKupffer+cells%2Cdendritic+cells%2CLangerhans+cells%2CErythroid+cells%3BCell+type+enriched%2CGroup+enriched%2CCell+type+enhanced+AND+sort_by%3Atissue+specific+score")
# Afficher le nombre total de liens obtenus
print(len(links))

# Fonction pour obtenir le nom et la description du gène à partir du contenu HTML
def get_gene_name_and_description(html):
    # Analyser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(html.text, "html.parser")
    
    # Initialiser les variables pour stocker le nom et la description du gène
    gene_name = None
    gene_description = None
    ntpm = None
    liste = []  # Initialiser une liste pour stocker les valeurs
    
    # Rechercher les balises <th> contenant les en-têtes
    th_keywidth_tags = soup.find_all("th", class_="keywidth")
    
    # Parcourir les balises <th> pour extraire le nom du gène
    for th_tag in th_keywidth_tags:
        if "Gene name" in th_tag.text:
            # Si l'en-tête contient "Gene name", obtenir la valeur de la cellule suivante
            gene_name = th_tag.find_next("td").text.strip()
            # Ajouter le nom du gène à la liste
            liste.append(gene_name)
    
    # Rechercher les balises <th> contenant les en-têtes
    th_tags = soup.find_all("th")
    
    # Parcourir les balises <th> pour extraire la description du gène
    for th_tag in th_tags:
        if "Gene description" in th_tag.text:
            # Si l'en-tête contient "Gene description", obtenir la valeur de la cellule suivante
            gene_description = th_tag.find_next("td").text.strip()
            # Ajouter la description du gène à la liste
            liste.append(gene_description)
            break

    # Rechercher toutes les balises <script>
    script_tags = soup.find_all("script")
    cell_types = ["Classical monocyte", "Non-classical monocyte", "Intermediate monocyte", "T-reg",
                  "Memory CD4 T-cell", "Naive CD4 T-cell", "Memory CD8 T-cell", "Naive CD8 T-cell",
                  "Memory B-cell", "Naive B-cell", "Myeloid DC", "NK-cell"]

    # Parcourir les balises <script> pour extraire les données des différents types de cellules
    for script_tag in script_tags:
        for cell_type in cell_types:
            # Vérifier si le type de cellule actuel est présent dans le contenu du script
            if f'"label":"{cell_type}"' in script_tag.text:
                # Extraire la valeur TPM associée au type de cellule
                ntpm = script_tag.text.split(f'"label":"{cell_type}"')[1].split('"value":"')[1].split('"')[0]
                # Ajouter la valeur TPM à la liste
                liste.append(ntpm)

        # Sortir de la boucle si ntpm est défini
        if ntpm:
            break
    
    # Ajouter les valeurs extraites à un nouveau ligne dans le DataFrame
    df.loc[len(df)] = liste

# Parcourir tous les liens des pages contenant des informations sur les cellules immunitaires
for link in links:
    # Envoyer une requête GET à l'URL spécifique du lien
    html = requests.get(f"https://www.proteinatlas.org{link}")

    # Appeler la fonction pour obtenir le nom et la description du gène
    get_gene_name_and_description(html)

# Afficher le DataFrame contenant toutes les informations extraites
print(df)

# Exporter le DataFrame au format CSV
df.to_csv("Scraping.csv")
