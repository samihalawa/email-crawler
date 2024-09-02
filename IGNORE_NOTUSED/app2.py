from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import requests
from bs4 import BeautifulSoup
import re
from googlesearch import search
import csv
from collections import defaultdict

app = Flask(__name__)
# Asegúrate de configurar correctamente CORS y el modo de trabajo de SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", engineio_logger=True, logger=True, async_mode='threading')

seen_emails = set()
domain_counts = defaultdict(int)

def find_emails(text):
    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
    return set(email_regex.findall(text))

def get_page_title(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'  # Especifica la codificación como UTF-8
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'No Title Found'
        return title.strip()
    except requests.RequestException:
        return 'No Title Found'

def crawl_website(url, search_query):
    try:
        response = requests.get(url)
        page_title = get_page_title(url)
        emails = find_emails(response.text)
        for email in emails:
            if "ejemplo" in email:
                continue
            domain = email.split('@')[-1]
            if domain in ["qq.com", "gmail.com", "yahoo.com", "hotmail.com"]:  # Allow unlimited emails from common domains
                max_emails_per_domain = float('inf')
            else:
                max_emails_per_domain = 2
            if domain_counts[domain] < max_emails_per_domain:
                seen_emails.add(email)
                domain_counts[domain] += 1
                socketio.emit('new_email', {'search_query': search_query, 'email': email, 'page_title': page_title, 'url': url})  # Emit event using socketio
                with open('emails.csv', 'r+', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    existing_emails = set(row[1] for row in reader)
                    if email not in existing_emails:
                        writer = csv.writer(file)
                        writer.writerow([search_query, email, page_title, url])
    except requests.RequestException:
        pass

def background_search(search_query):
    total_emails = 0  # Contador para el total de emails obtenidos
    for url in search(search_query, num_results=30):
        if total_emails >= 30:
            break  # Detener la búsqueda si ya se han obtenido 30 emails
        crawl_website(url, search_query)
        total_emails += 1


@app.route('/')
def index():
    return render_template('index111.html')

@app.route('/get_emails')
def get_emails():
    with open('emails.csv', 'r', encoding='utf-8') as file:
        emails = file.read()
    return emails

@socketio.on('start_search')
def handle_start_search(json):
    global seen_emails, domain_counts
    seen_emails.clear()  # Clear previously seen emails for each new search
    domain_counts = defaultdict(int)  # Reset domain counts
    search_query = json['search_query']
    threading.Thread(target=background_search, args=(search_query,)).start()

if __name__ == '__main__':
    # Elimina la línea de socketio.run() y simplemente inicia la aplicación Flask
    app.run(host='0.0.0.0', debug=True, port=5050)
