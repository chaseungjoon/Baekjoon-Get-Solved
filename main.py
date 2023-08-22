import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
user_agent = ua.random
headers = {
    'User-Agent': user_agent
}

def get_solved(user_id):
    problem_numbers = []
    submission_numbers = []
    url = f'https://www.acmicpc.net/status?user_id={user_id}&result_id=4'
    while len(submission_numbers) != 1:
        with requests.Session() as session:
            r = session.get(url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            href_values = [a['href'] for a in soup.find_all('a', class_='problem_title')]
            problem_numbers += [int(href.split('/')[-1]) for href in href_values]

            trs = soup.find_all('tr', id=lambda x: x and x.startswith('solution-'))
            submission_numbers = [tr.find('td').text for tr in trs]

        url = f'https://www.acmicpc.net/status?user_id={user_id}&result_id=4&top={submission_numbers[-1]}'
        problem_numbers = list(set(problem_numbers))

    return problem_numbers

my_id = input("Enter your id >> ").strip()
print(get_solved(my_id))
