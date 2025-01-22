#!/usr/bin/env python
import requests
import argparse
from bs4 import BeautifulSoup


SETTINGS = {
    'model': 'moritomo',  # 'moritomo', 'kojima', 'cumin', 'namuec'
    'rlocale': 'en_US',
    'locale': 'NONE',
    'level': 6,  # 9-1 for moritomo and kojima, 6-3 and 1 for cumin, 13-10 for namuec
    'solution': 'Interactive',  # 'None', 'Interactive' (HTML only), 'Inline', 'End', 'SplitEnd'
    'output': 'HTML',  # 'PDF', 'HTML'
    'difficulty': 'STARS',  # 'NONE', 'STARS', 'COUNT'
} 


def get_exam_link(override_settings: dict = None):
    s = requests.Session()
    s.headers.update({
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    })
    pre_res = s.get('https://www.sorobanexam.org/generator.html')
    soup = BeautifulSoup(pre_res.content, features='html.parser')
    token = soup.find(id='etoken').get('value')
    
    settings = SETTINGS.copy()
    if override_settings:
        settings.update(override_settings)
    settings['token'] = token

    s.headers.update({
        'origin': 'https://www.sorobanexam.org',
        'referer': 'https://www.sorobanexam.org/generator.html',
    })
    res = s.post('https://www.sorobanexam.org/ws/create', settings)
    if res.status_code == 200:
        return res.request.url

    raise Exception(f'Something went wrong!\n{BeautifulSoup(res.content, features="html.parser")}')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--level', type=int, default=6, help='level of exam (easiest 9 - hardest 1)')
    return parser.parse_args()


if __name__ == '__main__':
    options = vars(parse_args())
    print(get_exam_link(options))

