from bs4 import BeautifulSoup as bs # importing BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import argparse
import time
N = 10
#Variable pour le nombre de commentaires à récupérer

def get_video_info(url):
    s=Service(ChromeDriverManager().install())
    options = Options()
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(url)
    soup = bs(driver.page_source, "html.parser")
    result = {}
    result["Titre"] = soup.find("meta", itemprop="name")['content']
    result["Nombre de vues"] = soup.find("meta", itemprop="interactionCount")['content']
    result["Description"] = soup.find("meta", itemprop="description")['content']
    result["Nom de la chaine"] = soup.find("span", itemprop="author").next.next['content']
    result["ID de la video"] = soup.find("meta", itemprop="videoId")['content']
    #Commentaires
    commentaires = []
    element = driver.find_element(By.XPATH, "//*[@id=\"comments\"]")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    soup = bs(driver.page_source, 'html.parser')
    commentsList = soup.find_all("ytd-comment-thread-renderer", {"class": "style-scope ytd-item-section-renderer"}, limit = N)
    while commentsList == []:
        time.sleep(1)
        soup = bs(driver.page_source, 'html.parser')
        commentsList = soup.find_all("ytd-comment-thread-renderer", {"class": "style-scope ytd-item-section-renderer"}, limit = N)
    for comment in commentsList:
        commentaires.append(comment.find("yt-formatted-string", {"id": "content-text"}).text)
    result["Commentaires"] = commentaires
    raw_like = soup.find('button', class_="yt-spec-button-shape-next yt-spec-button-shape-next--tonal yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading yt-spec-button-shape-next--segmented-start")
    like = raw_like['aria-label']
    if like[0] == 'C':
        nb_like = like.split("Cliquez sur \"J'aime\" pour cette vidéo comme ")[1].split("autres internautes.")[0]
    else:
        nb_like = like.split("like this video along with ")[1].split("other people")[0]
    result["Nombre de likes"] = nb_like
    driver.quit()
    return result

parser = argparse.ArgumentParser() #on crée un objet parser
parser.add_argument('--input', help='Input JSON file with URLs', required=True) #on ajoute un argument à parser qui est le fichier d'entrée
parser.add_argument('--output', help='Output JSON file with data', required=True) #on ajoute un argument à parser qui est le fichier de sortie
args = parser.parse_args()
argdict = vars(args)
input_parameter = argdict['input']
output_parameter = argdict['output']

with open(input_parameter) as mon_fichier:
    urls = json.load(mon_fichier)

out = [] #output avec toutes les infos des videos

for url in urls: #on parcourt toutes les urls
    for i in urls[url]: #on parcourt toutes les videos de chaque url
        video_url = "https://www.youtube.com/watch?v=" + i #on construit l'url de la video
        data = get_video_info(video_url) #on récupère les infos de la video
        out.append(data) #on ajoute les infos de la video dans le output

with open(output_parameter, 'w') as outfile: #pn ouvre le fichier output
	json.dump(out, outfile, indent=4) #on écrit les données dans le fichier output