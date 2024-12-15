from ..functions import *

def main(data: list, LineCode: str, LogID: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    try:
        start: float = time()
        print(f"--- TRANSFORM ({LineCode}) ---")
        df: pd.DataFrame = pd.DataFrame(data)
        
        df: pd.DataFrame = df[df["type"] == "node"]
        df["LineCode"] = LineCode

        df.drop(["type", "nodes", "tags"], axis=1, inplace=True)

        engine: Engine = db_connection_alchemy()
        try:
            with engine.connect() as conn:
                tms: pd.DataFrame = pd.read_sql_query(f"SELECT * FROM [dbo].[Lines] WHERE [LineCode] = '{LineCode}'", conn)
        finally:
            engine.dispose()
        
        df.columns = tms.columns[1:-1]

        for col in df.columns:
            df[col] = process_column(df[col])

        df["ID"] = [
            str(uuid5(uuidNamespace, f"{row.latitude}{row.longitude}{row.LineCode}")).upper() 
            for row in df.itertuples(index=False)
        ]
        df["LogID"] = LogID

        update_merge_df: pd.DataFrame = pd.merge(tms, df, on=df.columns[:-1].to_list(), how="outer", indicator=True, suffixes=("_Greenwood", ""))
        update_df: pd.DataFrame = update_merge_df[update_merge_df["ID"].isin(tms["ID"].unique())]

        merged_df: pd.DataFrame = pd.merge(tms, df, how="outer", on="ID",  indicator=True, suffixes=("_Greenwood", ""))

        update_records: pd.DataFrame = merging(update_df)
        insert_records: pd.DataFrame = merging(merged_df)

        action_log("[dbo].[Lines]", None, start, "Transform", "Success", LogID)
        return insert_records, update_records
    
    except:
        action_log("[dbo].[Lines]", traceback.format_exc(), start, "Transform", "Fail", LogID)
        exit()