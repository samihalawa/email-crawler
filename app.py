import psycopg2
from psycopg2 import pool
from flask import Flask, render_template, send_from_directory, jsonify, request
from flask_socketio import SocketIO
import threading
import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime
import csv
from googlesearch import search
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Initialize connection pool
pg_pool = psycopg2.pool.ThreadedConnectionPool(
    sslmode='require',
    minconn=1,
    maxconn=5,
    dbname=os.getenv('PGDATABASE'),
    user=os.getenv('PGUSER'),
    password=os.getenv('PGPASSWORD'),
    host=os.getenv('PGHOST'),
    port=os.getenv('PGPORT'))

# SMTP configurations
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT')
smtp_user = os.getenv('SMTP_USER')
smtp_password = os.getenv('SMTP_PASSWORD')

seen_emails = set()
domain_counts = {}  # To track email counts per domain

# Patterns to exclude common invalid cases
invalid_patterns = [
    r'\.png$', r'\.jpg$', r'\.jpeg$', r'\.gif$', r'\.bmp$', r'^no-reply@',
    r'^prueba@', r'^\d+[a-z]*@'
]
typo_domains = ["gmil.com", "gmal.com", "gmaill.com", "gnail.com"]
MIN_EMAIL_LENGTH = 6
MAX_EMAIL_LENGTH = 254

def get_db_connection():
    try:
        return pg_pool.getconn()
    except psycopg2.OperationalError as e:
        print(f"Error: Could not connect to the PostgreSQL database. Detail: {e}")
        return None

def release_db_connection(conn):
    if conn:
        pg_pool.putconn(conn)

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
    email_regex = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
    all_emails = set(email_regex.findall(text))
    valid_emails = {email for email in all_emails if is_valid_email(email)}
    return valid_emails

def get_page_title(soup):
    return soup.title.string if soup.title else 'No Title Found'

def get_meta_description(soup):
    description = soup.find('meta', attrs={'name': 'description'})
    return description['content'] if description else 'No Description Found'

