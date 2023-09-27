import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver


chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
chrome_options.add_argument("--no-sandbox")  # Disable sandboxing

# Set ChromeDriver path to /usr/local/bin/chromedriver (where it's installed)
driver = webdriver.Chrome(options=chrome_options)



# Accédez à la page Web
driver.get("https://www.proteinatlas.org/humanproteome/single-cell-type/blood+%26+immune+cells#t-cells")

Tcell_list=["T-cells","B-cells","NK-cells"]

# Attendez que la page soit chargée
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "genelist")))

target_a = driver.find_element_by_xpath('//a[contains(text(), "T-cells")]')

# Si la balise <a> est trouvée, récupère le texte de la balise <td> parente
if target_a:
    td_element = target_a.find_element_by_xpath('../..')  # Remonte deux niveaux jusqu'à la balise <td>
    td_text = td_element.text.strip()
    print(td_text)
else:
    print("Balise <a> avec 'T-cells' non trouvée.")


# # Parcourez la liste des gènes
# for type_cell in Tcell_list :
#     for gene in driver.find_elements_by(""):
#         # Extrayez le nom du gène
#         name = gene._find_element_by_css_selector("td:nth-child(2)").text
#         # Extrayez l'ID du gène
#         id = gene.find_element_by_class_name("geneid").text
#         # Extrayez le lien vers la page du gène
#         link = gene.find_element_by_class_name("genelink").get_attribute("href")

#     # Imprimez les informations extraites
#     print(f"Nom : {name}")
#     print(f"ID : {id}")
#     print(f"Lien : {link}")

# # Fermez le navigateur
driver.quit()
