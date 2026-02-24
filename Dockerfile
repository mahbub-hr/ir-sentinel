FROM python:3.10-slim

RUN apt update && apt install -y clang llvm

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requiremeents.txt

COPY . .
CMD ["python", "server.py"]
