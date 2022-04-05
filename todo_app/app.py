from flask import Flask, render_template, redirect
from flask.globals import request
from todo_app.data.viewmodel import ViewModel
from todo_app.flask_config import Config

from todo_app.data.trello_service import TrelloService

def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config.from_object('todo_app.flask_config.Config')
    trello_service = TrelloService()

    @app.route('/')
    def index():
        items = trello_service.get_items()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/create', methods=['POST'])
    def create():
        title = request.form.get('title')
        trello_service.add_item(title)
        return redirect('/')

    @app.route('/complete/<id>', methods=['POST'])
    def complete(id):
        list_id = request.args.get('list_id')
        trello_service.complete_item(id, list_id)
        return redirect('/')

    return app