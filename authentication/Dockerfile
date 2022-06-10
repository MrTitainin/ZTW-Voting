FROM python
WORKDIR /authentication
ENV FLASK_APP=authenticationServer.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 6123
COPY . .
#CMD ["flask", "run"]
CMD ["python3","authenticationServer.py"]