# apps.py
from flask_app import create_app

# Create Flask app using the factory pattern
app = create_app()

if __name__ == "__main__":
    # Run the Flask server
    app.run(
        host="0.0.0.0",  # allows access from any device in your network
        port=5000,       # default Flask port
        debug=True       # auto-reloads on file changes + shows detailed errors
    )
