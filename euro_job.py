# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as soup
myUrl = "https://www.cursbnr.ro/"

import requests

url = 'http://france.meteofrance.com/france/meteo?PREVISIONS_PORTLET.path=previsionsville/750560'
page = requests.get(myUrl)

soup_page = soup(page.text, "html.parser")

cont1 = soup_page.find_all("div", {"class": "currency-value"})
for i in cont1:
    if 'EURO' in i.div.text and "Lei" in i.div.text:
        divs = i.find_all("div")
        crt_euro_full = divs[0].text
        variation = divs[1].text
        crt_euro = str(crt_euro_full).split("=")[1].replace(" Lei", "").strip()


cont2 = soup_page.find_all('p')[4]
table = cont2.find_next_sibling('table')
all_trs = table.find_all("tr")
ind = 0
for i in all_trs[0]:
    try:
        if i.text == "Euro min":
            index = ind
            break
        ind += 1
    except:
        pass
min_values = []
for i in range(1, len(all_trs)):
    all_tds = all_trs[i].find_all("td")
    min_values.append(float(str((all_tds[index].text))))


eur = "Curs euro: " + crt_euro
vars = "Delta: " + variation.split(" ")[0]
min_list = "Valori minime: " + str(min_values)
for value in min_values:
    if value > float(crt_euro):
        answer = "BUYYYYYYYYYYYYYYYYYY"
msg = "\r\n".join([eur, vars, min_list, ])
#print msg


def send_email(user, pwd, recipient, subject, body):
    import smtplib
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")

to_list = ["salexcme@gmail.com"]
send_email("alexrinf", "4Testing", to_list , "CURS EURO", msg)