from flask import Flask, render_template, session
import pymysql
from flask import request
from flask import redirect
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
# create a secret key used in encrypting the sessions
app.secret_key = "Wdg@#$%89jMfh2879mT"
connection = pymysql.connect(host='localhost', user='root', password='', database='shopit')


@app.route("/")
def home():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Items")
    rows = cursor.fetchall()
    return render_template('index.html', rows=rows)


@app.route("/search", methods=['POST','GET'])
def search():
    if request.method == "POST":
        searchterm = request.form['search']
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM Items WHERE ProductName LIKE '{}%'".format(searchterm[0]))
            rows = cursor.fetchall()
            return render_template('index.html', rows=rows)
        except:
            return render_template('index.html')
    return render_template('index.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM  shopit_users WHERE email=%s AND password =%s", (email, password))
        if cursor.rowcount == 1:
            session['key'] = email
            return redirect('/')
        else:
            return render_template('login.html', msg="Failed to login, Please check your username and Password")
    return render_template('login.html')


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO shopit_users(email,password,phone) VALUES(%s,%s,%s)", (email, password, phone))
            connection.commit()
        except:
            return render_template('register.html', msg1="Unable to create another account with {}".format(email))
        return render_template('register.html', msg1="Account Created Successfully")
    else:
        return render_template('register.html')


@app.route("/products")
def products():
    return "This will be products page"


@app.route('/single/<product_id>')
def single(product_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Items WHERE ProductID = %s", (product_id))
    product = cursor.fetchone()
    return render_template('single.html', product=product)


# logout
@app.route('/logout')
def logout():
    session.pop('key', None)
    return redirect('/login')


# mpesa payment
@app.route('/mpesa', methods=['POST', 'GET'])
def mpesa():
    if request.method == "POST":
        phone = str(request.form['phone'])
        qty = request.form['qty']
        amount = 1
        totalamount = str(amount * qty)
        # GENERATINMG ACCESS TOKEN
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "1",  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "ShopIt Limited",
            "TransactionDesc": "Pay goods on ShopIt"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        return response.text
    else:
        return "Invalid Request"


if __name__ == "__main__":
    app.run(debug=True)
