# imports
import pandas as pd
import requests
from selectolax import HTMLParser
import datetime

def scrape_data(url):
    response = requests.get(url)
    html = response.text
    doc = HTMLParser(html)
    tables = doc.css("table.table.table-striped.table-hover.table-condensed")
    return tables, doc

def extract_ocorrencias(doc):

    ocorrencias = []

    table_number = 2 
    while True:
        table_id = f"conteudo_repPeriodo_lblPeriodo_{table_number}"
        span_element = doc.css(f'#{table_id}')

        if not span_element:
            break

        ocorrencia = span_element[0].text()
        ocorrencias.append(ocorrencia)

        table_number += 1

    return ocorrencias

import datetime
import pandas as pd

def replace_portuguese_months(data_frame, column_name):
    month_mapping = {
        'Janeiro': 'January',
        'Fevereiro': 'February',
        'Março': 'March',
        'Abril': 'April',
        'Maio': 'May',
        'Junho': 'June',
        'Julho': 'July',
        'Agosto': 'August',
        'Setembro': 'September',
        'Outubro': 'October',
        'Novembro': 'November',
        'Dezembro': 'December'
    }

    for pt_month, en_month in month_mapping.items():
        data_frame[column_name] = data_frame[column_name].str.replace(pt_month, en_month)

def extract_and_convert_date(data_frame, column_name):
    data_frame['date'] = data_frame[column_name].apply(lambda x: datetime.datetime.strptime(x.split(': ')[-1], '%B de %Y'))

def get_tables(df:str,choose:str, tables):
    ind = {'capital':1,'demacro':2,'interior':3,'total':4}

    i = ind[df]
    df1 = []
    
    for table in tables[:67]:
        row_data = []
        rows = table.css('tr')[1:]
        for row in rows:
            cell = row.css("td")[i]
            row_data.append(cell.text().strip())
        row_data = np.array(row_data).T
        df1.append(row_data)
        
# Create a DataFrame from the extracted data
    df_df1 = pd.DataFrame(df1, columns = col1).astype('uint8')
    
    df2 = []
    
    for table in tables[67:]:
        row_data = []
        rows = table.css('tr')[1:]
        for row in rows:
            cell = row.css("td")[i]
            row_data.append(cell.text().strip())
        row_data = np.array(row_data).T
        df2.append(row_data)
        
# Create a DataFrame from the extracted data
    df_df2 = pd.DataFrame(df2, columns = col2).astype('uint8')
    
    df = pd.concat([df_df1[col2],df_df2],axis=0, ignore_index=True)
    dfraw = pd.concat([df_df1,df_df2],axis=0, ignore_index=True)
    typee = {'new':df1, 'old':df2,'total':df,'raw':dfraw}
    returned = typee[choose]
    return returned

def create_df_type(df:pd.DataFrame,name:str):
    df = df.assign(regiao=name)
    return df
