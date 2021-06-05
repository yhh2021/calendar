import json
import webbrowser
import abbrs
import pandas as pd

def read_schedule(filename: str) -> (str, str):
    dat = pd.read_excel(filename)
    date_col_name = dat.columns[0]
    current_date = None

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

                if current_date == None:
                    current_date = date

    return ',\n'.join(events), current_date.replace("'", '')

def render(filename: str) -> None: 
    OUT = './calendar-20/out.html'
    events_str, current_date = read_schedule(filename)

    template = abbrs.read_file('calendar-20/template.html')
    template = template.replace('TODAY_STR', current_date).replace('EVENTS_STR', events_str)

    abbrs.write_file(OUT, template)
    webbrowser.open(OUT)

if __name__ == '__main__':
    FILE = './calendar.xls'
    print(f'Parsing f{FILE}.')
    render(FILE)
