from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# codigo necesario para correr la app
app = Flask(__name__)

#cadena de conexiones
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root:@localhost:3306/api_rest_py'

#evita alertas y warnings de la conexión
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)

#Creacion de tabla Categoria
class Categoria(db.Model):
  cat_id = db.Column(db.Integer,primary_key=True)
  cat_nom = db.Column(db.String(100))
  cat_desp = db.Column(db.String(100))

#constructor
  def __init__(self, cat_nom, cat_desp):
    self.cat_nom = cat_nom
    self.cat_desp = cat_desp

#comando de creacion de tabla
with app.app_context():   
  db.create_all()

#esquema categoria
class CategoriaSchema(ma.Schema):
  class Meta:
    fields = ('cat_id','cat_nom','cat_desp')

#una sola respuesta
categoria_schema = CategoriaSchema()

#muchas respuestas
categorias_schema = CategoriaSchema(many=True)

#GET##########################################
@app.route('/categoria', methods=['GET'])
def get_categorias():
  all_categorias = Categoria.query.all()
  result = categorias_schema.dump(all_categorias)
  return jsonify(result)

#mensaje de bienvenida
@app.route('/',methods=['GET'])
def index():
  return jsonify({'Mensaje':'Bienvenido API rest con PY'})


#se reinicia la app cada vez que hay un cambio = nodemon
if __name__=="__main__":
  app.run(debug=True)