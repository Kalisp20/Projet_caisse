from flask import *
from bootstrap_datepicker_plus import DatePickerInput
from django import forms


import pdfplumber
import pyrebase
import requests

from src.database import *
from src.camera import *
from src.bills import *
from src.prediction import *

import mysql.connector
from mysql.connector import errorcode
import os
import sqlalchemy
from sqlalchemy.types import Integer
import numpy as np
from firebase.firebase import FirebaseAuthentication
import datetime
from datetime import datetime
#from flask.ext.cache import Cache
#from yourapp import app, your_cache_config

app = Flask(__name__)

#cache = Cache()

app.config['SECRET_KEY'] = os.environ.get('DJANGO_SECRET_KEY')
#Bootstrap(app)


## Authentification with Firebase email_password ##
firebaseConfig={
    "apiKey": "AIzaSyDdvxGy9We2PQHXqqYeBYwMlG1DH331v38",
    "authDomain": "connexion-79f65.firebaseapp.com",
    "projectId": "connexion-79f65",
    "databaseURL":"https://connexion-79f65-default-rtdb.europe-west1.firebasedatabase.app/",
    "storageBucket": "connexion-79f65.appspot.com",
    "messagingSenderId": "843638557638",
    "appId": "1:843638557638:web:3a0cdccedbc3008f3100c7",
    "measurementId": "G-9PCHQ7C4MH"
    }
firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()


camera=VideoCamera()
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

##JSON serializer for objects not serializable by default json code##
def json_serial(obj):
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

## Authentification ##
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
            company= request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            print(email)
            print(password)
            try:
                user= auth.sign_in_with_email_and_password(email, password)
                #user_id = auth.get_account_info(user['idToken'])
                #session['usr'] = user_id
                now=datetime.now()
                now= now.strftime("%Y/%m/%d %H:%M:%S")
                print(now)
                try:
                    conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1', database=company)
                    cur = conn.cursor(dictionary=True)
                    print(email)
                    print(type(email))
                    cur.execute("INSERT INTO activity(user,ouverture) VALUES(%s,%s);",(email,now))
                    print("Connexion OK")
                    conn.commit()
                    
                except:
                    print("Connexion KO")
                return redirect(url_for('.index', company=company))
            except:
                unsuccessful = 'Please check your credentials'
                return render_template('login.html', umessage=unsuccessful)
    return render_template('login.html')

