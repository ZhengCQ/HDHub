FROM python:3.6

COPY ./back-end /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt && pip install pymysql gunicorn
ENV FLASK_APP madblog.py
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
