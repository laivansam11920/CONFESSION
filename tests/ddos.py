from requests import post
import time

while True:
    i=post("https://confession-pdsi.onrender.com/submit-confession-form")
    print(i.status_code)
    print(i.text)
    time.sleep(60)