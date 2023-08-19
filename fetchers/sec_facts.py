import sys
sys.path.append('./')
import json
import itertools
from utils.requests_client import RequestsClient
from utils.utils import sanitize_CIK

def get_request_content(url):
    client = RequestsClient()
    client.request(url)
    return json.loads(client.content)

def get_company_facts_url(CIK):
    return f'https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK}.json'

def get_facts_data(f,concept,cik,frames):
    '''f: list of facts for a given financial concept
    concept: str, eg. marketCap, CostOfRevenue
    '''
    _data = {}
    out = []

    for row in f:
        if row.get('frame') is not None:
            _data[row.get('frame')] = {'cik': cik, 'concept': concept, 'form': row['form'], 'val': row['val'], 'fp': row['fp'],'fy': row['fy'], 'frame': row['frame'], 'filed': row['filed']}
        else:
            continue 
    
    for frame in frames:
        if frame in _data and _data[frame].get('fp', '').startswith('Q'):
            out.append(_data[frame]) 
        else:
            empty_frame = {'cik': cik, 'concept': concept, 'form': '', 'val': 0, 'fp': '', 'fy': '', 'frame': frame, 'filed': ''}
            out.append(empty_frame)
    return out 

def quarterly_ranges(start, end):
    out=[]
    for i in range(start,end+1):
        for q in range(1,5):
            out.append(f'CY{i}Q{q}')
    return out

def get_company_facts(cik, start_date=2021, end_date=2022):
    frames = quarterly_ranges(start_date, end_date)

    data = []
    url_cik= sanitize_CIK(cik)
    url = get_company_facts_url(url_cik)

    content = get_request_content(url)

    facts = content['facts']
    us_gaap = facts['us-gaap']
    
    revenues = us_gaap['Revenues']['units']['USD'] if us_gaap.get('Revenues',False) else []
    contractRevenues = us_gaap['RevenueFromContractWithCustomerExcludingAssessedTax']['units']['USD'] if us_gaap.get('RevenueFromContractWithCustomerExcludingAssessedTax',False) else []
    contractRevenueswTax = us_gaap['RevenueFromContractWithCustomerIncludingAssessedTax']['units']['USD'] if us_gaap.get('RevenueFromContractWithCustomerIncludingAssessedTax',False) else []
    revenues.extend(contractRevenues)
    revenues.extend(contractRevenueswTax)

    costofrevenue = us_gaap['CostOfRevenue']['units']['USD'] if us_gaap.get('CostOfRevenue',False) else []
    # costAndExpenses = us_gaap['CostsAndExpenses']['units']['USD'] if us_gaap.get('CostsAndExpenses',False) else []
    # costofrevenue.extend(costAndExpenses)
    grossprofit = us_gaap['GrossProfit']['units']['USD'] if us_gaap.get('GrossProfit',False) else [] 
    concepts = [(revenues, 'Revenues'),
                (costofrevenue, 'CostOfRevenue'),
                (grossprofit, 'GrossProfit')]

    concepts = [(facts,concept) for (facts,concept) in concepts if facts]

    for (facts,concept) in concepts:
        d = get_facts_data(facts,concept, cik, frames) 
        data.append(d)
    
    data = list(itertools.chain(*data)) # flatten list
    return data 

if __name__ == '__main__':
    data = get_company_facts('40533')