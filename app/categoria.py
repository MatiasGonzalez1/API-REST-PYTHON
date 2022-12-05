from flask import Flask,jsonify

# codigo necesario para correr la app
app = Flask(__name__)

#mensaje de bienvenida
@app.route('/',methods=['GET'])
def index():
  return jsonify({'Mensaje':'Bienvenido API rest con PY'})


#se reinicia la app cada vez que hay un cambio = nodemon
if __name__=="__main__":
  app.run(debug=True)