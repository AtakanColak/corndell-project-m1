FROM python:3.9-buster AS builder
EXPOSE 3000
RUN pip install "poetry==1.1.4"
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install
COPY ./todo_app /todo_app/

FROM builder as development
CMD ["poetry" "run", "flask", "run"]

FROM builder as production
CMD ["poetry","run","gunicorn","-w","4","-b","0.0.0.0:3000","todo_app.wsgi:app"]
