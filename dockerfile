# 1. Base image: Python 3.9 ka halka version use karenge
FROM python:3.9-slim

# 2. Container ke andar humara working folder /app hoga
WORKDIR /app

# 3. Mac ke folder se saara code container ke /app folder mein copy karo
COPY . /app

# 4. Requirements install karo
RUN pip install --no-cache-dir -r requirements.txt

# 5. Container start hote hi yeh command chalegi
CMD ["python", "app.py"]