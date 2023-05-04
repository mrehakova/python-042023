#petrpira

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

os.getcwd() 
os.chdir('C:\\Users\\magda\\Documents\\Czechitas\\PYTHON\\Python 2\\lekcie\\dom_ukol_1')


prezidenti=pd.read_csv('1976-2020-president.csv')
prezidenti.head()

prezidenti=prezidenti[["year","state","party_simplified","candidatevotes","totalvotes"]]

"""1. Urči pořadí jednotlivých kandidátů v jednotlivých státech a v jednotlivých letech (pomocí metody rank()).
Nezapomeň, že data je před použitím metody nutné seřadit a spolu s metodou rank() je nutné použít metodu groupby()."""

prezidenti.head()
prezidenti.dtypes
prezidenti=prezidenti.sort_values(["state"])
prezidenti["poradi_kandidatu"]=prezidenti.groupby(["state","year"])["candidatevotes"].rank(ascending=False)
prezidenti.head(30)
prezidenti=prezidenti.sort_values(["state","year","poradi_kandidatu"])
prezidenti.head(30) 


"""2.Pro další analýzu jsou důležití pouze vítězové. Vytvoř novou tabulku, která bude obsahovat pouze vítěze voleb"""
prezidenti.dtypes
prezidenti=prezidenti[prezidenti["poradi_kandidatu"]==1]
prezidenti.head()

"""3.Pomocí metody shift() přidej nový sloupec, abys v jednotlivých řádcích měl(a) po sobě vítězné strany ve dvou po sobě jdoucích letech."""
prezidenti["minuly_vitez_voleb"]=prezidenti.groupby(["state"])[["party_simplified"]].shift(+1)
prezidenti.head(30)
prezidenti.tail()

"""4.Porovnej, jestli se ve dvou po sobě jdoucích letech změnila vítězná strana. Můžeš k tomu použít např. funkci numpy.where() nebo metodu apply()."""
prezidenti_po76=prezidenti[prezidenti["year"]>1976].reset_index()
prezidenti_po76["zmena_strany_po76"]=np.where(prezidenti_po76["party_simplified"]!=prezidenti_po76["minuly_vitez_voleb"],"zmena","nedoslo k zmene")

prezidenti=prezidenti.reset_index() #kedze odkazujem na indexy, bez reset index to nefunguje
for i in range(len(prezidenti['party_simplified'])):
    if prezidenti.loc[i,'party_simplified']==prezidenti.loc[i,'minuly_vitez_voleb']:
        prezidenti.at[i,'zmena_strany']="nedoslo_k_zmene"
    elif prezidenti.loc[i,'party_simplified']!=prezidenti.loc[i,'minuly_vitez_voleb'] and pd.isna(prezidenti.loc[i,'minuly_vitez_voleb']):
        prezidenti.at[i,'zmena_strany']="nezname"
    else:
        prezidenti.at[i,'zmena_strany']="zmena"

prezidenti.head(30)

"""5.Proveď agregaci podle názvu státu a seřaď státy podle počtu změn vítězných stran."""

kde_sa_menili_strany=prezidenti[prezidenti["zmena_strany"]=="zmena"].groupby(["state"])["year"].count().sort_values(ascending=False)
kde_sa_menili_strany.head(20)
kde_sa_menili_strany.dtypes

"""6.Vytvoř sloupcový graf s 10 státy, kde došlo k nejčastější změně vítězné strany. Jako výšku sloupce nastav počet změn."""

fig = plt.figure(figsize = (15, 5))
plt.bar(kde_sa_menili_strany.index[0:10],(kde_sa_menili_strany.iloc[0:10]), color="#FF00FF")
plt.xlabel("Štáty")
plt.ylabel("Počet zmien víťaznej strany")
plt.title("10 štátov s najčastejšími zmenami víťaznej strany")
plt.show()

"""Pro další část pracuj s tabulkou se dvěma nejúspěšnějšími kandidáty pro každý rok a stát 
(tj. s tabulkou, která oproti té minulé neobsahuje jen vítěze, ale i druhého v pořadí)."""

prezidenti_2=pd.read_csv('1976-2020-president.csv')

