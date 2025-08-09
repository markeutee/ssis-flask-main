"""Application entry point."""

from ssis import create_app
from dotenv import load_dotenv


load_dotenv()  # Load .env variables


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

