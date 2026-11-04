import pandas as pd


def matches_to_process(path) -> pd.DataFrame:

    df_calendar_silver = pd.read_json(path, dtype={"date":str,"score_equipe_domicile":str,"score_equipe_exterieur":str,"is_loaded":bool})

    if not df_calendar_silver.empty:

        df_calendar_silver["date"] = pd.to_datetime(df_calendar_silver["date"], format="%Y-%m-%d")
        df_calendar_silver["date"] = df_calendar_silver["date"].dt.strftime("%d-%m-%Y")


    df = df_calendar_silver[(df_calendar_silver["is_loaded"]==False)] # noqa: E712

    return df

