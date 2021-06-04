import json
import pandas as pd

def read_schedule(filename: str) -> str:
    dat = pd.read_excel(filename)
    date_col_name = dat.columns[0]

    events = [ ]

    for _, row in dat.iterrows():
        row = row.to_dict()
        date = row[date_col_name].strftime("'%Y-%m-%d'")
        del row[date_col_name]
        
        for key, val in row.items():
            if pd.notna(val):
                title = json.dumps(f'{key}：{val}', ensure_ascii=False)
                events.append(f'''{{
                    title: {title},
                    start: {date}
                }}''')

    return ',\n'.join(events)
