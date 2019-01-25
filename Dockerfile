FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /deploy/Downloads
WORKDIR /deploy
COPY . /deploy/
RUN pip install -r requirements/develop.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
