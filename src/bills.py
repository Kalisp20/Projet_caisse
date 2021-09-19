import pandas as pd
from pandas.io import sql
import numpy as np
import re

import datetime
from datetime import timedelta
import mysql.connector
#import sqlite3
from mysql.connector import errorcode
import sqlalchemy
from sqlalchemy.types import Integer


class bills(object):

    def clean_data(pdf, date, id_fournisseur,taxe, marge, categ):
        liste_extract=[]
        for i in range(len(pdf.pages)):
            extract= pdf.pages[i].extract_tables(table_settings={"vertical_strategy": "text"})
            liste_extract.append(extract)
        
        test= liste_extract
        ## Nombre de produits par doc
        total_lines_table= 0
        for page in range(len(test)):
            for table in range(len(test[page])):
                ##Somme nombre total de lignes par table 
                total_lines_table+= len(test[page][table])

        total_rows= total_lines_table
        data= pd.DataFrame(columns=['n_lot','description_produit','produit','origine','quantité','unité','prix_unitaire','prix_total','nombre_colis','bon_livraison'], index=range(total_rows))
        
        ## Commandes REGEX
        detect_ref_commande= re.compile('^[B]\.[L]')
        detect_lot= re.compile('\d{6}')
        detect_colis= re.compile('\d{1}[\s][C,P]')
        detect_quantity= re.compile('^(\d*\.)?\d+[\s][K,P]')
        detect_anomalie= re.compile('[K,P][\s]')
        detect_number= re.compile('\d*\.?\d+')
        detect_decimal= re.compile('^\d{3}')
        date= re.compile('\d{2}[\s, /]{1}\d{2}[\s, /]{1}\d{1,2}')

        ## Liste pays Origine produit
        list_pays_origine= ['FRANCE', 'PEROU', 'NOUVELLE ZELANDE', 'CAMEROUN', 'GHANA','ESPAGNE','BRESIL', 'PAYS-BAS','AFRIQUE DU SUD', 'CHILI', 'ISRAEL', 'PEROU','CHINE','ITALIE','COTE D IVOIRE','SENEGAL'] 

        total_page= len(test[0:][0:])
        index=0
        index_to_drop=[]
        for page in range(0,total_page):


            for lines in range(len(test[page][0])):

            
                data['description_produit'][index]= test[page][0][lines][1:4]
                data['quantité'][index]= test[page][0][lines][-5]
                data['prix_unitaire'][index]= test[page][0][lines][-4]
                data['prix_total'][index]= test[page][0][lines][-3]

                for element in range(len(test[page][0][lines])):

                    ref_lot= detect_lot.match(test[page][0][lines][element])
                    if ref_lot:
                        data['n_lot'][index]=ref_lot.group()
                    
                    
                    ref_commande= detect_ref_commande.match(test[page][0][lines][element])
                    if ref_commande:
                        next_rows= index + 1
                        data['bon_livraison'][next_rows]= data['description_produit'][index]
                        for rows in range(next_rows, len(data)) :
                            data['bon_livraison'][rows]= data['bon_livraison'][next_rows]
                        index_to_drop.append(index)
                    
                
        
                    num_colis= detect_colis.match(test[page][0][lines][element])
                    if num_colis:
                        data['nombre_colis'][index]= num_colis.group()

                            
                    if test[page][0][lines][element] in list_pays_origine:
                        data['origine'][index]= test[page][0][lines][element]
                            
                    decimale= detect_decimal.match(data['prix_total'][index])
                    if decimale:
                        #print(test[page][0][lines][element])
                        data['prix_total'][index]= test[page][0][lines][-2]+decimale.group()
                    
                index+=1

        ## Liste fruits et legumes
        fruits_leg=['Abricot','Abricot-sec','Ail','Ananas','Artichaut','Asperge','Aubergine','Avocat','Banane','Bette','Betterave-rouge','Carambole','Carotte','Cassis','Céleri-branche','Céleri-rave','Cerise','Chou','Chou-fleur','Citron-jaune','Clémentine','Coing','Concombre','Courgette','Échalote','Endive','Fenouil','Figue','Fraise','Framboise','Gimgembre','Haricot-vert','Igname','Kaki','Kiwi','Kumquate','Laitue','Litchi','Mangue','Manioc','Melon','Mûre','Myrtille','Navet','Nectarine','Noix-de-coco','Oignon','Orange','Papaye','Pastèque','Patate-douce','Pêche','Poire','Poireau','Poivron','Pomelos','Pomme','Pomme-de-terre','Potiron','Prune','Radis','Raisin','Rhubarbe','Taro','Tomate']
        ##Éléments liste en majuscule
        fruits_leg= [x.upper() for x in fruits_leg]
        ##Conversion liste to Dataframe 
        fruits_leg= pd.DataFrame(fruits_leg)
        fruits_leg.columns=['nom']
        ## Utilisation list fruits et légumes pour déterminer produit produit.
        for element in range(len(data)):
            try:
                nom_prod= data['description_produit'][element][0].split()
                if fruits_leg['nom'].str.contains(nom_prod[0]).any():
                    data['produit'][element]= nom_prod[0]
            except:
                print(element)

        rows = data.index[index_to_drop]
        data.drop(rows, inplace=True)
        data.reset_index(drop=True, inplace=True)  

        for i in range(len(data)):
            anomalie= detect_anomalie.match(data['prix_unitaire'][i])
            if anomalie:
                print(anomalie)
                list_e= data['prix_unitaire'][i].split()
                data['quantité'][i]= data['quantité'][i]+list_e[0]
                data['prix_unitaire'][i]= list_e[1]
        


        for element in range(len(data)):
            try:
                data['n_lot'][element]= pd.to_numeric(data['n_lot'][element])
                data['prix_unitaire'][element]= pd.to_numeric(data['prix_unitaire'][element], downcast="float", inplace=True)
                
                data['prix_total'][element]= pd.to_numeric(data['prix_total'][element], downcast="float", inplace=True)
                
            except:
                price=data['prix_total'][element].split()
                if len(price)>=1:
                    data['prix_total'][element]= price[0]
        
        detect_unity= re.compile('[K,P]')
        for element in range(len(data)):
            unit= detect_unity.search(data['quantité'][element])
            if unit:
                data['unité'][element]= unit.group()
                data['quantité'][element]= data['quantité'][element].replace(unit.group(),'')
                data['quantité'][element]= data['quantité'][element].split()
                if len(data['quantité'][element])>=1:
                    data['quantité'][element]= data['quantité'][element][0]
                try:
                    data['quantité'][element]= pd.to_numeric(data['quantité'][element], downcast='float') 
                except:
                    print(data['quantité'][element][0:]) 
        
        data['prix_unitaire'].fillna(value=0, inplace=True)
        data['prix_total'].fillna(value=0, inplace=True)           
        data.dropna(inplace=True)
        data.reset_index(drop=True, inplace=True)


        data[['n_lot','description_produit','produit','origine','quantité','unité','prix_unitaire','prix_total','nombre_colis','bon_livraison']]= data[['n_lot','description_produit','produit','origine','quantité','unité','prix_unitaire','prix_total','nombre_colis','bon_livraison']].astype(str)
        
        data['quantité']= pd.to_numeric(data['quantité'], downcast='float', errors='coerce') 
        data['prix_unitaire']= pd.to_numeric(data['prix_unitaire'], downcast='float', errors='coerce') 
        
        data['prix_vente_unitaire']= ''
        data['date_livraison']= ''
        data['id_fournisseur']= ''
        data['prix_vente_unitaire']= data['prix_unitaire']*marge
        data['taxe']=taxe
        data['date_livraison']= date
        data['id_fournisseur']= id_fournisseur
        data['categorie']=categ
        data.to_csv('data.csv') 

        for element in range(len(data)):
            if data['quantité'][element]==0:
               data['quantité'][element]= float(data['prix_total'][element]) / float(data['prix_unitaire'][element])
        return data         
        
            
    def info_complete():

        data_conservation= pd.read_csv('/Users/hanane/Documents/projet_chef_doeuvre/App_caisse-main/src/data_conservation.csv')

        bills= pd.read_csv('data.csv')
        bills['jours_avant_peremption']=''
        bills['date_peremption']=''


        for row in range(len(bills)):
            for element in range(len(data_conservation)):
                
                try:
                    data_conservation['produit'][element]= data_conservation['produit'][element].upper()
                    data_conservation['produit'][element]= data_conservation['produit'][element].split()
                    nom_produit= data_conservation['produit'][element][0].upper()
                    
                    row= bills[bills['produit'].str.contains(nom_produit)==True].index.tolist()
                    if len(row) >0:
                
                        temps= data_conservation['mean_conservation'][element]
                        bills['jours_avant_peremption'][row]= data_conservation['mean_conservation'][element]
                        
                        bills['date_livraison'][row]= pd.to_datetime(bills['date_livraison'][row])
                        #bills['date_livraison'][row]= bills['date_livraison'][row].astype(datetime)
                        print(type(bills['date_livraison'][row]))

                        bills['date_peremption'][row]= bills['date_livraison'][row] + timedelta(days=temps)
                        bills['date_peremption'][row]= pd.to_datetime(bills['date_peremption'][row])
                        print(type(bills['date_peremption'][row]))
                        #bills['date_péremption'][row]= bills['date_péremption'][row].astype(datetime)
                except:
                    print()
        return bills
 



    def bills_to_bdd(doc_clean, company):

        doc_clean['date_peremption']= pd.to_datetime(doc_clean['date_peremption'])
        doc_clean['date_livraison']= pd.to_datetime(doc_clean['date_livraison'])
        doc_clean['jours_avant_peremption']= pd.to_numeric(doc_clean['jours_avant_peremption'], downcast='float', errors='coerce')

        engine = sqlalchemy.create_engine("mysql+pymysql://" + 'root' + ":" + 'virtuel1' + "@" + '127.0.0.1' + "/" + company)
        doc_clean.to_sql('Stock', con= engine, if_exists='append', index=False, method='multi')
        
        with engine.connect() as connection:
            result= connection.execute('SELECT * FROM Stock ORDER BY id_produit DESC ').fetchall()

        return result
    
