FROM python
WORKDIR /server
ENV FLASK_APP=votingServer.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5123
COPY . .
CMD ["flask", "run"]