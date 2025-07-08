from ..functions import *


def main(df: pd.DataFrame, engine: Engine):
    start = time()
    print("--- LOAD ---")
    try:
            if df.empty:
                print("NO RECORDS TO INSERT/UPDATE")
            else:
                batch_size = 50000
                total_records = len(df)
                processed_records = 0

                while processed_records < total_records:
                    with engine.connect() as conn:
                        batch = df.iloc[processed_records:processed_records + batch_size]
                        
                        print(f"#temp: LOADING BATCH {processed_records + 1} to {min(processed_records + batch_size, total_records)}")
                        
                        # Load the batch into the temp table
                        batch.to_sql("#temp", conn, index=False)
                        
                        print("#temp: LOADED")
                        
                        print("EXECUTING PROCEDURE: pro_lines")
                        conn.execute(text("EXEC pro_lines"))
                        print("EXECUTED PROCEDURE: pro_lines")

                        print("DROPPING #temp")
                        conn.execute(text("DROP TABLE #temp"))
                        print("DROPPED #temp")

                        conn.commit()
                        conn.close()

                        processed_records += len(batch)
                        print(f"Processed {processed_records} of {total_records} records")

    
            with engine.connect() as conn:
                actionLog(None, start, "Load", "Success", conn)
                conn.commit()

    except:
        error: str = traceback.format_exc()
        print(error)
        with engine.connect() as conn:
            actionLog(error, start, "Load", "Fail", conn)
            conn.commit()
        sys.exit(1)