from os import environ, listdir, path
from dotenv import load_dotenv
import polars as pl
import re
from datetime import datetime as dt
from time import time, sleep
import traceback
import sys
import pyodbc as py
import traceback

py.pooling = True
load_dotenv()

data: list[dict] = []

CONNECTION_STRING: str | None = environ.get("CONNECTION_STRING")
