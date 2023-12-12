import pandas as pd
import os
from scrapping.scrapping import scrape_data, extract_ocorrencias, replace_portuguese_months, extract_and_convert_date, get_tables, create_df_type

def pipeline(url):
    tables, doc = scrape_data(url)
    ocorr = extract_ocorrencias(doc)
    ocorrencia_time = pd.DataFrame(ocorr, columns=['ocorrencias'])
    replace_portuguese_months(ocorrencia_time, "ocorrencias")
    extract_and_convert_date(ocorrencia_time, 'ocorrencias' )
    df_tabular = pd.concat([pd.concat([create_df_type(get_tables('capital','raw',tables),'capital'),ocorrencia_time['date']],axis=1),
                        pd.concat([create_df_type(get_tables('demacro','raw',tables),'demacro'),ocorrencia_time['date']],axis=1),
                        pd.concat([create_df_type(get_tables('interior','raw',tables),'interior'),ocorrencia_time['date']],axis=1)],
                       axis=0)
    df_tabular = df_tabular.sort_values('date').reset_index(drop=True)
    df_tabular['feminicídio'].fillna(0, inplace=True)
    df_tabular.to_csv('df_tabular.csv')

    data_folder_path = os.path.join(os.pardir, 'data')
    if not os.path.exists(data_folder_path):
    # Create the "data" folder if it doesn't exist
        os.makedirs(data_folder_path)
    
    csv_file_path = os.path.join(data_folder_path, 'df_tabular.csv')

    # Save the DataFrame to a CSV file
    df_tabular.to_csv(csv_file_path, index=False)

    






