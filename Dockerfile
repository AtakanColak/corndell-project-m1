FROM python:3.9-buster AS builder

ENV FIREFOX_VER 87.0

EXPOSE 3000
WORKDIR /todo_parent
RUN pip install "poetry==1.1.4"
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install
COPY todo_app todo_app

FROM builder as development
CMD ["poetry" "run", "flask", "run"]

FROM builder as production
CMD ["poetry","run","gunicorn","-w","4","-b","0.0.0.0:3000","todo_app.wsgi:app"]

FROM builder as test
COPY tests tests
COPY .env.test tests/.env.test
ENTRYPOINT ["poetry", "run", "pytest", "tests"]

FROM builder as e2e_test
COPY selenium_tests selenium_tests

WORKDIR /

ADD https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz .
RUN tar xzvf /geckodriver-v0.31.0-linux64.tar.gz \
    && mv /geckodriver /usr/bin

RUN set -x \
   && apt update \
   && apt upgrade -y \
   && apt install -y \
       firefox-esr 

RUN set -x \
   && apt install -y \
       libx11-xcb1 \
       libdbus-glib-1-2 \
   && curl -sSLO https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VER}/linux-x86_64/en-US/firefox-${FIREFOX_VER}.tar.bz2 \
   && tar -jxf firefox-* \
   && mv firefox /opt/ \
   && chmod 755 /opt/firefox \
   && chmod 755 /opt/firefox/firefox

WORKDIR /todo_parent
ENTRYPOINT ["poetry", "run", "pytest", "selenium_tests"]