from src.Extraction import extract
from src.Transformation import transform
from src.Loading import load
from src.functions import *
import atexit

def main():
    LogID: str = str(uuid4())
    engine: Engine = create_engine(connString, pool_size=10, max_overflow=5, pool_timeout=30, pool_recycle=1800)
    atexit.register(lambda: engine.dispose())

    files = [file for file in listdir("data") if path.isfile(path.join("data", file))]

    for file in files:
        lineCode: str = file[:3]
        extraction: list = extract.main(LogID, file, engine)
        insert, update = transform.main(extraction, lineCode, engine, LogID)

        if insert.empty and update.empty:
            sleep(10)
            continue
            
        load.main(insert, update, LogID, lineCode, engine)
        sleep(10)

if __name__ == "__main__":
    main()