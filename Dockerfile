# cat Dockerfile
FROM ubuntu:22.04

ENV PYTHON_VERSION=3.10

# 필요 패키지 설치
RUN \
    apt-get update && \
    apt-get install -y python${PYTHON_VERSION} && \
    apt-get install -y python3-pip && \
    apt-get clean

RUN ln -s /usr/bin/python3 /usr/bin/python

# 앱 디렉터리 생성
WORKDIR /app

RUN \
   echo 'alias python="/usr/bin/python3"' >> /root/.bashrc && \
   echo 'alias pip="/usr/bin/pip3"' >> /root/.bashrc && \
   . /root/.bashrc

# 필요한 파일 복사
COPY app.py /app
COPY templates /app/templates
# COPY static /app/static

# Flask 설치
RUN pip install Flask

# 앱 실행
CMD ["python", "app.py"]
