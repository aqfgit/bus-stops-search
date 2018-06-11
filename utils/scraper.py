import bs4 as bs
import requests
import datetime
import json
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


def get_current_date_chunks():
    now = datetime.datetime.now().strftime("%Y%m%d")
    date_chunks = {
        'year': now[:4],
        'month': now[4:6],
        'day': now[6:]
    }

    return date_chunks


def get_table_data(url):
    source = requests.get(url)
    source.encoding = 'utf-8'
    soup = bs.BeautifulSoup(source.text, 'html.parser')

    table = soup.find('table')
    table_rows = table.find_all('tr')

    rows = []

    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        print(row[1])
        rows.append(row)

    return rows


def parse_table_rows_to_json(data):
    rows = {'rows': []}
    for count, row in enumerate(data):
        if count == 0:  # first row contains table headers, which we don't need
            continue

        rows['rows'].append({
            'time_start': row[1],
            'time_end': row[2],
            'info': row[5]
        })

    json_rows = json.dumps(rows, ensure_ascii=False).encode('utf8')
    return json_rows


def run(raw_data):
    raw_data = str(raw_data, 'utf-8')
    bus_stops = json.loads(raw_data)

    date_chunks = get_current_date_chunks()

    base_url = (
        'http://pksbielsko.stop.net.pl/rjaWyszukiwarkaPolaczen.php?data_pol={0}-{1}-{2}&pom=1&'
        'z_miejsca={3}&'
        'do_miejsca={4}&'
        'submit=Szukaj+po%C5%82%C4%85czenia'
        ).format(
            date_chunks['year'], date_chunks['month'], date_chunks['day'],
            bus_stops['from'], bus_stops['to']
            )
    print(base_url)
    try:
        bus_stops_ids = get_bus_stops_ids(base_url)
    except AttributeError:
        return 'Sprawdź nazwy przystanków.'

    final_url = (
        'http://pksbielsko.stop.net.pl/rjaWyszukiwarkaPolaczen.php?pom=2&data_pol={0}-{1}-{2}&'
        'sz_el_1={3}&'
        'sz_el_2={4}&'
        'z_miejsca={5}&do_miejsca={6}&'
        'submit=Szukaj+po%C5%82%C4%85czenia'
        ).format(
            date_chunks['year'], date_chunks['month'], date_chunks['day'],
            bus_stops['from'], bus_stops['to'],
            bus_stops_ids['from'], bus_stops_ids['to']
            )

    try:
        table_data = get_table_data(final_url)
        json_data = parse_table_rows_to_json(table_data)
        return json_data
    except AttributeError:
        return 'Autobusy nie na tej trasie nie kursują w tym dniu lub połączenie nie istnieje.'
