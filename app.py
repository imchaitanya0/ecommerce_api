from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os

load_dotenv()

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['JWT_SECRET_KEY']=os.getenv('JWT_SECRET_KEY')

db=SQLAlchemy(app)
jwt=JWTManager(app)
bcrypt=Bcrypt(app)
limiter=Limiter(
    get_remote_address,
    app=app,
    default_limits=("100 per minute"),
    storage_uri='memory://'
    )


from routes import auth,products,orders

app.register_blueprint(auth.bp)
app.register_blueprint(products.bp)
app.register(orders.bp)

@app.errorhandler(404)
def error_not_found():
    return jsonify({'msg':'not found'}),404

@app.errorhandler(500)
def internal_server():
    return jsonify({'msg':'internal server error'})

def init_db():
    with app.app_context():
        db.create_all()

if __name__=='__main__':
    init_db()
    app.run(debug=True)