import requests
import pandas as pd
from io import StringIO


def data_fetcher(url: str) -> pd.DataFrame:
    response = requests.get(url)
    if response.status_code == 200:
        text = response.content.decode("utf-8")

        return pd.read_csv(
            StringIO(text),
            encoding="utf-8",
            engine="python",
        )
    else:
        print(f"Ошибка при получении данных: {response.status_code}")
        return pd.DataFrame()
