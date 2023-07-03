FROM ubi8/python-38

WORKDIR /app

USER root

EXPOSE 8000

COPY ./requirements.txt .

COPY ./src .

ADD https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/openshift-client-linux.tar.gz /app/

RUN tar -xzvf /app/openshift-client-linux.tar.gz

RUN chmod 754 /app/oc

RUN rm /app/kubectl /app/README.md

RUN pip install -r requirements.txt

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "faa:app"]
