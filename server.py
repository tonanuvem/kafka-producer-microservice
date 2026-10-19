from flask import render_template
import connexion
from producer import create
from flask_cors import CORS

# Create the application instance
app = connexion.App(__name__, specification_dir='./')

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')
CORS(app.app,resources=r'/api/*',methods=['POST', 'OPTIONS'])

# Create a URL route in our application for "/"
@app.route('/')
def home():
    return render_template('home.html')

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    
    with app.app.app_context():
        # Mensagem inicial, visando criar o tópico
        try:
            print(str(create({"texto": "Iniciando Producer para o Kafka..."})))
        except Exception as e:
            print("Aviso: não foi possível publicar a mensagem inicial:", repr(e))
    
    app.run(host='0.0.0.0', port=5001, debug=True)
