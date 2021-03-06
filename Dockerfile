FROM python:3-alpine

WORKDIR /usr/src/api/
COPY . .
RUN pip install -r requirements.txt

CMD ["/bin/sh", "-c", "flask deploy-script && python main.py"]