@app.route('/logout/<company>', methods=['GET', 'POST'])
def logout(company):
    auth.current_user=None
    now=datetime.now()
    now= now.strftime("%Y/%m/%d %H:%M:%S")
    conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1', database=company)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id_activity FROM activity ORDER BY id_activity DESC LIMIT 1;")
    id_activity= cur.fetchone()
    id_activity=id_activity['id_activity']
    print(type(id_activity))
    cur.execute("UPDATE Activity SET fermeture=(%s) WHERE id_activity=(%s);", (now, id_activity))
    conn.commit()
    return render_template('login.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if (request.method == 'POST'):
            company= request.form['name']
            email = request.form['email']
            password = request.form['password']

            ## Save User info to Realtime Database Firebase ##
            db_user= {'User Name': company, 'Email': email}
            result= db_fire.post('/connexion-79f65-default-rtdb/user_db', db_user)

            ## Create User with email and password - Firebase ##
            user= auth.create_user_with_email_and_password(email, password)
            auth.send_email_verification(user['idToken'])
            return render_template('login.html')
    return render_template('register.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if (request.method == 'POST'):
            email = request.form.get('email')
            auth.send_password_reset_email(email)
            return render_template('login.html')
    return render_template('forgot-password.html')

## HOME ##
@app.route('/index/<company>', methods=['GET', 'POST'])
def index(company):
    print(company)
    database.get_db_connection(company)
    return render_template('index.html', company=company)

## STOCK ##
@app.route('/stock/<company>', methods=['GET', 'POST'])
def stock(company):
    conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1', database=company)
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT nom FROM Fournisseur;")
    fourni= cur.fetchall()
    name_fourni=list()
    for element in fourni:
        name_fourni.append(element['nom'])
    if len(name_fourni) == 0:
        no_fournisseur = "Veuillez renseigner votre fournisseur"


        return render_template('stock2.html',  no_fournisseur=no_fournisseur, company=company)


    if request.method == 'POST':

        if 'add_supplier'in request.form:
            print("tentative redirect")
            return redirect(url_for('test'))

        if 'Manuel' in request.form:
            categ=request.form.get('categ')
            fournisseur=request.form.get('id_f')
            print(fournisseur)
            #cur.execute("SELECT id_fournisseur FROM Fournisseur WHERE nom=%s;", (fournisseur,))
            id_fourni= cur.execute("SELECT id_fournisseur FROM Fournisseur WHERE nom=%s;", (fournisseur,))
            print(id_fourni)
            marge= 1+ float(request.form.get('marge_manuel'))/100
            taxe= float(request.form.get('taxe'))

            date=request.form.get('datetimepicker2')
            print(date)
            n_lot=request.form.get('lot')
            n_colis=request.form.get('colis')
            d_product = request.form.get('d_produit')
            product = request.form.get('prod')
            origine= request.form.get('ori')
            quantity = int(request.form.get('quantity'))
            unity= request.form.get('unity')
            price = int(request.form.get('price'))
            show_table_stocks= database.formulaire_to_BDD(company,date,id_fourni,categ,n_lot,n_colis,marge,d_product,product,origine,quantity,unity,price,taxe)
            return render_template('stock2.html', id_fournisseur=id_fourni,  name_fournisseur=name_fourni, company=company, data=show_table_stocks)

        if 'remove' in request.form:
            print("Remove row from stock ")
            id_stock=request.form.get('row_remove')
            
            print(id_stock)
            show_table_stocks= database.delete_row_stock(company, id_stock)
            return render_template('stock2.html', company=company, data=show_table_stocks)


        elif 'PDF' in request.form:
            categ=request.form.get('categ')
            
            fournisseur=request.form.get('id_f')
            cur.execute("SELECT id_fournisseur FROM Fournisseur WHERE nom LIKE %s;", (fournisseur,))
            id_fourni= cur.fetchall()
            for element in id_fourni:
                info_fournisseur=element['id_fournisseur']
            
            marge= 1+ float(request.form.get('marge'))/100
            taxe= float(request.form.get('taxe'))
            date=request.form.get('datetimepicker1')

            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                uploaded_file.save(uploaded_file.filename)
                doc= uploaded_file.filename
                pdf= pdfplumber.open(doc)
                nombre_page= "Nombres de pages = {}".format(len(pdf.pages))
                view_page= pdf.pages[5].to_image(resolution=150)
                view_page.save("static/img/image_pdf.jpg")
                
                doc_clean= bills.clean_data(pdf, date, info_fournisseur, taxe, marge, categ)
                doc_clean['date_livraison']=date
                doc_clean.to_csv('data.csv', index=False)
                doc_clean= bills.info_complete()
                doc_clean.to_csv('data.csv', index=False)
                doc_clean= bills.bills_to_bdd(doc_clean, company)

                return render_template('stock2.html', name_fournisseur=name_fourni, company=company, data=doc_clean, view_page=view_page, nombre_page=nombre_page)
            return render_template('stock2.html',  name_fournisseur=name_fourni, company=company)

    return render_template('stock2.html',  name_fournisseur=name_fourni, company=company)


@app.route('/updatestock/<company>', methods=['GET','POST'])
def updatestock(company):

    id_produit=request.form['pk']
    name = request.form['name']
    value = request.form['value']

    #config = {'host':'liserveur.mysql.database.azure.com','user':'maestro@liserveur','password':'El_pass20','database':'Spicerie'}
    conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1', database=company)
    cur = conn.cursor(dictionary=True)

    if name == 'id_fournisseur':
        cur.execute("UPDATE stock SET id_fournisseur = %s WHERE id_produit = %s ", (value, id_produit))
    elif name == 'prix_vente':
        cur.execute("UPDATE stock SET prix_vente_unitaire = %s WHERE id_produit = %s ", (value, id_produit))
    elif name == 'jours_conservation':
        cur.execute("UPDATE stock SET jours_avant_peremption = %s WHERE id_produit = %s", (value, id_produit))
        cur.execute("UPDATE stock SET date_peremption = DATE_ADD(date_livraison, INTERVAL %s DAY) WHERE id_produit = %s", (int(value), id_produit))
    elif name == 'lot':
        cur.execute("UPDATE stock SET n_lot = %s WHERE id_produit = %s ", (value, id_produit))
    elif name == 'categorie':
        cur.execute("UPDATE stock SET categorie = %s WHERE id_produit = %s ", (value, id_produit))    
    elif name == 'd_produit':
        cur.execute("UPDATE stock SET description_produit = %s WHERE id_produit = %s ", (value, id_produit))
    elif name == 'produit':
        cur.execute("UPDATE stock SET produit = %s WHERE id_produit = %s ", (value, id_produit))
    elif name == 'origine':
        cur.execute("UPDATE stock SET origine = %s WHERE id_produit = %s ", (value, id_produit))   
    elif name == 'quantité':
        cur.execute("UPDATE stock SET quantité = %s WHERE id_produit = %s ", (value, id_produit))
    elif name == 'unité':
        cur.execute("UPDATE stock SET unité = %s WHERE id_produit = %s ", (value, id_produit))
    elif name == 'prix_unitaire':
        cur.execute("UPDATE stock SET prix_unitaire = %s WHERE id_produit = %s ", (value, id_produit))
    elif name == 'taxe':
        cur.execute("UPDATE stock SET prix_unitaire = %s WHERE id_produit = %s ", (value, id_produit))


    conn.commit()
    cur.execute("SELECT * FROM stock")
    data= cur.fetchall()
    print(type(data))
    cur.close()

    return json.dumps({'status':'OK'})

@app.route('/consult_stock/<company>', methods=['GET','POST'])
def consult_stock(company):
    print('consult table stock')
    table_stock= database.consult_table_stock(company)
    
    if 'remove_product' in request.form:
        id_stock=request.form.get('row_remove')
        id_stock=id_stock[0]
        show_table_stocks= database.delete_row_stock(company, id_stock)
        return render_template('stock2.html', company=company, data=show_table_stocks)
    return render_template('stock2.html', company=company, data=table_stock)


## FOURNISSEUR ##
@app.route('/test/<company>', methods=['GET','POST'])
def test(company):

    ## Recherche fournisseur via api sirene
    if 'search_fournisseurs' in request.form :
        search= request.form.get('search_fournisseurs')
        API_SIRET= 'https://entreprise.data.gouv.fr/api/sirene/v1/full_text/'
        result= requests.get(API_SIRET+search)

        if result.status_code == 404:
            no_result= "Aucun résultat veuillez modifier votre recherche !"
            print(no_result)
            return render_template('fournisseurs.html', no_result=no_result, company=company)

        result= json.loads(result.content.decode('utf-8'))
        return render_template('fournisseurs.html', result=result, company=company)

    ## Données fournisseur selectionné enregistré sur table fournisseur
    elif 'send_to_fournisseur'in request.form:
        selected= (request.form.get('select_fournisseurs'))
        selected= list(selected.split(","))
        email= request.form.get('email')
        tel= request.form.get('tel')
        data_four= database.push_to_fournisseur(selected, email, tel, company)
        return render_template('fournisseurs.html', company=company)
    return render_template('fournisseurs.html', company=company)

### Suppression Fournisseur ###
@app.route('/test2/<company>', methods=['GET','POST'])
def test2(company):

    ## View table fournisseur
    data_table= database.consult_table_fournisseur(company)
    
    ## Option remove fournisseur 
    if "select_remove" in request.form:
        select_row= request.form.get("row_remove")
        select_row= list(select_row.split(","))
        print(select_row[0])
        id_f= int(select_row[0])
        new_table= database.delete_row_fournisseur(company, id_f)
        return render_template('fournisseurs.html', company=company, data=new_table)
    return render_template('fournisseurs.html', company=company, data=data_table)

### MAJ Fournisseur ###
@app.route('/updatefournisseur/<company>', methods=['GET','POST'])
def updatefournisseur(company):

    id_fournisseur=request.form['pk']
    name = request.form['name']
    value = request.form['value']

    conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1', database=company)
    cur = conn.cursor(dictionary=True)

    if name == 'email':
        cur.execute("UPDATE fournisseur SET email = %s WHERE id_produit = %s ", (value, id_fournisseur))
    elif name == 'num_tel':
        cur.execute("UPDATE fournisseur SET num_tel = %s WHERE id_produit = %s ", (value, id_fournisseur))


    cur.close()

    return json.dumps({'status':'OK'})


## CAISSE ##
@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/caisse/<company>', methods=['GET', 'POST'])
def caisse(company):
                # datetime object containing current date and time
    now = datetime.now()
    now= now.strftime("%Y/%m/%d %H:%M:%S")
  
    
    if request.method == 'POST':
        
        if 'go_pred2' in request.form:
            camera.capture()
            product = 'static/img/capture.jpg'
            result_pred= vision_pred.prediction(product)
            print(result_pred.upper())
            data= database.product_search(company,result_pred)
            if len(data)==0:
                no_found="Le produit n'est pas renseigné dans la table Stock"
                return render_template('caisse3.html', photo=video_feed, client=database.consult_client(company), no_found=no_found, result_pred= result_pred, company=company)
            else:
                return render_template('caisse3.html', photo=video_feed, client=database.consult_client(company), data=data, company=company)

        if 'search_product' in request.form:
            search_item= request.form.get('produit')
            product_find= database.search(company, search_item)
            if len(product_find)==0:
                no_found="Le produit n'est pas renseigné dans la table Stock"
                return render_template('caisse3.html', photo=video_feed, client=database.consult_client(company), no_found=no_found, result_pred= search_item, company=company)
            else:
                return render_template('caisse3.html', company=company, client=database.consult_client(company), data=product_find)

        if 'submit_product' in request.form:
            id_p= request.form.get('id_produit')
            id_p= int(id_p)
            quantity=request.form.get('quantity_product')
        
            product= database.id_p_search(company, id_p)
            infos_ticket= database.add_panier(company, product, quantity, now)
            result_TTC = 0
            result_HT=0
            for elem in infos_ticket:
                print(elem)
                result_TTC+= elem['TTC_5_5'] + elem['TTC_20'] 
                result_HT+= elem['HT_5_5'] + elem['HT_20'] 

            result_TTC= round(result_TTC,2)
            result_HT = round(result_HT,2)

            return render_template('caisse3.html',company=company, client=database.consult_client(company), ticket_attente=database.paiement_waiting(company) ,ticket=infos_ticket, prix_total_TTC=result_TTC, prix_total_HT=result_HT)

        if 'remove_product' in request.form:
            id_vente=request.form.get('row_remove')
            id_vente=id_vente[0]
            infos_ticket= database.delete_row_vente(company, id_vente)
            result_TTC = 0
            result_HT=0
            for elem in infos_ticket:
                print(elem)
                result_TTC+= elem['TTC_5_5'] + elem['TTC_20'] 
                result_HT+= elem['HT_5_5'] + elem['HT_20'] 

            result_TTC= round(result_TTC,2)
            result_HT = round(result_HT,2)
            return render_template('caisse3.html',company=company, client=database.consult_client(company), ticket_attente=database.paiement_waiting(company), ticket=infos_ticket, prix_total_TTC=result_TTC, prix_total_HT=result_HT)

        if 'paiement' in request.form:
            client=request.form.get('select_client')
            print(client)
            print(type(client))
            cb= request.form.get('CB')
            esp= request.form.get('espèces')
            cheque= request.form.get('chèque')
 
            if cb =='':
                print("remise vide")
                cb=0
            if esp =='':
                print("remise vide")
                esp=0
            if cheque =='':
                print("remise vide")
                cheque=0


            valid_panier= database.valid_basket(company, now, client)
            montant_transaction= database.transaction_paiement(company, cb, esp, cheque, now)
            montant_transaction= list(montant_transaction)
            print(montant_transaction)
            return render_template('caisse3.html',company=company, client=database.consult_client(company), ticket_attente=database.paiement_waiting(company) ,montant_transaction=montant_transaction)

        if 'wait' in request.form:
            print('wait')
            client=request.form.get('id_client')
            database.valid_basket(company, now, client)
            database.wait_paiement(company)
            return render_template('caisse3.html',company=company, client=database.consult_client(company), ticket_attente=database.paiement_waiting(company) )


        if 'paiement_wait' in request.form: 
            id_panier=request.form.get('id_panier')
            cheq=request.form.get('cheq_wait_paid')
            esp=request.form.get('esp_wait_paid')
            cb=request.form.get('cb_wait_paid')
            remise=request.form.get('remise_wait_paid')

            if cb =='':
                print("remise vide")
                cb=0
            if esp =='':
                print("remise vide")
                esp=0
            if cheq =='':
                print("remise vide")
                cheq=0
            paid_wait= database.paid_wait(company, id_panier, remise, cb, esp, cheq, now)
     
            return render_template('caisse3.html', photo=video_feed, client=database.consult_client(company), company=company, montant_transaction=paid_wait, ticket_attente=database.paiement_waiting(company))

        if 'add_client' in request.form:
            id_client=request.form.get('id_client')
            nom_client= request.form.get('nom_client')
            prenom_client=request.form.get('prenom_client')
            adresse=request.form.get('adresse')
            num_tel=request.form.get('num_tel')
            email=request.form.get('email')
            database.add_client(company, id_client, nom_client, prenom_client,adresse, num_tel, email)
            
            infos_ticket= database.consult_vente(company)
            result_TTC = 0
            result_HT=0
            for elem in infos_ticket:
                print(elem)
                result_TTC+= elem['TTC_5_5'] + elem['TTC_20'] 
                result_HT+= elem['HT_5_5'] + elem['HT_20'] 

            result_TTC= round(result_TTC,2)
            result_HT = round(result_HT,2)
            return render_template('caisse3.html',company=company, client=database.consult_client(company),ticket_attente=database.paiement_waiting(company) ,ticket=infos_ticket, prix_total_TTC=result_TTC, prix_total_HT=result_HT)

    return render_template('caisse3.html', photo=video_feed, client=database.consult_client(company), company=company, ticket_attente=database.paiement_waiting(company) )


def main():
    cache.init_app(app, config=your_cache_config)

    with app.app_context():
        cache.clear()

@app.route('/dashboard/<company>')
def dashboard(company): 

    conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1',database=company)
    cursor = conn.cursor(buffered=True)

    labels = list()
    values = list()


    cursor.execute("SELECT id_produit FROM Stock ORDER BY id_produit DESC LIMIT 1;")
    nb_in_stock= cursor.fetchone()
    print(nb_in_stock)

    cursor.execute("SELECT id_panier FROM Panier ORDER BY id_panier DESC LIMIT 1;")
    nb_in_panier= cursor.fetchone()

    cursor.execute("SELECT id_transaction FROM Caisse ORDER BY id_transaction DESC LIMIT 1;")
    nb_in_caisse= cursor.fetchone()

    if nb_in_stock is None:
        return render_template('no_charts.html')
    if nb_in_panier is None:
        return render_template('no_charts.html')
    if nb_in_caisse is None:
        return render_template('no_charts.html')

    else:
        cursor.execute("SELECT Total_encaissement from Caisse")
        rows = cursor.fetchall()
            # Convert query to objects of key-value pairs
        for row in rows:
            total_encaissement, =row
            print(total_encaissement)
            
        date_now= datetime.today().date()
        
        cursor.execute("SELECT Total_encaissement from Caisse WHERE DATE(date)=(%s)", (date_now,))
        ca_jour= cursor.fetchall()
        ca=0
        for item in ca_jour:
            total_jour, = item
            ca+=float(total_jour)
        ca_jour= ca

        cursor.execute("SELECT HOUR(date), SUM(total_encaissement) FROM Caisse WHERE DATE(date)=(%s) GROUP BY HOUR(date) ;", (date_now,))
        vente_heure= cursor.fetchall()
        heure=list()
        encaissement=list()
        print(vente_heure)
        for element in vente_heure:
            hour, total_hour= element
            print(hour)
            print(type(hour))
            heure.append(str(hour))
            encaissement.append(total_hour)

        cursor.execute("SELECT SUM(total_marge) from Panier")
        benef = cursor.fetchall()
        for row in benef:
            montant_marge, = row
        if montant_marge !=None:
            montant_marge= round(montant_marge,2)

        cursor.execute("SELECT SUM(prix_total) from Stock;")
        montant_depense = cursor.fetchall()
        for item in montant_depense:
            montant_depense, = item
        if montant_depense !=None:
            montant_depense= round(montant_depense,2)
        
            rapport_benef_depense= (montant_marge / montant_depense )
        #print(rapport_benef_depense)
            rapport_depense= 100-rapport_benef_depense
        #print(rapport_depense)

        product=list()
        quantity=list()
        
        cursor.execute("SELECT produit, SUM(quantité) FROM Stock GROUP BY produit ;")
        check_stock=cursor.fetchall()
        print(check_stock)
        for element in check_stock:
            produit,quantity_product=element
            print(element)
            product.append(produit)
            quantity.append(quantity_product)
        print(len(product))
        print(len(quantity))

        cursor.execute("SELECT produit, SUM(quantité) FROM Stock WHERE jours_avant_peremption<=1.5 GROUP BY produit ;")
        perissable= cursor.fetchall()
        PP=list()
        QP=list()
        for element in perissable:
            produit, quant = element
            PP.append(produit)
            QP.append(quant)
        print(PP, QP)
        return render_template('charts.html', company=company,total_encaissement=total_encaissement,  montant_marge=montant_marge, montant_depense= montant_depense, rapport_depense=rapport_depense, rapport_benef_depense=rapport_benef_depense, product=product, quantity=quantity, heure=heure, total_hour= encaissement, ca_jour=ca_jour, produit_perissable=PP, quantity_perissable=QP)


   

if __name__ == '__main__':
    main()
    app.run(debug=True)
    init_db(app)
