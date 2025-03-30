from ..functions import *

def main(data: list, LineCode: str, engine: Engine, LogID: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    start: float = time()  
    print(f"--- TRANSFORM ({LineCode}) ---")
    try: 
        df: pd.DataFrame = pd.DataFrame(data)
        df: pd.DataFrame = df[df["type"] == "node"]
        df["LineCode"] = LineCode

        df.drop(["type", "nodes", "tags"], axis=1, inplace=True)

        with engine.connect() as conn:
            tms: pd.DataFrame = pd.read_sql_query(f"SELECT * FROM [dbo].[Lines] WHERE [LineCode] = '{LineCode}'", conn)

            df.columns = tms.columns[1:-1]

            for col in df.columns:
                df[col] = process_column(df[col])

            df["Id"] = [
                str(uuid5(uuidNamespace, f"{row.latitude}{row.longitude}{row.LineCode}")).upper() 
                for row in df.itertuples(index=False)
            ]
            df["LogId"] = LogID

            update_merge_df: pd.DataFrame = pd.merge(tms, df, on=df.columns[:-1].to_list(), how="outer", indicator=True, suffixes=("_Greenwood", ""))
            update_df: pd.DataFrame = update_merge_df[update_merge_df["Id"].isin(tms["Id"].unique())]

            merged_df: pd.DataFrame = pd.merge(tms, df, how="outer", on="Id",  indicator=True, suffixes=("_Greenwood", ""))

            update_records: pd.DataFrame = merging(update_df)
            insert_records: pd.DataFrame = merging(merged_df)

            action_log(None, start, "Transform", "Success", LogID, conn)
            conn.commit()

        return insert_records, update_records
    
    except:
        with engine.connect() as conn:
            action_log(traceback.format_exc(), start, "Transform", "Fail", LogID, conn)
            conn.commit()
        sys.exit(1)