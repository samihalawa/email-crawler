import psycopg2
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import threading
import requests
from bs4 import BeautifulSoup
import re
from googlesearch import search
import csv
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", engineio_logger=True, logger=True, async_mode='threading')

seen_emails = set()
domains_seen = set()

# Patterns to exclude common invalid cases
invalid_patterns = [r'\.png$', r'\.jpg$', r'\.jpeg$', r'\.gif$', r'\.bmp$', r'^no-reply@', r'^prueba@', r'^\d+[a-z]*@']
typo_domains = ["gmil.com", "gmal.com", "gmaill.com", "gnail.com"]
MIN_EMAIL_LENGTH = 6
MAX_EMAIL_LENGTH = 254

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('POSTGRESQL_ADDON_DB'),
            user=os.getenv('POSTGRESQL_ADDON_USER'),
            password=os.getenv('POSTGRESQL_ADDON_PASSWORD'),
            host=os.getenv('POSTGRESQL_ADDON_HOST'),
            port=os.getenv('POSTGRESQL_ADDON_PORT')
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error: Could not connect to the PostgreSQL database. Detail: {e}")
        return None

def is_valid_email(email):
    if len(email) < MIN_EMAIL_LENGTH or len(email) > MAX_EMAIL_LENGTH:
        return False
    for pattern in invalid_patterns:
        if re.search(pattern, email, re.IGNORECASE):
            return False
    domain = email.split('@')[1]
    if domain in typo_domains:
        return False
    return True

def find_emails(text):
    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
    all_emails = set(email_regex.findall(text))
    valid_emails = {email for email in all_emails if is_valid_email(email)}
    return valid_emails

def get_page_title(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'No Title Found'
        return title.strip()
    except requests.RequestException:
        return 'No Title Found'

def crawl_website(url, search_query):
    global domains_seen
    try:
        response = requests.get(url)
        page_title = get_page_title(url)
        emails = find_emails(response.text)
        conn = get_db_connection()
        if conn is None:
            print("Error: Could not establish database connection.")
            return
        cur = conn.cursor()
        for email in emails:
            domain = email.split('@')[1]
            if email not in seen_emails and domain not in domains_seen:
                seen_emails.add(email)
                domains_seen.add(domain)
                socketio.emit('new_email', {'search_query': search_query, 'email': email, 'page_title': page_title, 'url': url})
                with open('emails.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([search_query, email, page_title, url])

                # Save to PostgreSQL
                cur.execute("""
                    INSERT INTO leads_copy (email, lead_source, url)
                    VALUES (%s, %s, %s)
                """, (email, search_query, url))
        conn.commit()
        cur.close()
        conn.close()
    except requests.RequestException:
        pass

def background_search(search_query, num_results):
    for url in search(search_query, num_results=int(num_results)):
        crawl_website(url, search_query)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/readData', methods=['GET'])
def read_data():
    data = []
    try:
        with open('emails.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(data)

@app.route('/csv-table')
def csv_table():
    return render_template('csv-table.html')

@app.route('/postgres-table')
def postgres_table():
    data = []
    conn = get_db_connection()
    if conn is None:
        return "Error: Could not connect to the database."
    cur = conn.cursor()
    cur.execute('SELECT email, lead_source, url FROM leads_copy')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    for row in rows:
        data.append({'email': row[0], 'lead_source': row[1], 'url': row[2]})
    return render_template('postgres-table.html', data=data)

@socketio.on('start_search')
def handle_start_search(json):
    global seen_emails, domains_seen
    seen_emails.clear()
    domains_seen.clear()
    search_query = json['search_query']
    num_results = json.get('num_results', 10)
    threading.Thread(target=background_search, args=(search_query, num_results)).start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, port=5050)