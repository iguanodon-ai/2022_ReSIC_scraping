import os
import pandas as pd
import re
import sys
import requests, fitz
import time
from tqdm import tqdm
import shutil


DATA = "data"
RAW = os.path.join(DATA, "raw")
WORK = os.path.join(DATA, "work")
FINAL = os.path.join(DATA, "final")

if not os.path.exists(DATA):
    os.makedirs(RAW)
    os.makedirs(WORK)
    os.makedirs(FINAL)


def stats_raw(file, display_info=True):
    #print(file)
    if "csv" in file:
        df = pd.read_csv(file)
        if display_info:
            print(list(df.columns))
            #print(df.head())
            print()
        return df
   
def clean_url(url, acteur=None):
    urls = url.split()
    urls = list(set(urls))
    if acteur is not None:
        return urls[0]
    return urls


def clean_date(date, acteur):
    if acteur == "vluchtelingen":
        dates = date.split()
        dates = list(set(dates))
        dates = [date for date in dates if len(re.findall('\d+', date)) > 0] # we need one digit
        date = dates[0]

    elif acteur == "orbit":
        #print("orbit")
        ### We replace months by their number and do some cleaning
        date = date.lower()
        months = {"januari": "01", "februari": "02", "maart": "03", "april": "04", "mei": "05", "juni": "06", "juli": "07", "augustus": "08", "september": "09", "oktober": "10", "november": "11", "december": "12"}
        for month in months.keys():
            if month in date:
                date = date.replace(" "+month+" ", "-"+months[month]+"-")
        dates = date.split()
        try:
            date = dates[0]
        except IndexError:
            date = "00-00-0000"

    elif acteur == "ciré":
        date = date.lower()
        months = {"janvier": "01", "février": "02", "mars": "03", "avril": "04", "mai": "05", "juin": "06", "juillet": "07", "août": "08", "aout": "08", "septembre": "09", "octobre": "10", "novembre": "11", "décembre": "12"}
        for month in months.keys():
            if month in date:
                date = date.replace(" "+month+" ", "-"+months[month]+"-")
        dates = date.split()
        try:
            date = dates[0]
        except IndexError:
            date = "00-00-0000"
    return date

def clean_strings(texte):
    texte = texte.replace('<div class="onefield fieldacycaptcha"> Veuillez activer le javascript pour envoyer ce formulaire</div>', '')
    return texte 

def clean_titles(title):
    temp = (title + title).find(title, 1, -1)
    if temp != -1:
        cleaned = title[:temp]
        return cleaned
    else:
        return title

def parse_vluchtelingen(file):
    print(f"### We're dealing with file: {file}")
    df = stats_raw(file, False)
    #print(df.head())
    df.fillna('', inplace=True)
    if "DOCU" in file: 
        df = df.groupby('link', as_index=False).agg({'link' : 'first', 'date' : ' '.join, 'link-href' : ' '.join, 'texte' : ' '.join, 'link-pdf-href' : ' '.join})
        df["link-pdf-href"] = df["link-pdf-href"].apply(clean_url)
        
    else:
        df = df.groupby('link-href', as_index=False).agg({'link' : 'first', 'date' : ' '.join, 'link-href' : ' '.join, 'texte' : ' '.join})
    
    # Cleaning URLs
    df["link-href"] = df["link-href"].apply(clean_url, acteur="vluchtelingen")
    # Keeping them dates clean
    df["date"] = df["date"].apply(clean_date, acteur="vluchtelingen")
    #if "OPINIE" not in file:
    #    df["titre"] = df["titre"].apply(clean_titles)

    print(f"### {file} has {len(df)} entries")
    print()
    return df

def parse_orbit(file):
    print(f"### We're dealing with file: {file}")
    df = stats_raw(file, False)
    print(df.head())
    df.fillna('', inplace=True)
    df = df.groupby('link-href', as_index=False).agg({'link' : 'first', 'date' : ' '.join,  'titre' : ' '.join, 'texte' : ' '.join})
    
    # Keeping them dates clean
    df["date"] = df["date"].apply(clean_date, acteur="orbit")
    df["titre"] = df["titre"].apply(clean_titles)

    print(f"### {file} has {len(df)} entries")
    print()
    return df

def parse_ciré(file):
    print(f"### We're dealing with file: {file}")
    df = stats_raw(file, False)
    print(df.head())
    df.fillna('', inplace=True)
    
    if "PUB" in file: 
        df = df.groupby('lien-news-href', as_index=False).agg({'date' : ' '.join,  'titre' : ' '.join, 'lien-pdf-href': ' '.join, 'texte' : ' '.join})
        df["lien-pdf-href"] = df["lien-pdf-href"].apply(clean_url)        
    else:
        df = df.groupby('lien-news-href', as_index=False).agg({'date' : ' '.join,  'titre' : ' '.join, 'texte' : ' '.join})

    # Keeping them dates clean
    df["date"] = df["date"].apply(clean_date, acteur="ciré")

    # removing html
    df["texte"] = df["texte"].apply(clean_strings)
    df["titre"] = df["titre"].apply(clean_titles)

    print(f"### {file} has {len(df)} entries")
    print()
    return df

def get_pdf_txt(URL):
    response = requests.get(URL)
    with open("temp", 'wb') as f:
        f.write(response.content)
    try:
        with fitz.open("temp") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
    except:
        print(URL)
        sys.exit()

    time.sleep(3)
    try:
        os.remove("temp")
    except PermissionError:
        time.sleep(5)
        os.remove("temp")
    return text
