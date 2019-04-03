# Using Python requests and the Google Maps Geocoding API.
#
# References:
#
# * http://docs.python-requests.org/en/latest/
# * https://developers.google.com/maps/

import re
import unicodedata
import urlsigner
import requests


GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
clientId = 'put your client ID here'
key = 'put your key here'


def convert_to_abbreviation(street_address):
    street_address = re.sub('road', 'rd', street_address)
    street_address = re.sub('street', 'st', street_address)
    street_address = re.sub('boulevard', 'blvd', street_address)
    street_address = re.sub('court', 'ct', street_address)
    street_address = re.sub('terrace', 'terr', street_address)
    street_address = re.sub('circle', 'cir', street_address)
    street_address = re.sub('highway', 'hwy', street_address)
    street_address = re.sub('parkway', 'pkwy', street_address)
    street_address = re.sub('ridge', 'rdg', street_address)
    street_address = re.sub('drive', 'dr', street_address)
    street_address = re.sub('lane', 'ln', street_address)
    street_address = re.sub('north', 'n', street_address)
    street_address = re.sub('south', 's', street_address)
    street_address = re.sub('east', 'e', street_address)
    street_address = re.sub('west', 'w', street_address)

    return street_address


def check_street_match(address_component, input_address_component):

    address_types = {
        'street_address': 0,
        'route': 1,
        'intersection': 2
    }

    found_address_component = None

    if address_component['types'][0] in address_types:
        found_address_component = address_component['short_name'].lower()

    if found_address_component is None:
        return False
    elif unicodedata.normalize('NFKD', found_address_component).encode('ascii', 'ignore') == input_address_component:
        return True
    else:
        return False


def check_city_match(address_component, input_address_component):

    address_types = {
        'locality': 0,
        'administrative_area_level_3': 1
    }

    found_address_component = None

    if address_component['types'][0] in address_types:
        found_address_component = address_component['short_name'].lower()

    if found_address_component is None:
        return None
    elif unicodedata.normalize('NFKD', found_address_component).encode('ascii', 'ignore') == input_address_component:
        return True
    else:
        return False


def check_zip_code_match(address_component, input_address_component):

    address_types = {
        'postal_code': 0,
        'postal_code_prefix': 1
    }

    found_address_component = None

    if address_component['types'][0] in address_types:
        found_address_component = address_component['long_name'].lower()

    if found_address_component is None:
        return None
    elif unicodedata.normalize('NFKD', found_address_component).encode('ascii', 'ignore') == input_address_component:
        return True
    else:
        return False


def check_state_match(address_component, input_address_component):

    address_types = {
        'administrative_area_level_1': 0
    }

    found_address_component = None

    if address_component['types'][0] in address_types:
        found_address_component = address_component['short_name'].lower()

    if found_address_component is None:
        return None
    elif unicodedata.normalize('NFKD', found_address_component).encode('ascii', 'ignore') == input_address_component:
        return True
    else:
        return False


def check_country_match(address_component, input_address_component):

    address_types = {
        'country': 0
    }

    found_address_component = None

    if address_component['types'][0] in address_types:
        found_address_component = address_component['short_name'].lower()

    if found_address_component is None:
        return None
    elif unicodedata.normalize('NFKD', found_address_component).encode('ascii', 'ignore') == input_address_component:
        return True
    else:
        return False


def address_validation(street_address_input, city_input, zip_code_input, state_input, country_input):

    street_address_input = convert_to_abbreviation(street_address_input)
    street_address_input = ' '.join([word for word in street_address_input.split() if not word.isdigit()])
    address = [street_address_input, city_input, zip_code_input, state_input, country_input]
    url = GOOGLE_MAPS_API_URL + '?'
    url += 'address=' + ','.join(address).replace(' ', '+').lower()
    url += '&client=' + clientId
    signed_url = urlsigner.sign_url(url, key)

    # Do the request and get the response data
    req = requests.post(signed_url)

    res = req.json()

    # "OK" indicates that no errors occurred; the address was successfully parsed and at least one geocode was returned.
    if res['status'].upper() != 'OK':
        print res['status']
        return False

    is_street_matched = None
    is_city_matched = None
    is_zip_code_matched = None
    is_state_matched = None
    is_country_matched = None

    geodata = dict()
    for address_component in res['results'][0]['address_components']:
        if is_street_matched is None:
            is_street_matched = check_street_match(address_component, street_address_input)
        if is_city_matched is None:
            is_city_matched = check_city_match(address_component, city_input)
        if is_zip_code_matched is None:
            is_zip_code_matched = check_zip_code_match(address_component, zip_code_input)
        if is_state_matched is None:
            is_state_matched = check_state_match(address_component, state_input)
        if is_country_matched is None:
            is_country_matched = check_country_match(address_component, country_input)

        if is_street_matched is not None and is_city_matched is not None and is_zip_code_matched is not None and \
                is_state_matched is not None and is_country_matched is not None:
            geodata['lat'] = res['results'][0]['geometry']['location']['lat']
            geodata['lng'] = res['results'][0]['geometry']['location']['lng']
            geodata['formatted_address'] = res['results'][0]['formatted_address']
            break

    results = dict()

    if len(geodata) > 0:
            geodata['street'] = is_street_matched
            geodata['city'] = is_city_matched
            geodata['zip_code'] = is_zip_code_matched
            geodata['state'] = is_state_matched
            geodata['country'] = is_country_matched

    return geodata


if __name__ == "__main__":
    print ('Enter an address')
    geodata = address_validation(raw_input("Street Address:"), raw_input("City:"), raw_input("State/Province:"), raw_input("Zip Code:"), raw_input("Country:"))
    
    if len(geodata) > 0:
        print ('Found a valid address: {formatted_address}'.format(**geodata))
        print('Matched street = {street}, Matched city = {city}, Matched zip code = {zip_code}, '
              'Matched state = {state}, Matched country = {country}, '
              '(lat, lng) = ({lat}, {lng})'.format(**geodata))
    else:
        print ('Unknown address')