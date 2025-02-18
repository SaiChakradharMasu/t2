FROM python:3.12-slim-bookworm

WORKDIR /app

# RUN apt-get update && \
#     apt-get install -y libmariadb3 libmariadb-dev
    
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "main.py"]