from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import requests
from bs4 import BeautifulSoup
import re
import csv
from googlesearch import search

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", engineio_logger=True, logger=True, async_mode='threading')

class ContactCrawler:
    def __init__(self):
        self.seen_contacts = set()
        self.domains_seen = set()
        self.session = requests.Session()

    def find_emails(self, text):
        email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
        return set(email_regex.findall(text))

    def find_phones(self, text):
        phone_regex = re.compile(r'\b\d{10,12}\b')
        return set(phone_regex.findall(text))

    def find_weixin_ids(self, text):
        weixin_regex = re.compile(r'(微信|VFX|黎明拍网红节目商机)[:：]?\s*([a-zA-Z0-9]+)')
        return {match[1] for match in weixin_regex.findall(text)}

    def get_page_title(self, url):
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else 'No Title Found'
            return title.strip()
        except requests.RequestException:
            return 'No Title Found'

    def is_valid_email(self, email):
        if len(email) < 6 or email.split('@')[1].endswith(('jpg', 'gif', 'png')):
            return False
        return True

    def crawl_website(self, url, search_query, data_type):
        try:
            response = self.session.get(url)
            page_title = self.get_page_title(url)
            contacts = self.find_emails(response.text) if 'emails' in data_type else (self.find_phones(response.text) if 'phones' in data_type else self.find_weixin_ids(response.text))
            for contact in contacts:
                if contact not in self.seen_contacts:
                    self.seen_contacts.add(contact)
                    socketio.emit('new_contact', {'search_query': search_query, 'contact': contact, 'page_title': page_title, 'url': url})
                    with open('contacts.csv', 'a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([search_query, contact, page_title, url])
        except requests.RequestException:
            pass

    def background_search(self, search_query, num_results, data_type):
        for url in search(search_query, num_results=int(num_results)):
            self.crawl_website(url, search_query, data_type)

@app.route('/')
def index():
    return render_template('indexBuenoChino.html')

@socketio.on('start_search')
def handle_start_search(json):
    crawler = ContactCrawler()
    search_query = json['search_query']
    num_results = json.get('num_results', 10)  # Default to 10 if not specified
    data_type = json.get('data_type', 'emails')  # Default to emails if not specified
    threading.Thread(target=crawler.background_search, args=(search_query, num_results, data_type)).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5050)
