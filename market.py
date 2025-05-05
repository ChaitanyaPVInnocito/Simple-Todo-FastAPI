from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/market')
def market_page():
    items = [
        {'id': '1', 'name': 'water', 'barcode': '245123452345' , 'price': 1.00},
        {'id': '2', 'name': 'soda', 'barcode': '245123452345' , 'price': 1.50},
        {'id': '3', 'name': 'juice', 'barcode': '245123452345' , 'price': 2.00},
        {'id': '4', 'name': 'milk', 'barcode': '245123452345' , 'price': 1.20},
        {'id': '5', 'name': 'coffee', 'barcode': '245123452345' , 'price': 2.50}
    ]
    return render_template('market.html', items=items)