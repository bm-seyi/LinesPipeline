import requests
import urllib.parse
from ..functions import action_log, traceback, time

def main(LogID: str, path: str) -> list:
    start: float = time()
    print(f"--- EXTRACT ({path[:3]})---")
    try:
        with open(f"data/{path}") as fd:
            osm_query: str = fd.read()

        with requests.Session() as session:
            response = session.get(f"https://overpass-api.de/api/interpreter?data={urllib.parse.quote(osm_query)}")
        
        if response.status_code != 200:
            raise Exception(f"Error Ocurred: {response.status_code}, {response.content}")
        
        data: dict = response.json() 
        elements: list = data.get('elements', [])

        action_log("[dbo].[Lines]", None, start, "Extract", "Success", LogID)
        return elements
    
    except:
        action_log("[dbo].[Lines]", traceback.format_exc(), start, "Extract", "Fail", LogID)
        exit()
