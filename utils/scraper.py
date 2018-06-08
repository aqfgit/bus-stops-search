import bs4 as bs
import requests

#python -m run 1.py

url = 'http://pksbielsko.stop.net.pl/rjaWyszukiwarkaPolaczen.php?pom=2&data_pol=2018-06-06&sz_el_1=RUDZICA%2C+1&sz_el_2=BIELSKO-BIA%C5%81A%2C+D.A.&z_miejsca=7221150&do_miejsca=7220108&submit=Szukaj+po%C5%82%C4%85czenia'

source = requests.get(url).text
soup = bs.BeautifulSoup(source, 'html.parser')

table = soup.find('table')
table_rows = table.find_all('tr')

for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text for i in td]
    print(row)

    



