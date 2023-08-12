from utils.constants import EDGAR_IX_URL
from utils.requests_client import RequestsClient
from utils.utils import submissions_url, sanitize_CIK, str2dict
import pandas as pd

EDGAR_INDEX = 'https://www.sec.gov/Archives/edgar/full-index/{year}/{quarter}/master.idx'

def request_submissions(cik):
    try:
        url = submissions_url(sanitize_CIK(cik))
        c = RequestsClient()
        c.request(url)
        return str2dict(c.content)
    except:
        return float('nan') 

def get_ciks(n=10):
    client = RequestsClient()
    idx_url = EDGAR_IX_URL.format(year=2023, quarter='QTR2')
    client.request(idx_url)
    lines = client.content.split('\n')
    lines = [i for i in lines if '8-K' in i]
    ciks = [i.split('|')[0] for i in lines]
    ciks = list(set(ciks))[:n]
    return ciks

if __name__ == "__main__":
    df = pd.DataFrame(get_ciks(10), columns=['cik'])
    print(f'Companies found: {df.shape[0]}')
    df['r'] = df.cik.apply(lambda cik: request_submissions(cik))
    df['sic'] = df.r.apply(lambda r: r.get('sic'))
    df['sicDescription'] = df.r.apply(lambda r: r.get('sicDescription'))
    df['stateOfIncorporation'] = df.r.apply(lambda r: r.get('stateOfIncorporation', float('nan')))
    df['ticker'] = df.r.apply(lambda r: r.get('tickers')[0] if len(r.get('tickers'))>0 else float('nan'))
    df['exchange'] = df.r.apply(lambda r: r.get('exchanges')[0] if len(r.get('exchanges'))>0 else float('nan'))
    df['name'] = df.r.apply(lambda r: r.get('name', float('nan')))
    df['entityType'] = df.r.apply(lambda r: r.get('entityType', float('nan')))
    df.drop('r', axis=1, inplace=True)
    df.to_csv('./data/companies.csv', index=False)
