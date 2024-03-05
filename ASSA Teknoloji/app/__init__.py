# app/__init__.py

# Bu kod, Flask kullanarak iki farklı Flask uygulaması oluşturur. İlk uygulama, 
# HTML formu aracılığıyla kullanılan bir arayüz sağlar ve HTML dosyalarını 
# '/templates' dizininden alır. 
# İkinci uygulama ise bir API hizmeti olarak kullanılır ve diğer programlarla 
# iletişim kurmak için tasarlanmıştır. routes modülü, her iki uygulamanın da 
# yönlendirmelerini ve işlevselliğini içerir.

# Import Flask class from the flask module
from flask import Flask

# Create Flask application for HTML usage - TEST
# Set the template folder path to '/templates'
# app = Flask(__name__, template_folder='C:/Users/dagac/Desktop/github/DEMO/ASSA Teknoloji/templates/')

# Create Flask application for API service - POSTMAN
# Initialize Flask application
app = Flask(__name__)

# Import and use the routes module
from app import routes