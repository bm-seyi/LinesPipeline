from ..functions import *

def main(insert_df: pd.DataFrame, update_df: pd.DataFrame, LogID: str, LineCode: str) -> None:
    try:
        start: float = time()
        print(f"--- LOAD ({LineCode}) ---")

        if insert_df.empty:
            print("NO RECORDS TO INSERT")
        else:
            query: str = f"INSERT INTO [dbo].[Lines] ({",".join([f"[{col}]" for col in insert_df.columns])}) VALUES ({", ".join(f":{col}" for col in insert_df.columns)})"
            execute(query, insert_df, "[dbo].[Lines]", True)
        
        if update_df.empty:
            print("NO RECORDS TO UPDATE")
            
        else:
            columns: list[str] = [f"[{col}] = :{col}" for col in update_df if col != "ID"]
            query = text(f"UPDATE [dbo].[Lines] SET {", ".join(columns)} WHERE [ID] = :{"ID"}")
            engine: Engine = db_connection_alchemy()
            try:
                with engine.connect() as conn:
                    for index, row in update_df.iterrows():
                        conn.execute(query, row.to_dict())
                        print(f"{"ID"}: {row["ID"]} --- UPDATED")
                        print(f"Row: {index + 1} of {update_df.shape[0]} --- [dbo].[Lines]")
                    conn.commit()
            finally:
                engine.dispose()

        action_log("[dbo].[Lines]", None, start, "Load", "Success", LogID)

    except:
        action_log("[dbo].[Lines]", traceback.format_exc(), start, "Load", "Fail", LogID)
        exit()