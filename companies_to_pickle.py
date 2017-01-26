from requests import Session
from lxml import html
from functools import partial

from file_utils import save_with_pickle

session = Session()
session.headers.update({
                         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) '
                                       'Chrome/23.0.1271.64 Safari/537.11 '
                     })
my_request = partial(session.get, params="switch_lang=en")


def get_elements_tree(url):
    page = my_request(url)
    tree = html.fromstring(page.content)
    return tree


def get_new_company(company):
    """ Creates dict for new company and tries to find out
        location of offices and company website url
    """

    tree = get_elements_tree(company['dou_url'])

    offices = tree.xpath("//div[@class='offices']/text()") or ['']
    site = tree.xpath("//div[@class='site']/a/@href") or ['']

    new_company = {
        'name': company['name'],
        'offices': offices[0].strip() or 'not specified',
        'site': site[0] or company['dou_url']
    }

    return new_company


def companies_generator():
    """ Iterates through the list and returns dict with company site on 'dou.ua' and company name
    """
    url = 'https://jobs.dou.ua/ratings/'
    tree = get_elements_tree(url)
    elements = tree.xpath("//td[@class='company-name']/a")

    for element in elements:
        yield get_new_company({'dou_url': element.xpath("@href")[0],
                               'name': element.xpath("text()")[0]})


def init_companies():
    """ Main function
    """
    companies = []
    companies_gen = companies_generator()

    for counter, company in enumerate(companies_gen):
        companies.append(company)

        print(counter)
        # if counter == 10:
        #     break

    print('Number of companies: {}'.format(len(companies)))

    save_with_pickle(companies)
