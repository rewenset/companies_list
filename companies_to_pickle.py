from urllib.request import urlopen, Request

import re

from file_utils import save_with_pickle
from company_parser import CompanyParser


def companies_generator():
    """ Iterates through the list and returns dict with company site on 'dou.ua' and company name
    """
    url = 'https://jobs.dou.ua/ratings/'

    req = Request(url)
    resp = urlopen(req)
    resp_data = resp.read()

    text = str(resp_data)
    pattern = r'<td class="company-name">\\n[\\(?=t)]*<a href="(?P<dou_url>.*?)">(?P<company_name>.*?)</a>\\n[\\(?=t)]+</td>'

    for match in re.finditer(pattern, text):
        yield {'dou_url': match.group('dou_url'), 'name': match.group('company_name')}


def init_companies():
    """ Main function
    """
    companies = []
    company_parser = CompanyParser()
    companies_gen = companies_generator()

    for counter, company in enumerate(companies_gen):
        new_company = company_parser.get_new_company(company)
        companies.append(new_company)

        print(counter)
        # if counter == 10:
        #      break

    print('Number of companies: {}'.format(len(companies)))

    save_with_pickle(companies)
