FROM python:3.11-slim

WORKDIR /app

# Slim version already has what we need for basic python
# Removed heavy build tools as we don't need to build C++ extensions anymore

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
