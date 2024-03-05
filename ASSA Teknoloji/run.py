# run.py

# Bu kod, Flask uygulamasını çalıştırmak için kullanılır. 'app' değişkeni, 
# Flask uygulamasını içeren 'app' modülünden alınır. Daha sonra, kod, 
# bu betik doğrudan ana program olarak çalıştırıldığında Flask uygulamasını 
# hata ayıklama modunda çalıştırır.

# Import the 'app' variable from the app module
from app import app

# Check if this script is executed as the main program
if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)