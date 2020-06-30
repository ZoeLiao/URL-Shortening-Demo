FROM tiangolo/uwsgi-nginx:python3.7
COPY . /backend
WORKDIR /backend
ENV UWSGI_INI ./backend/uwsgi.ini
COPY entrypoint.sh /entrypoint.sh

RUN pip3 install -r requirements.txt

ENTRYPOINT ["sh", "/entrypoint.sh"]
EXPOSE 8000
