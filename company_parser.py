from urllib.request import Request, build_opener, HTTPCookieProcessor
from http.cookiejar import CookieJar
import re


class CompanyParser:
    """ There are only two hard things in Computer Science...
    """

    def __init__(self):
        self.cj = CookieJar()
        self.opener = build_opener(HTTPCookieProcessor(self.cj))
        self.first_time = True
        self.regex = re.compile(r'<div class="offices">[\\(?=n|t)]*(.*?\)?)[\\(?=n|t)]*</div>.*?'
                                r'<div class="site">[\\(?=n|t)]*<a href="(.*?)" target')

    def get_str_resp(self, some_url):
        """ Return string response from given url.
            For first time, also specify english language in cookie.
        """
        request = Request(some_url)
        if self.first_time:
            response = self.opener.open(request)
            # Add my own cookie
            response.headers.add_header('Set-Cookie', 'lang=en; path=/; domain=.dou.ua; HttpOnly')
            self.cj.extract_cookies(response, request)
            self.first_time = False

        response = self.opener.open(request)
        return str(response.read())

    def match_info(self, data):
        """ Search for offices and website url
            in input string with regex
        """
        offices = None
        site = None

        company_info = self.regex.findall(data)

        if company_info:
            offices, site = company_info[0]
        else:
            print("No info: {}".format(data))

        return offices, site

    def get_new_company(self, company):
        """ Creates dict for new company and tries to find out
            location of offices and company website url
        """
        new_company = {
            'name': company['name'],
            'offices': 'not specified',
            'site': company['dou_url']
        }

        response_data = self.get_str_resp(company['dou_url'])
        offices, site = self.match_info(response_data)

        if offices:
            new_company['offices'] = offices
        if site:
            new_company['site'] = site

        return new_company
