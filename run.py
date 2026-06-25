from app import create_app
import os


app = create_app()

if __name__ == '__main__':
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, port=5001)