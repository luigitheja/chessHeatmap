import requests
from bs4 import BeautifulSoup
import requests, zipfile, io
import os

def download_file(file_url, dwnld_path):
    
    fname = file_url.split("/")[-1].replace(".zip",".pgn")
    # print("file path",os.path.join(dwnld_path,fname), "file exists", os.path.exists(os.path.join(dwnld_path, fname)))
    # exit()
    # return
    if os.path.exists(os.path.join(dwnld_path,fname)):
        return "already present", file_url    
    try:
        r = requests.get(file_url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(dwnld_path)
    except Exception as e:
        print(e)
        return "cannot download", file_url

    return "ok", file_url



URL = "https://www.pgnmentor.com/files.html"
r = requests.get(URL)
#print(r.content)
soup = BeautifulSoup(r.content, 'html.parser')
#print(soup.prettify())
links=soup.find_all('a',href=True)

links = [x['href'] for x in links if 'zip' in x['href']]

links = list(set(links))



base_url = "https://www.pgnmentor.com/"

for link in links:
    print(link)
    full_link = base_url + link
    output_folder  = "D:\programs\chess pgn dataset\scraped_games"
    print(download_file(full_link, output_folder))