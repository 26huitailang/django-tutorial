FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /deploy
WORKDIR /deploy
COPY . /deploy/
RUN pip install -r requirements/develop.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
