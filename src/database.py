# pip install azure plotnine passgen pymysql adal wget tempfile
import mysql.connector
from mysql.connector import errorcode



class database(object):
    
    def create_table(company):

        DB_NAME = company

        cnx = mysql.connector.connect(host="localhost", user='root', password='virtuel1')
        cursor = cnx.cursor()
        cursor.execute("USE {}".format(company))
        #config = {"host":"liserveur.mysql.database.azure.com", "port":"3306", "user":"maestro@liserveur","password":"El_pass20", "database":company}
        #conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        #cursor = conn.cursor()
        print(company)

        TABLES = {} 
        
        TABLES["Fournisseur"]= ("CREATE TABLE `Fournisseur` ("
        "`id_fournisseur` INT NOT NULL AUTO_INCREMENT,"
        "`nom` TEXT,"
        "`activité` TEXT,"
        "`SIRET` TEXT,"
        "`SIREN` TEXT,"
        "`adresse` TEXT,"
        "`num_tel` TEXT(11),"
        "`email` TEXT,"
        "PRIMARY KEY (`id_fournisseur`)"
        ")")

        TABLES["Client"]= ("CREATE TABLE `Client` ("
        "`id_client` INT NOT NULL AUTO_INCREMENT,"
        "`nom` TEXT,"
        "`prenom` TEXT,"
        "`adresse` TEXT,"
        "`num_tel` TEXT(11),"
        "`email` TEXT,"
        "PRIMARY KEY (`id_client`)"
        ")")

        TABLES["Stock"]= ("CREATE TABLE `Stock` ("
        "`id_produit` INT NOT NULL AUTO_INCREMENT,"
        "`id_fournisseur` INT,"
        "`categorie` TEXT(50),"
        "`n_lot` INT,"
        "`nombre_colis` TEXT,"
        "`description_produit` TEXT(150),"
        "`produit` TEXT(50),"
        "`origine` TEXT(50),"
        "`quantité` FLOAT,"
        "`unité` TEXT,"
        "`prix_unitaire` FLOAT,"
        "`prix_total` FLOAT,"
        "`prix_vente_unitaire` FLOAT,"
        "`taxe` FLOAT,"
        "`bon_livraison` TEXT(150),"
        "`date_livraison` DATETIME,"
        "`date_peremption` DATETIME,"
        "`jours_avant_peremption` FLOAT,"
        "`type_conservation` TEXT,"
        "PRIMARY KEY (`id_produit`)"
        ")")



        TABLES["Panier"]=(" CREATE TABLE `Panier` ("
        "`id_panier` INT NOT NULL AUTO_INCREMENT,"
        "`id_client` INT,"
        "`nb_product` INT,"
        "`contenu` TEXT,"
        "`total_marge` FLOAT,"
        "`TTC_5_5` FLOAT,"
        "`HT_5_5` FLOAT,"
        "`TTC_20` FLOAT,"
        "`HT_20` FLOAT,"
        "`Total_TTC` FLOAT,"
        "`Total_HT` FLOAT,"
        "`date` DATETIME,"
        "`id_transaction_paiement` TEXT,"
        "PRIMARY KEY (`id_panier`)"
        ")")

        TABLES["Caisse"]= ("CREATE TABLE `Caisse` ("
        "`id_transaction` INT NOT NULL AUTO_INCREMENT,"
        "`id_panier` INT,"
        "`CB` FLOAT,"
        "`espèces` FLOAT,"
        "`chèque` FLOAT,"
        "`Total_encaissement` FLOAT,"
        "`Total_rendu` FLOAT,"
        "`date` DATETIME,"
        "PRIMARY KEY (`id_transaction`)"
        ")")

        TABLES["Activity"]= ("CREATE TABLE `Activity` ("
        "`id_activity` INT NOT NULL AUTO_INCREMENT,"
        "`user` TEXT,"
        "`ouverture` DATETIME,"
        "`fermeture` DATETIME,"
        "PRIMARY KEY (`id_activity`)"
        ")")




        TABLES["Vente"]=(" CREATE TABLE `Vente` ("
        "`id_vente` INT NOT NULL AUTO_INCREMENT,"
        "`id_produit` INT,"
        "`produit` TEXT,"
        "`quantité` FLOAT,"
        "`unité` TEXT,"
        "`total_marge` FLOAT,"
        "`TTC_5_5` FLOAT,"
        "`HT_5_5` FLOAT,"
        "`TTC_20` FLOAT,"
        "`HT_20` FLOAT,"
        "`Total_TTC` FLOAT,"
        "`Total_HT` FLOAT,"
        "`date` DATETIME,"
        "PRIMARY KEY (`id_vente`)"
        ")")


  
        
        for table_name in TABLES:
            table_description = TABLES[table_name]

            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

        return "OK"

      
    def get_db_connection(company):
            # Construct connection string
        try:
            conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
            print("Connection established")
            cursor = conn.cursor()

            #cursor.execute("SHOW DATABASES")
            database.create_table(company)
            

            for x in cursor:
                print(x)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                #config = {'host':'liserveur.mysql.database.azure.com','user':'maestro@liserveur','password':'El_pass20'}
                conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1')
                cursor = conn.cursor()
                cursor.execute("CREATE DATABASE " + company)
                database.create_table(company)
                print('Database Create')
            else:
                print(err)
        else:
            cursor = conn.cursor(dictionary=True)
        return cursor

    def formulaire_to_BDD(company,date,fournisseur,categ,n_lot,n_colis,marge,d_product,product,origine,quantity,unity,price,taxe):

        conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("INSERT INTO stock(id_fournisseur, categorie, n_lot, nombre_colis, description_produit, produit, origine, quantité, unité, prix_unitaire, prix_total, prix_vente_unitaire, date_livraison, taxe) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",(fournisseur, categ, n_lot, n_colis, d_product, product, origine, quantity, unity, price, quantity*(price), marge*(price), date, taxe))
        conn.commit()
        cursor.execute("SELECT * FROM stock;")
        data=cursor.fetchall()
        return data

    def consult_vente(company):
        conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Vente")
        vente= cursor.fetchall()
        return vente

    def consult_client(company):
        conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Client")
        client= cursor.fetchall()
        return client

    def add_client(company, id_client, nom_client, prenom_client,adresse, num_tel, email):
        conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("INSERT INTO Client(id_client, nom, prenom, adresse, num_tel, email) VALUES (%s,%s,%s,%s,%s,%s)", (id_client, nom_client, prenom_client,adresse, num_tel, email))
        return conn.commit()
        
    def product_search(company, result_pred):
        print('Function product_search')
        conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_produit, description_produit, produit, prix_vente_unitaire, unité FROM Stock WHERE produit LIKE ('%s')" %result_pred.upper())
        product= cursor.fetchall()
        return product
    
    def id_p_search(company, id_p):
        print('Function id_p_search')
        conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT categorie, id_produit, produit, prix_unitaire, prix_vente_unitaire, taxe, unité FROM Stock WHERE id_produit LIKE ('%s')" %id_p)
        product= cursor.fetchall()
        return product

    def add_panier(company, product,quantity, now): 
        print('Function add panier')
        conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        cursor = conn.cursor(dictionary=True)
        id_produit= product[0]["id_produit"]
        produit= product[0]["produit"]
        quantity= float(quantity) 
        montant_marge= (product[0]["prix_vente_unitaire"] - product[0]["prix_unitaire"])*quantity

        unity= product[0]["unité"]
        prix_vente_HT= float(quantity)*(product[0]["prix_vente_unitaire"])

        if float(product[0]["taxe"]) == 5.5:
            HT_5_5= round(prix_vente_HT)
            TTC_5_5= round(prix_vente_HT* (1+ float(product[0]["taxe"])/100))
            HT_20=0
            TTC_20=0
        else:
            HT_20= round(prix_vente_HT)
            TTC_20= round(prix_vente_HT* (1+ float(product[0]["taxe"])/100))
            HT_5_5=0
            TTC_5_5=0

        total_TTC= round(TTC_20 + TTC_5_5)
        total_HT= round(HT_5_5 + HT_20)
        cursor.execute("INSERT INTO Vente(id_produit, produit, quantité, unité, total_marge, HT_5_5, TTC_5_5, HT_20, TTC_20, Total_TTC, Total_HT, date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s, %s,%s, %s,%s);", (id_produit, produit,quantity,unity, montant_marge, HT_5_5, TTC_5_5, HT_20, TTC_20, total_TTC, total_HT, now,))

        ## Mise à jour Stock ##
        cursor.execute("UPDATE Stock SET quantité= quantité-(%s) WHERE id_produit=(%s)", (quantity, id_produit))
        cursor.execute("SELECT * FROM Vente;")
        data=cursor.fetchall()
        print("état table vente")
        

        print(data)
        conn.commit()

        return data

    def search(company, search_item):
        conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT categorie, id_produit, produit, prix_vente_unitaire, unité FROM Stock WHERE produit = %s OR id_produit = %s", (search_item, search_item))
        product_find= cursor.fetchall()
        return product_find
    
    def push_to_fournisseur(selected, email, tel, company):
        print("Fonction push_to_fournisseur")
        conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        cursor = conn.cursor(dictionary=True)
        nom= str(selected[0])
        activité=str(selected[3])
        SIRET=str(selected[1])
        SIREN=str(selected[2])
        adresse= str(selected[4:])

        cursor.execute("INSERT INTO fournisseur(nom, activité, SIRET, SIREN, adresse, num_tel, email ) VALUES (%s,%s,%s,%s,%s,%s,%s)", (nom, activité, SIRET, SIREN, adresse,tel, email))
        return conn.commit()

    def consult_table_fournisseur(company):
        print("Fonction consult_table_fournisseur")
        conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM fournisseur;")
        fournisseur= cursor.fetchall()
        return fournisseur
    
    def consult_table_stock(company):
        print("Fonction consult table stock")
        conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM stock;")
        stock= cursor.fetchall()
        return stock
    
    def delete_row_fournisseur(company, id_f):
        print("Fonction delete_row_fournisseur")
        conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        cursor = conn.cursor(dictionary=True)
        query= "DELETE FROM fournisseur WHERE id_fournisseur = (%s) "
        cursor.execute(query, (id_f,))
        conn.commit()
        cursor.execute("SELECT * FROM fournisseur;")
        fournisseur= cursor.fetchall()
        return fournisseur
    
    def delete_row_vente(company, id_vente):
        print("Fonction delete_row_vente")
        conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        cursor = conn.cursor(dictionary=True)
        query= "DELETE FROM Vente WHERE id_vente = (%s)"
        cursor.execute(query, (id_vente,))
        conn.commit()
        cursor.execute("SELECT * FROM Vente;")
        panier= cursor.fetchall()
        return panier
    
    def delete_row_stock(company, id_vente):
        print("Fonction delete_row_stock")
        conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        cursor = conn.cursor(dictionary=True)
        query= "DELETE FROM Stock WHERE id_produit = (%s)"
        cursor.execute(query, (id_vente,))
        conn.commit()
        cursor.execute("SELECT * FROM Stock;")
        stock= cursor.fetchall()
        return stock

    def valid_basket(company, now, client):
        print("Fonction valid_basket")
        conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        cursor = conn.cursor(dictionary=True)

    ###GET info from Vente ###
        
        ## Contenu Panier ##
        cursor.execute("SELECT * FROM Vente;")
        valid_panier1= cursor.fetchall()
        
        print(valid_panier1)
        print(len(valid_panier1))
        print("contenu panier")
        
        id_produit=[]
        produit=[]
        quantity=[]
        unity=[]
        product_adding=[]
  
        for elem in valid_panier1:
            print(elem)
            print()
            id_produit= elem['id_produit']
            
            produit= elem['produit']
            quantity= elem['quantité']
            unity= elem['unité']
        
        product_adding.append(list([id_produit,produit,quantity,unity]))
        product_adding=str(product_adding)
        ## Total marge Panier ##
        cursor.execute("SELECT SUM(total_marge) FROM Vente;")
        total_marge= cursor.fetchall()
        print(total_marge)
        montant=0
        for element in total_marge:
            montant_marge= element['SUM(total_marge)']
        montant_marge=round(montant_marge,2)
        ## Prix Total Panier Taxe 5.5##
        cursor.execute("SELECT SUM(HT_5_5) FROM Vente;")
        HT_5_5= cursor.fetchall()
        print(HT_5_5)
        prix_HT=0
        for elem in HT_5_5:
            prix_HT= elem['SUM(HT_5_5)']
        HT_5_5=round(prix_HT,2)
        print(HT_5_5)   

        cursor.execute("SELECT SUM(TTC_5_5) FROM Vente;")
        TTC_5_5= cursor.fetchall()
        prix_TTC=0
        for elem in TTC_5_5:
            prix_TTC= elem['SUM(TTC_5_5)']
        TTC_5_5 = round(prix_TTC,2)
        print(TTC_5_5)

        ## Prix Total Panier Taxe 20##

        cursor.execute("SELECT SUM(HT_20) FROM Vente;")
        HT_20= cursor.fetchall()
        print(HT_20)
        prix_HT=0
        for elem in HT_20:
            prix_HT= elem['SUM(HT_20)']
        HT_20=round(prix_HT,2)
        print(HT_20)   

        cursor.execute("SELECT SUM(TTC_20) FROM Vente;")
        TTC_20= cursor.fetchall()
        
        prix_TTC=0
        for elem in TTC_20:
            prix_TTC= elem['SUM(TTC_20)']
        TTC_20 = round(prix_TTC,2)
        print(TTC_20)

        total_HT= HT_20+HT_5_5
        total_TTC= TTC_20 + TTC_5_5

        ## Nombre de produits dans Panier ##
        nb_product=len(valid_panier1)

        print(now)
        print(total_HT)
    ### Create Panier from Info Vente ###
        cursor.execute("INSERT INTO Panier (id_client, nb_product, contenu, total_marge, HT_5_5, TTC_5_5, HT_20, TTC_20, Total_TTC, Total_HT, date) VALUES (%s,%s, %s, %s,%s,%s,%s,%s,%s, %s,%s)", (client,nb_product, product_adding, montant_marge, HT_5_5, TTC_5_5, HT_20, TTC_20, total_TTC, total_HT, now,))
        conn.commit()

        cursor.execute("SELECT * FROM Panier;")
        panier= cursor.fetchall()
        return panier


    def transaction_paiement(company, cb, espèces, chèque, now):
        print("Fonction transaction_paiement")
        conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        cursor = conn.cursor(dictionary=True)

        ## LAST ID_PANIER ##
        cursor.execute("SELECT id_panier FROM Panier ORDER BY id_panier DESC LIMIT 1;")
        panier= cursor.fetchall()
        id_panier= panier[0]['id_panier']
        cursor.execute("SELECT TTC_5_5, TTC_20 FROM Panier WHERE id_panier= (%s)", (id_panier,) )
        montant_a_payer= cursor.fetchall()
        montant_a_payer= float(montant_a_payer[0]['TTC_20']) + float(montant_a_payer[0]['TTC_5_5'])

        cb=float(cb)
        espèces= float(espèces)
        chèque= float(chèque)
        montant_reçu = cb+espèces+chèque

        montant_rendu= montant_reçu - montant_a_payer 

        print(montant_reçu)
        print(espèces)


        cursor.execute("INSERT INTO Caisse (id_panier, CB, espèces, chèque, Total_encaissement, Total_rendu, date) VALUES (%s, %s,%s,%s,%s, %s,%s)", (id_panier,  cb, espèces, chèque, montant_reçu,montant_rendu, now))
        conn.commit()

        cursor.execute("SELECT id_transaction FROM Caisse ORDER BY id_transaction DESC LIMIT 1;")
        n_transaction= cursor.fetchall()
        n_transaction= n_transaction[0]['id_transaction']
        
        cursor.execute('UPDATE Panier SET id_transaction_paiement=(%s) WHERE id_panier= (%s)', (n_transaction, id_panier))
        ### Delete row from table Vente -- PURGE ###
        cursor.execute("DELETE FROM Vente")
        conn.commit()
        return (montant_reçu, montant_rendu)
    
    def wait_paiement(company):
        conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id_panier FROM Panier ORDER BY id_panier DESC LIMIT 1;")
        panier= cursor.fetchall()
        id_panier= panier[0]['id_panier']
        message_transaction= "En attente de paiement"

        cursor.execute('UPDATE Panier SET id_transaction_paiement=(%s) WHERE id_panier= (%s)', (message_transaction, id_panier))
        conn.commit()
        ### Delete row from table Vente -- PURGE ###
        cursor.execute("DELETE FROM Vente")
        return conn.commit()
    
    def paiement_waiting(company):
        print("Fonction paiement_waiting")
        conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        cursor = conn.cursor(buffered=True)
        message_transaction= "En attente de paiement"

        cursor.execute("SELECT * FROM Panier WHERE id_transaction_paiement=(%s)", (message_transaction,))
        panier_waiting= cursor.fetchall()
        return panier_waiting

    def paid_wait(company, id_panier, remise, cb, esp, cheq, now):
        print("Fonction paid_wait")
        conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT Total_TTC FROM Panier WHERE id_panier= (%s)", (id_panier,) )
        montant_a_payer= cursor.fetchall()
        montant_a_payer= montant_a_payer[0]['Total_TTC']
        print(montant_a_payer)
        cb=float(cb)
        esp= float(esp)
        cheq= float(cheq)
        montant_reçu = cb+esp+cheq

        montant_rendu= montant_reçu - montant_a_payer 
        
        cursor.execute("INSERT INTO Caisse (id_panier, CB, espèces, chèque, Total_encaissement, Total_rendu, date) VALUES (%s, %s,%s,%s,%s, %s,%s)", (id_panier,  cb, esp, cheq, montant_reçu, montant_rendu, now))
        conn.commit()

        cursor.execute("SELECT id_transaction FROM Caisse ORDER BY id_transaction DESC LIMIT 1;")
        n_transaction= cursor.fetchall()
        n_transaction= n_transaction[0]['id_transaction']
        
        cursor.execute('UPDATE Panier SET transaction_paiement=(%s) WHERE id_panier= (%s)', (n_transaction, id_panier))
        conn.commit()
        return montant_reçu, montant_rendu