def crawl_website(url, search_query, auto_send=False, email_template=''):
    global seen_emails, domain_counts
    try:
        start_time = datetime.now()
        response = requests.get(url)
        http_status = response.status_code
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        page_title = get_page_title(soup)
        meta_description = get_meta_description(soup)
        scrape_duration = datetime.now() - start_time
        emails = find_emails(response.text)

        with open('emails.csv', 'r+', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            existing_emails = set(row[1] for row in reader)

        for email in emails:
            if "ejemplo" in email:
                continue
            domain = email.split('@')[-1]
            if domain in ["qq.com", "gmail.com", "yahoo.com", "hotmail.com"]:
                max_emails_per_domain = float('inf')
            else:
                max_emails_per_domain = 2
            if domain_counts.get(domain, 0) < max_emails_per_domain:
                seen_emails.add(email)
                domain_counts[domain] = domain_counts.get(domain, 0) + 1
                if email not in existing_emails:
                    with open('emails.csv', 'a', newline='',
                              encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([search_query, email, page_title, url])

                    conn = get_db_connection()
                    if conn:
                        try:
                            cur = conn.cursor()
                            cur.execute(
                                """
                                INSERT INTO leadsgood (
                                    email, lead_source, url, page_title, meta_description, http_status, scrape_duration, scrape_batch_id, scraped_at, created_by, lead_status
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, (email, search_query, url, page_title,
                                  meta_description,
                                  http_status, scrape_duration, 'batch_id',
                                  datetime.now(), 'system', 'new'))
                            conn.commit()
                            cur.close()

                            # Add the search query to `search_queries` table if not exists
                            cur = conn.cursor()
                            cur.execute(
                                """
                                INSERT INTO search_queries (query, total_contacts)
                                VALUES (%s, %s)
                                ON CONFLICT (query) DO UPDATE
                                SET total_contacts = search_queries.total_contacts + %s
                            """, (search_query, 1, 1))
                            conn.commit()
                            cur.close()

                            # Send email if auto_send is enabled
                            if auto_send:
                                contact_info = {
                                    'email': email,
                                    'url': url,
                                    'name': page_title,
                                    'company': meta_description
                                }
                                customized_email = customize_email(
                                    email_template, contact_info)
                                send_email(email, 'Your Custom Email Subject',
                                           customized_email)

                            socketio.emit(
                                'new_email', {
                                    'search_query': search_query,
                                    'email': email,
                                    'page_title': page_title,
                                    'url': url,
                                    'meta_description': meta_description
                                })
                        finally:
                            release_db_connection(conn)
    except requests.RequestException as e:
        error_message = str(e)
        scrape_duration = datetime.now() - start_time
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT INTO leadsgood (
                        email, lead_source, url, error_message, http_status, scrape_duration,
                        scrape_batch_id, scraped_at, created_by, lead_status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, ('', search_query, url,
                      error_message, http_status, scrape_duration, 'batch_id',
                      datetime.now(), 'system', 'error'))
                conn.commit()
                cur.close()
            finally:
                release_db_connection(conn)

def send_email(recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

def customize_email(template, contact_info):
    return template.replace('<name>', contact_info['name']) \
                   .replace('<company>', contact_info['company']) \
                   .replace('<url>', contact_info['url'])

def send_campaign_email(campaign_id):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()

            cur.execute(
                "SELECT name, search_query, email_template FROM campaigns WHERE id = %s",
                (campaign_id, ))
            campaign = cur.fetchone()
            if campaign is None:
                return

            search_query, email_template = campaign[1], campaign[2]

            cur.execute(
                """
                SELECT email, name, company, url, page_title, meta_description
                FROM leadsgood
                WHERE lead_source = %s
            """, (search_query, ))
            contacts = cur.fetchall()
            for contact in contacts:
                contact_info = {
                    'email': contact[0],
                    'name': contact[1] or 'Friend',
                    'company': contact[2] or 'Your Company',
                    'url': contact[3] or 'Your Website'
                }
                customized_email = customize_email(email_template,
                                                   contact_info)
                send_email(contact_info['email'], 'Your Custom Email Subject',
                           customized_email)
                socketio.emit('email_sent', {
                    'email': contact_info['email'],
                    'status': 'SENT'
                })
        finally:
            release_db_connection(conn)

def background_search(search_query,
                      num_results,
                      auto_send=False,
                      email_template=''):
    for url in search(search_query, num_results=int(num_results)):
        crawl_website(url, search_query, auto_send, email_template)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manifest.json')
def manifest():
    return send_from_directory(app.static_folder, 'manifest.json')

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory(app.static_folder, 'service-worker.js')

@app.route('/campaigns')
def campaigns():
    return render_template('campaign.html')

@app.route('/campaigns/<int:campaign_id>')
def view_campaign(campaign_id):
    return render_template('view_campaign.html', campaign_id=campaign_id)

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
    return render_template('postgres-table.html')

@app.route('/start')
def load_start_page():
    return render_template('start.html')

@app.route('/api/readPostgresData', methods=['GET'])
def read_postgres_data():
    data = []
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    offset = (page - 1) * per_page
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'desc')
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error":
                        "Error: Could not connect to the database."}), 500
    try:
        cur = conn.cursor()
        cur.execute(
            f"""
            SELECT email, lead_source, url, page_title, meta_description, scrape_duration, http_status, created_at
            FROM leadsgood
            ORDER BY {sort_by} {order}
            LIMIT %s OFFSET %s
        """, (per_page, offset))
        rows = cur.fetchall()
        cur.execute("SELECT COUNT(*) FROM leadsgood")
        total = cur.fetchone()[0]
        cur.close()
        data.extend([{
            'email': row[0],
            'lead_source': row[1],
            'url': row[2],
            'page_title': row[3],
            'meta_description': row[4],
            'scrape_duration': str(row[5]),
            'http_status': row[6],
            'created_at': row[7]
        } for row in rows])
    finally:
        release_db_connection(conn)
    return jsonify({
        'data': data,
        'total': total,
        'page': page,
        'per_page': per_page
    })

@app.route('/api/search_queries', methods=['GET'])
def get_search_queries():
    data = []
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, query, total_contacts, created_at FROM search_queries ORDER BY created_at DESC"
            )
            rows = cur.fetchall()
            cur.close()
            data.extend([{
                'id': row[0],
                'query': row[1],
                'total_contacts': row[2],
                'created_at': row[3]
            } for row in rows])
        finally:
            release_db_connection(conn)
    return jsonify({'data': data})

@app.route('/api/campaigns', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_campaigns():
    if request.method == 'POST':
        data = request.json
        campaign_name = data.get("name")
        search_query = data.get("search_query")
        email_template = data.get("email_template")

        # Input validation
        if not all([campaign_name, search_query, email_template]):
            return jsonify({'error': 'All fields (name, search_query, email_template) are required.'}), 400

        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT INTO campaigns (name, search_query, email_template)
                    VALUES (%s, %s, %s)
                    """, (campaign_name, search_query, email_template))
                conn.commit()
                cur.close()
                return jsonify({'status': 'Campaign created successfully'})
            except Exception as e:
                # Log the exception and return an error response
                print(f"Error occurred: {e}")
                return jsonify({'error': 'Failed to create campaign. Please try again later.'}), 500
            finally:
                release_db_connection(conn)
        else:
            return jsonify({'error': 'Failed to connect to the database.'}), 500

    elif request.method == 'PUT':
        data = request.json
        campaign_id = data.get("id")
        campaign_name = data.get("name")
        search_query = data.get("search_query")
        email_template = data.get("email_template")

        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    """
                    UPDATE campaigns
                    SET name = %s, search_query = %s, email_template = %s, updated_at = NOW()
                    WHERE id = %s
                    """,
                    (campaign_name, search_query, email_template, campaign_id))
                conn.commit()
                cur.close()
            finally:
                release_db_connection(conn)
            return jsonify({'status': 'Campaign updated successfully'})

    elif request.method == 'DELETE':
        campaign_id = request.args.get("id")

        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM campaigns WHERE id = %s",
                            (campaign_id, ))
                conn.commit()
                cur.close()
            finally:
                release_db_connection(conn)
            return jsonify({'status': 'Campaign deleted successfully'})

    elif request.method == 'GET':
        data = []
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT id, name, search_query, email_template, created_at FROM campaigns ORDER BY created_at DESC"
                )
                rows = cur.fetchall()
                cur.close()
                data.extend([{
                    'id': row[0],
                    'name': row[1],
                    'search_query': row[2],
                    'email_template': row[3],
                    'created_at': row[4]
                } for row in rows])
            finally:
                release_db_connection(conn)
        return jsonify({'data': data})

    return jsonify({'error': 'Unsupported request method.'}), 405

@socketio.on('start_search')
def handle_start_search(json):
    global seen_emails, domain_counts
    seen_emails.clear()
    domain_counts.clear()
    search_query = json['search_query']
    num_results = json.get('num_results', 10)
    auto_send = json.get('auto_send', False)
    email_template = json.get('email_template', '')
    threading.Thread(target=background_search,
                     args=(search_query, num_results, auto_send,
                           email_template)).start()

@socketio.on('send_campaign')
def handle_send_campaign(json):
    campaign_id = json['campaign_id']
    threading.Thread(target=send_campaign_email, args=(campaign_id,)).start()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5050)