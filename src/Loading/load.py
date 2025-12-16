from .. import functions
from polars import DataFrame
import pyodbc as py

def main(df: DataFrame):
    print("--- LOAD ---")
    query: str = f"INSERT INTO #temp ({",".join([f"[{col}]" for col in df.columns])}) VALUES ({", ".join(["?" for _ in df.columns])})"
    
    with py.connect(functions.CONNECTION_STRING) as conn:
        if not df.is_empty():
            try:
                with open("temp.sql", "r") as f:
                    conn.execute(f.read())
                
                cursor = conn.cursor()
                cursor.fast_executemany = True

                cursor.executemany(query, df.rows())

                conn.execute("EXEC usp_opm_lines")
           
            except Exception:
                conn.rollback()
                raise
        else:
            print("NO RECORDS TO INSERT/UPDATE")

        conn.commit()



  

