FROM python:3.8.10

COPY . /app
WORKDIR /app

RUN pip install eth-brownie
RUN apt-get update || : && apt-get install -y nodejs \
    npm                       # note this one
RUN npm install -g ganache-cli
RUN brownie pm install OpenZeppelin/openzeppelin-contracts@4.4.2

#RUN brownie pm clone OpenZeppelin/openzeppelin-contracts@4.4.2

CMD brownie test ./tests/test_CreateDS.py
