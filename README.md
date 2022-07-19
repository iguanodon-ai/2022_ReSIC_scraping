<a href="https://iguanodon.ai"><img src="img/iguanodon.ai.png" width="125" height="125" align="right" /></a>

# Scraping et mise en forme ALCESTE de données web

## Description

Ce repository contient le code créé dans le cadre d'une mission de récupération et de mise en forme d'un corpus web au format [ALCESTE [pdf]](http://www.image-zafar.com/images/formatage_alceste.pdf). 

## Étapes

Ce projet comporte deux grandes étapes : la récupération des données sur les sites des acteurs (_web scraping_), et le formattage de ces données en format ALCESTE. 

### Récupérer les données

1. Installer l'extension Chrome [webscraper.io](webscraper.io)
2. Importer plusieurs `sitemaps` : un site map pour chaque ligne dans les fichier `sitemaps` 
3. Pour chaque `sitemap`, lancer le scraping et placer l'export du scraping en format `csv` dans `data/raw`

### Formatter les données

1. `main.py` fait appel à différentes fonctions dans `utils.py`. Le script prend deux arguments possibles:
    1. `DF` (`python main.py DF`), qui formattera tous les exports CSV pour chaque site dans le même format, et si besoin va extraire le texte d'un PDF (dans le cas d'une page Web qui a une pièce-jointe en PDF)
    2. `ALCESTE` (`python main.py ALCESTE`), qui lira tous les fichiers créés à l'étape décrite ci-dessus et qui produira les fichiers au format ALCESTE requis dans `data/final`: un fichier par acteur, et un fichier par langue.



## Licence et contact

Ce code a été écrit par Simon Hengchen ([https://iguanodon.ai](https://iguanodon.ai)) à la commande de Cécile Balty ([Université libre de Bruxelles](https://www.ulb.be/fr/cecile-balty)). Ce code est mis à disposition du public <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">sous licence permissive CC BY-SA 4.0</a>. 


 <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
