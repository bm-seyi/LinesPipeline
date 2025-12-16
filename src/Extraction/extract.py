import requests
import urllib.parse
from .. import functions

def main(path: str, lineCode: str):
    print(f"Retrieving Data from Open Street Maps for: {lineCode}")
    with open(f"data/{path}") as fd:
        osm_query: str = fd.read()

    response = requests.get(f"https://overpass-api.de/api/interpreter?data={urllib.parse.quote(osm_query)}", timeout=60)
    
    if response.status_code != 200:
        response.raise_for_status()
    
    responseJson: dict = response.json()
    elements: list[dict] = responseJson.get('elements', [])
    
    functions.data.extend([ {**item, "LineCode": lineCode} for item in elements ])    
  