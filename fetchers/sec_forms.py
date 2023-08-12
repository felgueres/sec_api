import logging as pylogging
import json
import os
import pandas as pd
from utils.requests_client import RequestsClient
from utils.form_client import FormClient
from utils.utils import sanitize_CIK

pylogging.basicConfig()

def get_request_content(url):
    client = RequestsClient()
    client.request(url)
    return json.loads(client.content)

def get_company_submissions_url(CIK):
    return f'https://data.sec.gov/submissions/CIK{CIK}.json'

def parse_10K_submissions(CIK):
    sanitized_CIK = sanitize_CIK(CIK)
    subs_url = get_company_submissions_url(sanitized_CIK)
    print(subs_url)
    try:
        submissions = get_request_content(subs_url)
        recent = submissions['filings']['recent']
        form_10K_idxs = [idx for idx, form in enumerate(recent['form']) if form == '10-K']
        for k in recent.keys():
            recent[k]=[e for idx, e in enumerate(recent[k]) if idx in form_10K_idxs]
        return submissions
    except Exception as e:
        print(f'msg: {e}')

def get_latest_10K_url(cik):
    subs=parse_10K_submissions(cik)
    print(subs)
    accession=subs['filings']['recent']['accessionNumber'][0] #Ordered list, first item is latest.
    accession=accession.replace('-','')
    primaryDoc=subs['filings']['recent']['primaryDocument'][0]
    f_url=f'https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{primaryDoc}'
    return f_url

def get_form_text(url):
    f=FormClient(url)
    f.fetch_text_from_url()
    t = f.get_text() 
    return t

if __name__ == '__main__':
    path_shortlist = './data/shortlist.csv'
    df = pd.read_csv(path_shortlist)
    [print(x) for x in df.f_url.tolist()]
    print(df.cik.tolist())
