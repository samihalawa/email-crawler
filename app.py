from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import requests
from bs4 import BeautifulSoup
import re
from googlesearch import search
import csv

app = Flask(__name__)
socketio = SocketIO(app)
seen_emails = set()

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
            if email not in seen_emails:
                seen_emails.add(email)
                socketio.emit('new_email', {'search_query': search_query, 'email': email, 'page_title': page_title, 'url': url})  # Emit event using socketio
                with open('emails.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([search_query, email, page_title, url])
    except requests.RequestException:
        pass



def background_search(search_query):
    for url in search(search_query, num_results=50):
        crawl_website(url, search_query)

@app.route('/')
def index():
    return render_template('index.html')

    @app.route('/get_emails')
    def get_emails():
        with open('emails.csv', 'r', encoding='utf-8') as file:
            emails = file.read()
        return emails
    

@socketio.on('start_search')
def handle_start_search(json):
    global seen_emails
    seen_emails.clear()  # Clear previously seen emails for each new search
    search_query = json['search_query']
    threading.Thread(target=background_search, args=(search_query,)).start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, port=5050)
