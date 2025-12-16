from src.Extraction import extract
from src.Transformation import transform
from src.Loading import load
from src.functions import *
import polars as pl

def main():
    try:
        files = [file for file in listdir("data") if path.isfile(path.join("data", file))]
        print("---EXTRACT---")
        for file in files:
            lineCode: str = file[:3]
            extract.main(file, lineCode)
            sleep(5)

        df: pl.DataFrame = transform.main(lineCode)
        load.main(df, lineCode)
        sleep(10)

    except:
        error: str = traceback.format_exc()
        print(error)

        sys.exit(1)

if __name__ == "__main__":
    main()
