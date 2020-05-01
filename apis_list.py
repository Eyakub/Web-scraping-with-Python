from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://www.programmableweb.com/category/all/apis"
# url = "https://www.programmableweb.com/category/tools/api"

apis_list = {}
list_no = 0

while True:
    response = requests.get(url)

    data = response.text

    soup = BeautifulSoup(data, 'html.parser')

    apis_odd = soup.find_all('tr', {'class': 'odd'})
    apis_even = soup.find_all('tr', {'class': 'even'})

    for api in apis_even:
        api_name = api.find(
            'td', attrs={'class': 'views-field-pw-version-title'}).find('a').text
        api_link = 'https://www.programmableweb.com' + \
            api.find('td', attrs={
                'class': 'views-field-pw-version-title'}).find('a').get('href')
        api_desc = api.find(
            'td', attrs={'class': 'views-field-field-api-description'}).text
        api_category_tags = api.find(
            'td', attrs={'class': 'views-field-field-article-primary-category'}).find('a')
        api_category = api_category_tags.text if api_category_tags else 'N/A'

        list_no += 1
        apis_list[list_no] = [api_name, api_link, api_desc, api_category]

    for api in apis_even:
        api_name = api.find(
            'td', attrs={'class': 'views-field-pw-version-title'}).find('a').text
        api_link = 'https://www.programmableweb.com' + \
            api.find('td', attrs={
                     'class': 'views-field-pw-version-title'}).find('a').get('href')
        api_desc = api.find(
            'td', attrs={'class': 'views-field-field-api-description'}).text
        api_category_tags = api.find(
            'td', attrs={'class': 'views-field-field-article-primary-category'}).find('a')
        api_category = api_category_tags.text if api_category_tags else 'N/A'

        list_no += 1
        apis_list[list_no] = [api_name, api_link, api_desc, api_category]

    url_tag = soup.find('a', {'title': 'Go to next page'})
    if url_tag:
        if url_tag.get('href'):
            url = 'https://www.programmableweb.com/' + url_tag.get('href')
        else:
            break
    else:
        break
    print("Total apis:", list_no)
    api_list_df = pd.DataFrame.from_dict(apis_list, orient = 'index', columns = ['API Nane', 'API Link', 'API Desc', 'API Category'])
    api_list_df.head()
    api_list_df.to_csv('api_list.csv')