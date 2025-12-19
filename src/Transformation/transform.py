from .. import functions
import polars as pl

def main() -> pl.DataFrame:
    print("---TRANSFORM---")
    
    lf = (
        pl.LazyFrame(functions.data)
        .filter(pl.col("type") == "node")
        .drop(["type", "tags"])
        .cast({"id": pl.Utf8})
        .unique(subset=["id"])
    )

    df = lf.collect()

    return  df
