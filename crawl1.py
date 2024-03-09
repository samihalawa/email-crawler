import re
import requests
from googlesearch import search
import os
import csv
from bs4 import BeautifulSoup

def find_emails(text):
    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
    return set(email_regex.findall(text))

def get_page_title(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'No Title Found'
        return title.strip()
    except requests.RequestException:
        return 'No Title Found'

def crawl_website(url, search_query, csv_writer, seen_emails):
    try:
        response = requests.get(url)
        page_title = get_page_title(url)
        emails = find_emails(response.text)
        
        for email in emails:
            if email not in seen_emails and not email.startswith('ejemplo'):
                print(f"{email} ({page_title})")
                csv_writer.writerow([search_query, email, page_title, url])
                seen_emails.add(email)
    except requests.RequestException:
        pass

def google_search(query, csv_writer, seen_emails):
    for url in search(query, num_results=50):
        crawl_website(url, query, csv_writer, seen_emails)

def main():
    csv_file_path = 'emails1.csv'
    
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if os.stat(csv_file_path).st_size == 0:
            writer.writerow(["Search Term", "Email", "Page Title", "URL"])
        
        seen_emails = set()
        while True:
            try:
                search_query = input("Please enter the search term (or type 'exit' to quit): ")
                if search_query.lower() == 'exit':
                    print("Exiting the program.")
                    break
                
                google_search(search_query, writer, seen_emails)
                
            except KeyboardInterrupt:
                print("\nProcess interrupted by user. Exiting.")
                break

if __name__ == "__main__":
    main()
