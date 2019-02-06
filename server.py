from flask import render_template
import connexion
from producer import create

# Create the application instance
app = connexion.App(__name__, specification_dir='./')

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')

# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    return '<a href="api/ui/">Bem vindos. Acessar Swagger UI</a>'


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    
    with app.app_context():
        # Classe definida só para postar uma mensagem inicial, visando criar o tópico
        class Texto:
          def __init__(self, msg, n):
            self.texto = msg
          def get(self, m, n):
            return self.texto
        print(str(create(Texto("Iniciando Producer para o Kafka...",""))))
    
    app.run(host='0.0.0.0', port=5001, debug=True)
