from ..functions import *

def main(insert_df: pd.DataFrame, update_df: pd.DataFrame, LogID: str, LineCode: str, engine: Engine) -> None:
    start: float = time()
    print(f"--- LOAD ({LineCode}) ---")
    try:
        with engine.connect() as conn:
            if insert_df.empty:
                print("NO RECORDS TO INSERT")
            else:
                query: str = f"INSERT INTO [dbo].[Lines] ({",".join([f"[{col}]" for col in insert_df.columns])}) VALUES ({", ".join(f":{col}" for col in insert_df.columns)})"
                execute(query, insert_df, "[dbo].[Lines]",conn,True)
            

            if update_df.empty:
                print("NO RECORDS TO UPDATE")
            else:
                columns: list[str] = [f"[{col}] = :{col}" for col in update_df if col != "Id"]
                query = text(f"UPDATE [dbo].[Lines] SET {", ".join(columns)} WHERE [Id] = :{"Id"}")
                for index, row in update_df.iterrows():
                    conn.execute(query, row.to_dict())
                    print(f"{"Id"}: {row["Id"]} --- UPDATED")
                    print(f"Row: {index + 1} of {update_df.shape[0]} --- [dbo].[Lines]")
               

            action_log(None, start, "Load", "Success", LogID, conn)
            conn.commit()

    except:
        with engine.connect() as conn:
            action_log(traceback.format_exc(), start, "Load", "Fail", LogID, conn)
            conn.commit()
        sys.exit(1)