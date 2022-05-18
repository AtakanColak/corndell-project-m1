from dotenv import find_dotenv, load_dotenv
from todo_app import create_app
from todo_app.data.trello_service import TrelloService

app = create_app()
if __name__ == "__main__":
    app.run()