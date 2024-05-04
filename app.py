from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import requests
from bs4 import BeautifulSoup
import re
from googlesearch import search
import csv

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", engineio_logger=True, logger=True, async_mode='threading')

seen_emails = set()
domains_seen = set()

# Patterns to exclude common invalid cases
invalid_patterns = [
    r'\.png$',  # File extensions
    r'\.jpg$',
    r'\.jpeg$',
    r'\.gif$',
    r'\.bmp$',
    r'^no-reply@',
    r'^prueba@',
    r'^\d+[a-z]*@',
]

# Common typo domains
typo_domains = ["gmil.com", "gmal.com", "gmaill.com", "gnail.com"]

# Email validation criteria
MIN_EMAIL_LENGTH = 6
MAX_EMAIL_LENGTH = 254

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
        for email in emails:
            domain = email.split('@')[1]
            if email not in seen_emails and domain not in domains_seen:
                seen_emails.add(email)
                domains_seen.add(domain)
                socketio.emit('new_email', {'search_query': search_query, 'email': email, 'page_title': page_title, 'url': url})
                with open('emails.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([search_query, email, page_title, url])
    except requests.RequestException:
        pass

def background_search(search_query, num_results):
    for url in search(search_query, num_results=int(num_results)):
        crawl_website(url, search_query)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/saved-emails')
def saved_emails():
    data = []

    # Read the CSV file and parse its content
    with open('emails.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return render_template('saved_emails.html', data=data)


@socketio.on('start_search')
def handle_start_search(json):
    global seen_emails, domains_seen
    seen_emails.clear()
    domains_seen.clear()
    search_query = json['search_query']
    num_results = json.get('num_results', 10)  # Default to 10 if not specified
    threading.Thread(target=background_search, args=(search_query, num_results)).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5050)
