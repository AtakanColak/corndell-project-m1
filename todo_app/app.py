from flask import Flask, render_template, redirect
from flask.globals import request
from todo_app.data.viewmodel import ViewModel
from todo_app.flask_config import Config

from todo_app.data.trello_items import get_items, add_item, complete_item

app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    items = get_items()
    item_view_model = ViewModel(items)
    return render_template('index.html', view_model=item_view_model)

@app.route('/create', methods=['POST'])
def create():
    title = request.form.get('title')
    add_item(title)
    return redirect('/')

@app.route('/complete/<id>', methods=['POST'])
def complete(id):
    complete_item(id)
    return redirect('/')