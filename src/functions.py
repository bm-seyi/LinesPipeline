from os import environ, listdir, path
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import re
from sqlalchemy import create_engine, Engine, text, Connection
from datetime import datetime as dt
from time import time, sleep
import traceback
import sys

load_dotenv()

connString: str | None = environ.get("connString")

int_pattern = re.compile(r'^\d+(\.\d+)?$')
decimal_pattern = re.compile(r"^[-+]?\d*\.\d+$")

def process_column(column: pd.Series) -> pd.Series:
    if (column.isna() | column.apply(lambda x: re.match(decimal_pattern, str(x)) is not None)).all():
        return column.astype("Float64")
    
    if (column.isna() | column.apply(lambda x: re.match(int_pattern, str(x)) is not None)).all():
        return column.astype("Int64")

    return column.astype("string")

def actionLog(error_message:str | None, Start: float, Content: str, status: str, conn: Connection):
    log: dict = {
        "CreatedOn" : [dt.now().strftime("%Y-%m-%d %H:%M:%S")], 
        "Project": "Lines",
        "Type": "Pipeline",
        "Error_Message" : [error_message], 
        "Duration" : [round(time() - Start, 2)], 
        "Content" : [Content],
        "Status": [status]
    }
    df: pd.DataFrame = pd.DataFrame.from_dict(log)

    query: str = f"INSERT INTO [dbo].[ActionLog] ({",".join([f"[{col}]" for col in df.columns])}) VALUES ({", ".join([f":{col}" for col in df.columns])})" 
    
    conn.execute(text(query), df.to_dict())
    print("[dbo].[ActionLog] --- INSERTED")
