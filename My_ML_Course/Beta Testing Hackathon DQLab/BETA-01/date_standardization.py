import pandas as pd

def normalize_tanggal_transaksi(input_xlsx_path: str, output_xlsx_path: str) -> None:
    
    month_mapping = {
        'januari': 'January', 'februari': 'February', 'maret': 'March', 'april': 'April',
        'mei': 'May', 'juni': 'June', 'juli': 'July', 'agustus': 'August',
        'september': 'September', 'oktober': 'October', 'november': 'November', 'desember': 'December',
        'jan': 'Jan', 'feb': 'Feb', 'mar': 'Mar', 'apr': 'Apr', 
        'jun': 'Jun', 'jul': 'Jul', 'aug': 'Aug', 'sep': 'Sep', 
        'okt': 'Oct', 'nov': 'Nov', 'des': 'Dec'
    }
    
    dataset = pd.read_excel(input_xlsx_path, engine='openpyxl')
    
    dataset['Tanggal Transaksi'] = dataset['Tanggal Transaksi'].astype(str).str.strip()
    
    dataset['Tanggal Transaksi'] = dataset['Tanggal Transaksi'].str.replace("'", "20", regex=False)
    
    mask_comma = dataset['Tanggal Transaksi'].str.contains(',', na=False)
    if mask_comma.any():
        temp = dataset.loc[mask_comma, 'Tanggal Transaksi'].str.replace(',', '', regex=False).str.split(expand=True)
        if temp.shape[1] == 3:
            dataset.loc[mask_comma, 'Tanggal Transaksi'] = temp[1] + ' ' + temp[2] + ' ' + temp[0]
    
    for indo_month, eng_month in month_mapping.items():
        dataset['Tanggal Transaksi'] = dataset['Tanggal Transaksi'].str.replace(
            indo_month, eng_month, case=False, regex=False
        )
    
    dataset['Tanggal Transaksi'] = pd.to_datetime(
        dataset['Tanggal Transaksi'], 
        format='mixed', 
        dayfirst=True
    )
    
    dataset['Tanggal Transaksi'] = dataset['Tanggal Transaksi'].dt.strftime('%d-%m-%Y')
    
    dataset.to_excel(output_xlsx_path, index=False, engine='openpyxl')
    return dataset

print(normalize_tanggal_transaksi(
        'data/penjualan_dqmart_01-beta.xlsx',
        'data/penjualan_dqmart_01-normalized.xlsx'
    ))