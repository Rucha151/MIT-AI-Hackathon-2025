# Personal CRM Assistant (Extended with LinkedIn Messaging)

import os
import pytesseract
from PIL import Image
import spacy
import sqlite3
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize NLP
nlp = spacy.load("en_core_web_sm")

# Setup Flask
app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Setup SQLite
conn = sqlite3.connect('contacts.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS contacts
             (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT, company TEXT, notes TEXT, linkedin TEXT)''')
conn.commit()

# OCR and NLP Pipeline
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # OCR
    image = Image.open(filepath)
    text = pytesseract.image_to_string(image)

    # NLP
    doc = nlp(text)
    name = email = phone = company = linkedin = ""
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            name = ent.text
        elif ent.label_ == 'ORG':
            company = ent.text
        elif '@' in ent.text:
            email = ent.text
        elif ent.text.replace('-', '').isdigit():
            phone = ent.text
        elif 'linkedin.com' in ent.text:
            linkedin = ent.text.strip()

    # Store in DB
    c.execute("INSERT INTO contacts (name, email, phone, company, notes, linkedin) VALUES (?, ?, ?, ?, ?, ?)",
              (name, email, phone, company, text, linkedin))
    conn.commit()

    return jsonify({"message": "Contact saved", "data": {"name": name, "email": email, "phone": phone, "company": company, "linkedin": linkedin}})

# Simple Search
@app.route('/')
def home():
    return "Personal CRM Assistant is running!"

@app.route('/search')
def search():
    q = request.args.get('q', '')
    c.execute("SELECT * FROM contacts WHERE name LIKE ? OR company LIKE ?", (f"%{q}%", f"%{q}%"))
    rows = c.fetchall()
    return jsonify(rows)

# LinkedIn Connect and Message (requires user login in browser session)
@app.route('/linkedin/connect', methods=['POST'])
def linkedin_connect():
    data = request.get_json()
    linkedin_url = data.get('linkedin')
    message = data.get('message')

    if not linkedin_url or not message:
        return jsonify({"error": "Missing LinkedIn URL or message."}), 400

    # Start browser
    driver = webdriver.Chrome()
    driver.get(linkedin_url)

    time.sleep(5)  # Wait for manual login or page load

    try:
        connect_button = driver.find_element(By.XPATH, '//button[contains(text(), "Connect")]')
        connect_button.click()
        time.sleep(2)
        add_note_button = driver.find_element(By.XPATH, '//button[contains(text(), "Add a note")]')
        add_note_button.click()
        time.sleep(1)
        message_box = driver.find_element(By.TAG_NAME, 'textarea')
        message_box.send_keys(message)
        send_button = driver.find_element(By.XPATH, '//button[contains(text(), "Send")]')
        send_button.click()
    except Exception as e:
        driver.quit()
        return jsonify({"error": f"Failed to send connection request: {str(e)}"}), 500

    driver.quit()
    return jsonify({"message": "LinkedIn connection request sent."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

