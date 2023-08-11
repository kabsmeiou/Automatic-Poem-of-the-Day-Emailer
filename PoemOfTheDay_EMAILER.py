import requests
from bs4 import BeautifulSoup

import time
from datetime import date

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

now = str(date.today())

def poem_url_requester(URL):
    response = requests.get(URL)
    if response.status_code == 200:
        return response.content
    else:
        print("Failed to access url.")
        return None

def send_mail():
    email_content = ''
    URL = "https://www.poetryfoundation.org/"
    content = poem_url_requester(URL)
    soup = BeautifulSoup(content, 'html.parser')
    poem_content_url = ''
    poem_of_the_day = soup.find('h2', class_="c-hdgSerif c-hdgSerif_3")

    if poem_of_the_day:
        poem_link = poem_of_the_day.find('a', href=True)
        if poem_link:
            poem_url = poem_link['href']
            print("Poem link found! Extracting Poem...\n")
            poem_content_url = poem_url_requester(poem_url)
        else:
            print("No poem link found.")
    else:
        print('Error! Poem not found.')

    poem_soup = BeautifulSoup(poem_content_url, 'html.parser')
    poem_title = poem_soup.find('h1').text.strip()
    poem_author = poem_soup.find('span', class_="c-txt c-txt_attribution").text.strip()
    
    #with open(f'python/PoemOfTheDay({now}).txt', 'w') as f:
    email_content += poem_title + '<br>' + poem_author + '<br><br>' 
        #f.write(f'{poem_title}\n')
        #f.write(f'{poem_author}\n\n')
        #print("File saved.")

        #find all elements of div and iterate through each line of the poem
        
    poem_content = poem_soup.find_all('div', style="text-indent: -1em; padding-left: 1em;")
    for lines in poem_content:
        line = lines.text.strip()
        email_content += line + '<br>'
        #f.write(f'{line}\n')

    print("Composing EMAIL...\n")
    SERVER = 'smtp.gmail.com'
    PORT = 587
    SENDER = 'randomusername@gmail.com'
    RECIPIENT = 'anotherusername@gmail.com'
    PASSWORD = 'somepassword'

    msg = MIMEMultipart()

    msg['Subject'] = "Poem of the Day " + now
    msg['From'] = SENDER
    msg['To'] = RECIPIENT

    msg.attach(MIMEText(email_content, 'html'))

    print('Initializing Server...\n')

    server = smtplib.SMTP(SERVER, PORT)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(SENDER, PASSWORD)
    server.sendmail(SENDER, RECIPIENT, msg.as_string())
    server.quit()
    print('EMAIL sent.')

if __name__ == '__main__':
    while True:
        send_mail()
        time.sleep(86400)