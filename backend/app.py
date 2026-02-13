import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template
from flask_cors import CORS

from routers.cliente_router import cliente_bp

app = Flask(__name__, 
            static_folder='static',
            static_url_path='/static')
CORS(app)

app.register_blueprint(cliente_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)