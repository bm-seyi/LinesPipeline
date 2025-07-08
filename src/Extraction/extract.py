import requests
import urllib.parse
from ..functions import *

def main(path: str, engine: Engine) -> list:
    start: float = time()
    print(f"--- EXTRACT ({path[:3]})---")
    try:
        with open(f"data/{path}") as fd:
            osm_query: str = fd.read()

        response = requests.get(f"https://overpass-api.de/api/interpreter?data={urllib.parse.quote(osm_query)}", timeout=60)
        
        if response.status_code != 200:
            raise Exception(f"Error Ocurred: {response.status_code}, {response.content}")
        
        data: dict = response.json() 
        elements: list = data.get('elements', [])

        with engine.connect() as conn:
            actionLog(None, start, "Extract", "Success", conn)
            conn.commit()
        return elements
    
    except:
        error: str = traceback.format_exc()
        print(error)
        with engine.connect() as conn:
            actionLog(error, start, "Extract", "Fail", conn)
            conn.commit()
        sys.exit(1)    
