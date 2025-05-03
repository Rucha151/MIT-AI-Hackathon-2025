FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr libglib2.0-0 libnss3 libxss1 libgconf-2-4 \
    libappindicator1 libasound2 libatk-bridge2.0-0 libgtk-3-0 \
    curl unzip wget fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Work directory
WORKDIR /app

# Copy files
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Install spaCy model separately to avoid partial build fails
RUN python3 -m spacy download en_core_web_sm

COPY . .

EXPOSE 5000
CMD ["python3", "personal_crm_assistant.py"]

