#!/usr/bin/env python
__version__ = "0.0.1"

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


def get_exam(override_settings: dict = None, stream=False):
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
    res = s.post('https://www.sorobanexam.org/ws/create', settings, stream=stream)
    if res.status_code == 200:
        return res

    soup = BeautifulSoup(res.content, features='html.parser')
    content = soup.find(id='content')
    if not content:
        content = soup
    raise Exception(
        f'Something went wrong!\n{content}'
    )


def get_exam_link(override_settings: dict = None):
    res = get_exam(override_settings)
    return res.request.url


def get_exam_pdf(pdf_name: str = None, override_settings: dict = None):
    if pdf_name and not pdf_name.endswith('.pdf'):
        pdf_name += '.pdf'
    if not override_settings:
        override_settings = {}
    override_settings['output'] = 'PDF'
    override_settings['solution'] = 'End'
    override_settings['locale'] = 'AUTO'
    override_settings['size'] = 'A4'
    res = get_exam(override_settings, stream=True)
    if res.headers.get('content-type') != 'application/pdf':
        raise Exception(f'Something went wrong!\n{res.content}')
    if not pdf_name:
        pdf_name = res.headers.get('content-disposition').split('=')[1].strip()
    with open(pdf_name, 'wb') as pdf_file:
        pdf_file.write(res.content)
        print('Your exam is at {}'.format(pdf_name))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--level', type=int, default=6, help='level of exam (easiest 9 - hardest 1)')
    parser.add_argument('-o', '--output', type=str, default=None, help='output PDF name')
    parser.add_argument('-m', '--model', type=str, default='moritomo',
                        choices=['moritomo', 'kojima', 'cumin', 'namuec'],
                        help="select exam model (default: moritomo)")
    parser.add_argument('-s', '--solution', type=str, default='Inline',
                        choices=['Interactive', 'None', 'Inline', 'End', 'SplitEnd'],
                        help="select exam solution (default: Inline)")
    return parser.parse_args()


def main():
    options = vars(parse_args())
    pdf_name = options.pop('output')
    if not pdf_name:
        link = get_exam_link(options)
        print('Here is you exam link!\n')
        print('    {}'.format(link))
    else:
        get_exam_pdf(pdf_name, override_settings=options)
    print('\nIf you like this program, please support https://www.sorobanexam.org/about.html')


if __name__ == '__main__':
    main()
