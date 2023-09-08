from os.path import isfile

from Logger import LOGGER
from pandas import DataFrame, read_csv


def write_row(row: dict, chat_id: int) -> None:
    df = DataFrame.from_dict(row, orient="columns")
    database = f"../data/database/{chat_id}_database.csv"

    if not isfile(database):
        with open(database, "w") as f:
            f.write("chat_id,message_id,message_text,reply_text\n")

    df.to_csv(database, mode="a", index=False, header=False)
    LOGGER.info(f"Wrote row to database: {row}")


def retrieve_recent_chat_history(chat_id: int) -> list[tuple[str]] | None:
    database = f"../data/database/{chat_id}_database.csv"

    if isfile(database):
        df = read_csv(database)
        chat_history_df = df.tail(1)

        if len(chat_history_df):
            return [
                (row["message_text"], row["reply_text"])
                for _, row in chat_history_df.iterrows()
            ]
        else:
            return None
    else:
        return None
