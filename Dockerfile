FROM python:3.9-buster
EXPOSE 3000
RUN pip install "poetry==1.1.4"
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install
COPY ./todo_app /todo_app/
CMD ["poetry","run","gunicorn","-w","4","-b","0.0.0.0:3000","wsgi:app"]