import requests
import csv
from bs4 import BeautifulSoup as bs


headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
search_value = input("Type your request: ")
link = "https://krasnoyarsk.hh.ru/search/vacancy?text={}".format(search_value)


def parse(base_url, headers):
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)

    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = base_url[:-1] + str(i)
                if url not in urls:
                    urls.append(url)
        except:
            print("Error. Can't find jobs...")

        for url in urls:
            request = session.get(url, headers=headers)
            soup = bs(request.content, 'lxml')
            divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
            for div in divs:
                try:
                    title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                    href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                    company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                    vacansy_responsibility = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                    vacansy_requirement = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                    content = vacansy_responsibility + "  " + vacansy_requirement
                    jobs.append({
                        'title': title,
                        'href': href,
                        'company': company,
                        'content': content
                    })
                except:
                    print("Can't find divs")
                print("Parsing...")
        if(len(jobs) != 0):
            if len(jobs) == 1:
                print(str(len(jobs)) + " job was successful found!")
            else:
                print(str(len(jobs)) + " jobs were successful found!")
        else:
            print("No jobs found...")
    else:
        print("Error. Can't parse jobs...")
    return jobs


def file_writer(jobs):
    with open('jobs.csv', 'w', encoding='utf-8') as file:
        pen = csv.writer(file)
        pen.writerow(('Vacansy name', 'URL', 'Company name', 'Description'))
        for job in jobs:
            pen.writerow((job['title'], job['href'], job['company'], job['content']))


file_writer(parse(link, headers))
