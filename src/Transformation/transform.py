from ..functions import *

def main(data: list, LineCode: str, engine: Engine) -> pd.DataFrame:
    start: float = time()  
    print(f"--- TRANSFORM ({LineCode}) ---")
    try: 
        df: pd.DataFrame = pd.DataFrame(data)
        df: pd.DataFrame = df[df["type"] == "node"]
        df["LineCode"] = LineCode

        df.drop(["type", "nodes", "tags"], axis=1, inplace=True)

        for col in df.columns:
            df[col] = process_column(df[col])
        
        with engine.connect() as conn:
            actionLog(None, start, "Transform", "Success", conn)
            conn.commit()

        return df
    
    except:
        error: str = traceback.format_exc()
        print(error)
        with engine.connect() as conn:
            actionLog(error, start, "Transform", "Fail", conn)
            conn.commit()
        sys.exit(1)    