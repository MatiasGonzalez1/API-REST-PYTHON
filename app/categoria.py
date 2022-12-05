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

#GET X ID ####################################
@app.route('/categoria/<id>', methods=['GET'])
def get_categoria_x_id(id):
  una_categoria = Categoria.query.get(id)
  return categoria_schema.jsonify(una_categoria)

#POST ########################################
@app.route('/categoria', methods=['POST'])
def insert_categoria():
  data = request.get_json(force=True)
  cat_nom = data['cat_nom']
  cat_desp = data['cat_desp']

  nueva_categoria = Categoria(cat_nom, cat_desp)
  db.session.add(nueva_categoria)
  db.session.commit()
  return categoria_schema.jsonify(nueva_categoria)

#PUT #########################################
@app.route('/categoria/<id>', methods=['PUT'])
def update_categoria(id):
  actualizar_categoria = Categoria.query.get(id)
  
  cat_nom = request.json['cat_nom']
  cat_desp = request.json['cat_desp']

  actualizar_categoria.cat_nom = cat_nom
  actualizar_categoria.cat_desp = cat_desp
  
  db.session.commit()
  return categoria_schema.jsonify(actualizar_categoria)


#DELETE ######################################
@app.route('/categoria/<id>', methods=['DELETE'])
def delete_categoria(id):
  eliminar_categoria = Categoria.query.get(id)
  db.session.delete(eliminar_categoria)
  db.session.commit()
  return categoria_schema.jsonify(eliminar_categoria)
  
#mensaje de bienvenida
@app.route('/',methods=['GET'])
def index():
  return jsonify({'Mensaje':'Bienvenido API rest con PY'})


#se reinicia la app cada vez que hay un cambio = nodemon
if __name__=="__main__":
  app.run(debug=True)