import sys


def decode_email(code_str):
    email = ''.join([chr(int(code_str[i:i + 2], 16) ^ int(code_str[:2], 16))
                     for i in range(2, len(code_str), 2)])
    return email


def scrape_infor_page_company(soup):
    # Initialize dictionaries to store company information
    company_infor = {}
    director_dict = {}

    tr_tags = soup.find_all('tr')
    # Iterate through each 'tr' tag
    for tr_tag in tr_tags:
        p_tags = tr_tag.find_all('p')

        if len(p_tags) == 2:
            company_infor[p_tags[0].text] = p_tags[1].text

        if len(p_tags) == 5:
            director_data = {
                'Director Name': p_tags[1].text,
                'Designation': p_tags[2].text,
                'Appointment Date': p_tags[3].text
            }
            director_dict[p_tags[0].text] = director_data

    company_infor['Directors'] = director_dict

    # Get the company email if available
    if soup.find('a', class_='_cf_email_'):
        company_infor['Email'] = decode_email(soup.find('a', class_='_cf_email_')['data-cfemail'])

    # Get the company address
    class_tags = soup.find_all('div', class_='col-lg-6 col-md-6 col-sm-12 col-xs-12')
    address = ''
    for class_tag in class_tags:
        t = class_tag.find_all('p')
        for t1 in t:
            address = t1.text

    # Add the company address to the company information dictionary
    company_infor['Address'] = address
    return company_infor


def filter_company(company_infor):
    company_infor = {key: value for key, value in company_infor.items() if "Login to view" not in value
                     or "N\A" not in value}
    del company_infor['Age of Company']
    del company_infor['Number of Employees']

    return company_infor
