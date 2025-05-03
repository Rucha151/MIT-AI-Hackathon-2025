# MIT-AI-Hackathon-2025
# AI-Powered Personal CRM Assistant

An AI-powered assistant that extracts contact details from business cards, images, and PDFs, organizes them into a searchable database, and sends personalized LinkedIn connection requests.

## 🚀 Features

* 📤 Upload business cards, PDFs, or photos to extract contact info
* 🧠 NLP and OCR pipeline using Tesseract and spaCy
* 🗃️ Store and search contacts via SQLite
* 🔗 Send LinkedIn connection requests with custom messages (via Selenium)
* 🖥️ Lightweight frontend with drag-and-drop UI

## 🧰 Tech Stack

* **Python**, **Flask** – API and server
* **Tesseract OCR** – Extract text from images
* **spaCy** – Named Entity Recognition for contacts
* **SQLite** – Contact database
* **Selenium + ChromeDriver** – LinkedIn automation
* **HTML/CSS/JS** – Frontend
* **Docker** – Containerization

## 📦 Installation

### Option 1: Run with Docker

```bash
git clone https://github.com/your-username/personal-crm-assistant.git
cd personal-crm-assistant
docker build -t personal-crm .
docker run -p 5000:5000 personal-crm
```

### Option 2: Run locally

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python personal_crm_assistant.py
```

## 🔍 API Endpoints

* `POST /upload` – Upload a file for contact extraction
* `GET /search?q=John` – Search contacts
* `POST /linkedin/connect` – Send LinkedIn request (requires logged-in Chrome session)

## 🖼️ Frontend Usage

Open `index.html` in your browser. Make sure the backend is running on `localhost:5000`.

## ⚠️ Limitations

* LinkedIn automation requires manual login into the browser.
* Running Selenium inside Docker may require GUI or headless setup.
* Not suitable for production without HTTPS and authentication.

## 📌 To-Do

* ✅ Improve OCR accuracy with layout parsing
* 🛠️ Batch processing for Excel/CSV
* 🌐 Chrome Extension integration

## 🧠 Credits

Built as a 12-hour project using open-source tools. Contributions welcome!
