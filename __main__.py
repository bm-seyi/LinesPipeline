from src.Extraction import extract
from src.Transformation import transform
from src.Loading import load
from time import sleep
from os import listdir, path, environ
import polars as pl
import traceback
import sys
from dotenv import load_dotenv
import mssql_python as ms


load_dotenv()


def main():
    try:
        files = [file for file in listdir("data") if path.isfile(path.join("data", file))]
        print("---EXTRACT---")
        for file in files:
            lineCode: str = file[:3]
            extract.main(file, lineCode)
            sleep(25)

        df: pl.DataFrame = transform.main()
        load.main(df)

    except:
        error: str = traceback.format_exc()
        print(error)

        sys.exit(1)

if __name__ == "__main__":
    main()
