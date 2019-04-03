# address-validation
Address Validation Tool using Google Maps API

This package contains python scripts that allow performing address validation process (using the Google Maps Geocoding service). Address validation is a process of checking a mailing address against an authoritative database to see if the address is valid. In the proposed method, a single address that is sent for validation passes through a process called geocoding, after which the input components are compared against the geocoding result.

### Geocoding
Geocoding is a method used to assign geographic coordinates to an individual based on their address. The process converts a human-readable address (e.g. "1600 Amphitheatre Parkway, Mountain View, CA, US") into geographic coordinates (e.g. latitude 37.423021 and longitude -122.083739).

### Google Maps Geocoding API
The proposed method uses the Google Maps Geocoding API to perform the geocoding. In case the requested address was successfully parsed and at least one address is found, the service returns a geocode result with applicable address components (e.g. street name, city, postal code, ext.).

## The methodology
The proposed method takes the user input and performing a geocoding by calling the Google Maps Geocoding service. In the case at least one address is returned, it iterates over the result and extracts the returned street name, city, zip code, state, and country. Then, it compares each address component with the user's input and displays the matching result.

The user enters a single address for validation:
```js
Street Address: 
City:
State/Province:
Zip Code:
Country:
```
In case a valid address is found, the output will look like this:
```js
Found a valid address.
Matched street = True, Matched city = True, Matched zip code = True, Matched state = True, Matched country = True, (lat, lng) = (x, y)
```
In case not valid address is found, the output will look like this:
```
Unknown address
```

### Libraries
#####   re — Regular expression operations
#####   unicodedata — Unicode database
#####   requests — Apache2 licensed HTTP
#####   urlsigner — Secured URLs creation

### Package
#### [address-validation-tool.py](https://github.com/lironmarcus/address-validation/blob/master/address-validation-tool.py) - The main module, includes the function that calls the Google Maps Geocoding API.
#### [urlsigner.py](https://github.com/lironmarcus/address-validation/blob/master/urlsigner.py) - The module that signs a request URL with a URL signing secret.

### References:
#### * http://docs.python-requests.org/en/latest/
#### * https://developers.google.com/maps/
