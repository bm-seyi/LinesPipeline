from os import environ, listdir, path
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import re
from sqlalchemy import create_engine, Engine, text
from datetime import datetime as dt
from time import time
import traceback
from uuid import uuid4, UUID, uuid5

load_dotenv()

connString: str | None = environ.get("connString")


int_pattern = re.compile(r'^\d+(\.\d+)?$')
decimal_pattern = re.compile(r"^[-+]?\d*\.\d+$")

uuidNamespace: UUID = UUID("7d01914f6ebad7cdb36db86c1226e4a7") # devskim: ignore DS173237 

replace_dict: dict = {pd.NaT: None, np.nan: None, pd.NA: None}

def db_connection_alchemy() -> Engine:
   """Returns a SQLALCHEMY engine"""
   engine: Engine = create_engine(connString)
   return engine

def merging(df: pd.DataFrame, remove: bool = False) -> pd.DataFrame:
    if not df.empty:
        if remove:
            new_records: pd.DataFrame = df[df["_merge"] == "left_only"].drop_duplicates(ignore_index=True)
            new_records.drop([col for col in new_records.columns if "_Greenwood" not in col and col != 'registrationNumber'] + ["_merge"], axis=1, inplace=True)
            new_records.columns = [col.replace("_Greenwood", "") for col in new_records.columns]
        else:
            new_records: pd.DataFrame = df[df["_merge"] == "right_only"].drop_duplicates(ignore_index=True)
            new_records.drop([col for col in new_records.columns if "_Greenwood" in col] + ["_merge"], axis=1, inplace=True)

        new_records.replace(replace_dict, inplace=True)
        new_records.reset_index(drop=True, inplace=True)
        return new_records
    else:
        return df

def action_log(source: str, error_message:str | None, Start: float, ETL: str, status: str, ID: str):
        log: dict = {
                "CreatedOn" : [dt.now().strftime("%Y-%m-%d %H:%M:%S")], 
                "Source" : [source], 
                "Error_Message" : [error_message], 
                "Duration" : [round(time() - Start, 2)], 
                "ETL" : [ETL],
                "Status": status,
                "Group_ID": ID
               }
        action_log: pd.DataFrame = pd.DataFrame.from_dict(log)

        SQL_Query: str = f""" INSERT INTO  [dbo].[Action_Log] ({",".join([f"[{col}]" for col in action_log.columns])}) VALUES ({", ".join([f":{col}" for col in action_log.columns])})""" 
        execute(SQL_Query, action_log, "Action Log")

def execute(query: str, df: pd.DataFrame, database: str, printID: bool = False):
    engine: Engine = db_connection_alchemy()
    try:
        id = df.columns[0]
        with engine.connect() as connection:
            if printID:
                for index, row in df.iterrows():
                    connection.execute(text(query), row.to_dict())
                    print(f"ID: {row[id]} --- INSERTED")
                    print(f"Row: {index + 1} of {df.shape[0]} --- {database}")
                connection.commit()
            else:
                for index, row in df.iterrows():
                    connection.execute(text(query), row.to_dict())
                    print(f"Row: {index + 1} of {df.shape[0]} --- {database}")
                connection.commit()
    except Exception:
        raise
    finally:
        engine.dispose()

def process_column(column: pd.Series):
    if (column.isna() | column.apply(lambda x: re.match(decimal_pattern, str(x)) is not None)).all():
        return column.astype("Float64")
    
    if (column.isna() | column.apply(lambda x: re.match(int_pattern, str(x)) is not None)).all():
        return column.astype("Int64")

    return column.astype("string")
