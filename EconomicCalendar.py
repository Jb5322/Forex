# -*- coding: utf-8 -*-
"""
Economic Events
Python web-scraper for economic events on the Bloomberg Econoday calendar. 
"""

import arrow 
import requests
from bs4 import BeautifulSoup

def calendar(url): 
    
    url = url

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 

    request = requests.get(url, headers=header) 

    soup = BeautifulSoup(request.text, 'html.parser') 

    table = soup.find('table', {'id': 'economicCalendarData'}) 

    body = table.find('tbody') 

    lines = body.findAll('tr', {'class': 'js-event-item'}) 

    calendar = [] 
    
    for tr in lines:

        time = tr.attrs['data-event-datetime'] 
        time = arrow.get(time, 'YYYY/MM/DD HH:mm:ss') 
        time = time.strftime('%H:%M')
        calendar.append(time)

        time = tr.attrs['data-event-datetime'] 
        time = arrow.get(time, 'YYYY/MM/DD HH:mm:ss') 
        hours = (int(time.strftime('%H')) * 60)
        minutes = int(time.strftime('%M'))
        verification = hours + minutes 
        calendar.append(verification) 

        column = tr.find('td', {'class': 'flagCur'}) 
        #flag = column.find('span')
        #calendar.append(flag.get('title'))
        typ = column[-6:]
        calendar.append(typ)

        impact = tr.find('td', {'class': 'sentiment'})
        bull = impact.findAll('i', {'class': 'grayFullBullishIcon'}) 
        calendar.append(len(bull))

        event = tr.find('td', {'class': 'event'})
        a = event.find('a') 

        calendar.append('{}{}'.format(url, a['href']))  

        calendar.append(a.text.strip())

    return calendar 


data = (calendar('https://www.investing.com/economic-calendar/')) 

print(data)
print('')

amount = (len(data) / 6) 

while True:
        
    verification = data[1]
    area = data[2] 
    impact = data[3] 
   
    if impact == 3 :
    
        news = (f'Area of Currency: {area}\
                \nImpact Level: {impact}\
                \n').strip() 
                
        print(news)
        print('')
        
        
    else:
        pass
    

    for item in range(0, 6):
        del data[0] 

    amount = amount - 1

    if amount == 0:
        break

    else:
        pass
    
    
    
    
    
