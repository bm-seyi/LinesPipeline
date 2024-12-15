from src.Extraction import extract
from src.Transformation import transform
from src.Loading import load
from src.functions import *

def main():
    start: float = time()
    LogID: str = str(uuid4())
    try:
        files = [file for file in listdir("data") if path.isfile(path.join("data", file))]

        for file in files:
            lineCode: str = file[:3]
            extraction: list = extract.main(LogID, file)
            insert, update = transform.main(extraction, lineCode, LogID)

            if insert.empty and update.empty:
                continue
                
            load.main(insert, update, LogID, lineCode)
        

    except:
        action_log("[dbo].[Lines]", traceback.format_exc(), start, "Script", "Fail", LogID)
        exit()

if __name__ == "__main__":
    main()