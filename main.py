# from timeit import default_timer as timer

from html_page_gen import generate_html_page
from companies_to_pickle import init_companies

if __name__ == '__main__':
    # start = timer()

    init_companies()        # creates pickle file with list of companies
    generate_html_page()    # generates html page from pickle file

    # end = timer()
    # print(end - start)