prezidenti_2=prezidenti_2.sort_values(["state"])
prezidenti_2["poradi_kandidatu"]=prezidenti_2.groupby(["state","year"])["candidatevotes"].rank(ascending=False)
prezidenti_2=prezidenti_2.sort_values(["state","year","poradi_kandidatu"])
prezidenti_2.head(30)
prezidenti_2.dtypes
prezidenti_2_1=prezidenti_2[prezidenti_2["poradi_kandidatu"]==1]
prezidenti_2_2=prezidenti_2[prezidenti_2["poradi_kandidatu"]==2]
prezidenti_2_union= pd.concat([prezidenti_2_1,prezidenti_2_2])
prezidenti_2_union=prezidenti_2_union.sort_values(["year","state"])

prezidenti_2prvni=prezidenti_2_union[["year","state","party_simplified","candidatevotes","totalvotes","poradi_kandidatu"]]
prezidenti_2prvni.head(30)

prezidenti_2merged=pd.merge(prezidenti_2_1,prezidenti_2_2,on=["year","state"])
prezidenti_2merged.head(10)
prezidenti_2merged.columns()
prezidenti_2merged=prezidenti_2merged[["year","state","candidatevotes_x","totalvotes_x","party_simplified_x","poradi_kandidatu_x",
                                       "candidatevotes_y","totalvotes_y","party_simplified_y","poradi_kandidatu_y"]]
prezidenti_2merged.columns = ["year","state","candidatevotes_1","totalvotes_1","party_simplified_1","poradi_kandidatu_1",
                                       "candidatevotes_2","totalvotes_2","party_simplified_2","poradi_kandidatu_2"]
prezidenti_2merged.head(10)

""""1.Přidej do tabulky sloupec, který obsahuje absolutní rozdíl mezi vítězem a druhým v pořadí."""
prezidenti_2merged["rozdil_vitez_druhy"]=prezidenti_2merged["candidatevotes_1"]-prezidenti_2merged["candidatevotes_2"]
prezidenti_2merged.head()

"""2.Přidej sloupec s relativním marginem, tj. rozdílem vyděleným počtem hlasů."""
prezidenti_2merged["relativni_margin"]=prezidenti_2merged["rozdil_vitez_druhy"]/prezidenti_2merged["totalvotes_1"]
prezidenti_2merged.head()

"""3.Seřaď tabulku podle velikosti relativního marginu a zjisti, kdy a ve kterém státě byl výsledek voleb nejtěsnější."""
prezidenti_2merged.sort_values("relativni_margin", ascending=True).iloc[0,:].state  # na Floride
prezidenti_2merged.sort_values("relativni_margin", ascending=True).iloc[0,:].year   # v roku 2000

"""4.Vytvoř pivot tabulku, která zobrazí pro jednotlivé volební roky, kolik států přešlo od Republikánské strany k Demokratické straně,
kolik států přešlo od Demokratické strany k Republikánské straně a kolik států volilo kandidáta stejné strany."""

prezidenti.head()


def priprava_na_pivot(row): #funguje
    if "zmena" in row["zmena_strany"]:
        if "DEMOCRAT" in row["party_simplified"]:
            return "k demokratom"
        if "REPUBLICAN" in row["party_simplified"]:
            return "k republikanom"
    if "nedoslo_k_zmene" in row["zmena_strany"]:
        return "stejna_strana"
    if "nezname" in row["zmena_strany"]:
        return "neznamy predch.kandidat"

prezidenti["smer_zmeny"]=prezidenti.apply(priprava_na_pivot,axis=1)
prezidenti.head()

def priprava_na_pivot2(row):  #funguje
    if row["zmena_strany"]=="zmena":
        if row["party_simplified"]=="DEMOCRAT":
            return "k demokratom"
        if row["party_simplified"]=="REPUBLICAN":
            return "k republikanom"
    if row["zmena_strany"]=="nedoslo_k_zmene":
        return "stejna_strana"
    if row["zmena_strany"]=="nezname":
        return "neznamy predch.kandidat"

prezidenti["smer_zmeny2"]=prezidenti.apply(priprava_na_pivot2,axis=1)
prezidenti.head()


#pivot tabulka
prezidenti_po76_pre_pivot=prezidenti[prezidenti["year"]>1976] # v 76 bol vzdy neznamy predchadzajuci kandidat
pd.pivot_table(prezidenti_po76_pre_pivot, values="state", index="year", columns="smer_zmeny", aggfunc=len, fill_value=0, margins=False)

