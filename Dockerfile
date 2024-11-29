# 베이스 이미지로 Python 사용
FROM python:3.9-slim

# 앱 디렉터리 생성
WORKDIR /app

# 필요한 파일 복사
COPY app.py /app
COPY templates /app/templates
# COPY static /app/static

# Flask 설치
RUN pip install Flask

# 앱 실행
CMD ["python", "app.py"]
