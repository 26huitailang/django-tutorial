FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /deploy/Downloads
WORKDIR /deploy
COPY . .
RUN pip install -r requirements/develop.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
