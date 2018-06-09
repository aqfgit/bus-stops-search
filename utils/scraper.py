import bs4 as bs
import requests
import datetime

# python -m run 1.py


# The bus search website where I'm pulling data from
# needs the user to submit essentialy the same form twice.
# The first time the user actually has to select bus stops.
# Then then the user is presented with the comfirmation page,
# where another button has to be pressed.
# So to recreate the first phase, i just need bus stops names
# and for the second phase, for some reason i also need to pass
# bus stops id's to the url, which are stored in option fields
# on the confirmation page.

def get_bus_stops_ids(url):
    source = requests.get(url)
    source.encoding = 'utf-8'
    soup = bs.BeautifulSoup(source.text, 'html.parser')

    form = soup.find('form', class_='rja_form')
    id_from = form.find('select', {'name': 'z_miejsca'}).option['value']
    id_to = form.find('select', {'name': 'do_miejsca'}).option['value']

    ids = {'from': id_from, 'to': id_to}
    return ids


def get_current_date_chunks() {
    now = datetime.datetime.now().strftime("%Y%m%d")
    date_chunks = {
        'year': now[:4],
        'month': now[4:6],
        'day': now[6:]
    }

    return date_chunks
}

def run():
    base_url = 'http://pksbielsko.stop.net.pl/rjaWyszukiwarkaPolaczen.php?data_pol=2018-06-09&pom=1&z_miejsca=I%C5%81OWNICA%2C+CENTRUM&do_miejsca=RUDZICA%2C+2&submit=Szukaj+po%C5%82%C4%85czenia'
    
    return get_bus_stops_ids(base_url)

    # source = requests.get(url)
    # source.encoding = 'utf-8'
    # soup = bs.BeautifulSoup(source.text, 'html.parser')

    # table = soup.find('table')
    # table_rows = table.find_all('tr')

    # rows = []

    # for tr in table_rows:
    #     td = tr.find_all('td')
    #     row = [i.text for i in td]
    #     rows.append(row)

    # return rows
