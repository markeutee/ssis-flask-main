"""Application entry point."""

from ssis import create_app
from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)

load_dotenv()  


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

