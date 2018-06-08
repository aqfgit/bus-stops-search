import bs4 as bs
import requests

#python -m run 1.py
def run():
    url = 'http://pksbielsko.stop.net.pl/rjaWyszukiwarkaPolaczen.php?pom=2&data_pol=2018-06-06&sz_el_1=RUDZICA%2C+1&sz_el_2=BIELSKO-BIAŁA%2C+D.A.&z_miejsca=7221150&do_miejsca=7220108&submit=Szukaj+po%C5%82%C4%85czenia'

    source = requests.get(url)
    source.encoding = 'utf-8'
    soup = bs.BeautifulSoup(source.text, 'html.parser')

    table = soup.find('table')
    table_rows = table.find_all('tr')

    rows = []

    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        rows.append(row)

    with open('somefile.txt', 'w') as the_file:
        the_file.write(rows[1][5])

    return rows
   
