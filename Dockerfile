FROM ubi8/python-38

WORKDIR /app

EXPOSE 8000

COPY ./requirements.txt .

COPY ./src .

ADD https://oc-bucket-rh.s3.ap-southeast-2.amazonaws.com/oc /app/

RUN pip install -r requirements.txt

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "faa:app"]
