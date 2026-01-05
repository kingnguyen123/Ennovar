from flask import Flask
from flask_cors import CORS
from backend.routes.products import products_bp
from backend.routes.sales import sales_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(products_bp)
app.register_blueprint(sales_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)