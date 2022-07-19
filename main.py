from utils import *

if __name__ == "__main__":
    
    if sys.argv[1] == "DF": 

        for SOURCE in ["orbit", "cire", "vluchtelingen"]:


            files = [file for file in os.listdir(RAW) if SOURCE in file]

            dfs = []
            for file in files:
                if SOURCE == "vluchtelingen":
                    df = parse_vluchtelingen(os.path.join(RAW,file))
                if SOURCE == "cire":
                    df = parse_ciré(os.path.join(RAW,file))
                if SOURCE == "orbit":
                    df = parse_orbit(os.path.join(RAW,file))
            
                if "ACTUS" in file:
                    df['Category'] = "actualités"
                if "COMMU" in file:
                    df['Category'] = "presse"
                if "PUB" in file:
                    df['Category'] = "publications"
                if "NIEUWS" in file:
                    df['Category'] = "nieuws"
                if "DOCU" in file:
                    df['Category'] = "documentatie"
                if "AGENDA" in file:
                    df['Category'] = "agenda"
                if "OPINIE" in file:
                    df['Category'] = "opinie"
                dfs.append(df)

            df = pd.concat(dfs)
            TOTAL = len(df)

            x = 0

            if SOURCE == "orbit":
                df.to_csv(os.path.join(WORK,SOURCE+".tsv"), sep="\t")
                break

            for i, row in tqdm(df.iterrows(), total=TOTAL):
                if SOURCE == "cire":
                    lien_pdf = "lien-pdf-href"
                if SOURCE == "vluchtelingen":
                    lien_pdf = "link-pdf-href"

                try:    
                    if not pd.isna(row[lien_pdf]):
                        x += 1
                        texte = " "
                        for url in row[lien_pdf]:
                            if url.endswith(".pdf"):
                                texte += " "+ get_pdf_txt(url)
                        row["texte"] = row["texte"] + texte
                except ValueError:
                    x += 1
                    texte = " "
                    for url in row[lien_pdf]:
                        if url.endswith(".pdf"):
                            texte += " "+ get_pdf_txt(url)
                    row["texte"] = row["texte"] + texte


            df.to_csv(os.path.join(WORK,SOURCE+".tsv"), sep="\t")
    
    elif sys.argv[1] == "ALCESTE":
        
        ### one file per actor
        files = os.listdir(WORK)
        print(files)
        for file in files:
            ACTEUR = file.replace(".tsv", "")
            df = pd.read_csv(os.path.join(WORK, file), sep="\t")
            print(df.head())
            print(df.columns)
            path_out = os.path.join(FINAL, ACTEUR+".txt")
            f_out = open(path_out, "w")
            for i, row in df.iterrows():
                #if i > 4:
                #    sys.exit()
                content = "**** *article_"+str(i)
                content += " *date_"+row["date"]
                content += " *année_"+row["date"].split("-")[-1]
                content += " *catégorie_"+row["Category"]
                if ACTEUR == "orbit" or ACTEUR == "vluchtelingen":
                    content += " *URL_"+row["link-href"]
                if ACTEUR == "cire":
                    content += " *URL_"+row["lien-news-href"]
                content += "\n"+str(row["texte"]).replace("*", "")+"\n\n\n"
                #print(content)
                f_out.write(content)
            f_out.close()
            if ACTEUR == "cire":
                shutil.copy(path_out, path_out.replace(ACTEUR, "fr"))


        ### one file per lang
        ### FR already exists because CIRÉ
        ### lazy implementation
        compteur = 0
        files = [file for file in os.listdir(WORK) if "cire" not in file]
        f_out = open(os.path.join(FINAL, "nl.txt"), "w")
        for file in files:
            ACTEUR = file.replace(".tsv", "")
            df = pd.read_csv(os.path.join(WORK, file), sep="\t")
            print(df.head())
            print(df.columns)
            
            for i, row in df.iterrows():
                compteur += 1
                content = "**** *article_"+str(compteur)
                content += " *date_"+row["date"]
                content += " *année_"+row["date"].split("-")[-1]
                content += " *catégorie_"+row["Category"]
                content += f" *acteur_{ACTEUR}"
                content += " *URL_"+row["link-href"]
                content += "\n"+str(row["texte"]).replace("*", "")+"\n\n\n"
                #print(content)
                f_out.write(content)
        f_out.close()

