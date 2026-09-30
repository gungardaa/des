# 1 image untuk kedua pihak (sender & receiver beda command di compose.yaml).
FROM python:3.12-slim
WORKDIR /app
COPY des.py sender.py receiver.py ./
CMD ["python", "sender.py"]
