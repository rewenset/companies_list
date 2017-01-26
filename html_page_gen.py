from file_utils import load_with_pickle
import codecs

def generate_html_page():
    """ Generates html page 'companies.html' with list of companies
    """
    companies = load_with_pickle()

    with codecs.open('companies.html', 'w', 'utf-8') as file:

        with open("template.html") as template:
            for line in template:
                file.write(line)

        for counter, company in enumerate(companies):
            file.write('\n<a href="{}"><div class="company">'.format(company['site']))
            file.write('\n\t {}. {}: '.format(counter, company['name']))
            file.write('\n\t({})'.format(company['offices']))
            file.write('\n</div></a>\n')

        file.write('</body>\n')
        file.write('</html>')
