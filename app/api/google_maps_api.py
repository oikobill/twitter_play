from app.keys import google_maps_api_key
import requests

def get_geocoordinates(location):
    """
    Using the Google Geocoding API to get where the users are from.
    Given the location in the form of a string, returns (Lat, Lon)
    """ 
    if location is not None:
        try:
            request = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+location+"&key="+google_maps_api_key)
            json_coordinates = request.json()['results'][0]['geometry']['location']
        except (IndexError, requests.exceptions.SSLError) as e:
            print("Index Error occured during geolocation API call")
            return None, None
    else:
        return None, None

    lat = json_coordinates['lat']
    lon = json_coordinates['lng']
    
    return (lat, lon)