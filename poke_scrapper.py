from argparse import ArgumentParser
from bs4 import BeautifulSoup
import requests


def get_name_from_html_txt(input_txt: str) -> str:
    lower_str = input_txt.lower().replace("'", '').replace(". ", '-')
    if lower_str.find(u'u2640') != -1:
        lower_str = 'nidoran-f'
    elif lower_str.find(u'u2642') != -1:
        lower_str = 'nidoran-m'

    return lower_str


if __name__ == '__main__':

    ap = ArgumentParser()

    # ap.add_argument(
    #     '-p', '--pokemon-list', required=True, help='Pth to raw html file')
    ap.add_argument(
        '-s', '--sprites', required=False, help='Dir for storing sprites',
        default='./sprites')

    args = vars(ap.parse_args())

    page_get_resp = \
        requests.get(url='https://pokemondb.net/pokedex/national#gen-1')

    # print(page_get_resp.text)
    # input('sanity check')

    soup = BeautifulSoup(page_get_resp.text)
    names = []

    blue_links = []

    for link in soup.findAll('a'):

        # print(link)

        prcsd_link = str(link)
        if 'data-src=' in prcsd_link:
            data_src_txt_dirty = prcsd_link.split('data-src=')[-1]
            data_src_txt_clean = \
                [el for el in data_src_txt_dirty.split('"') if el][0]
            # print(data_src_txt_clean)
            # input('sanity check')
            blue_links.append(data_src_txt_clean)

    # prcsd_names = []
    for img_link in blue_links:

        poke_name = \
            img_link.split('/')[-1].replace('.png', '').lower() \
            .replace('.', '').replace(',', '')

        img_resp = \
            requests.get(
                'http://img.pokemondb.net/sprites/red-blue/normal/{}.png'
                .format(poke_name))

        if img_resp.status_code != 200:
            print('[x] Error downloading %s' % img_link)
            continue

        # f = open('%s%s.png' % (args['sprites'], name), 'wb')
        with open('{}/{}.png'.format(args['sprites'], poke_name), 'wb') as imgf:
            print('{} has been saved.'.format(poke_name))
            imgf.write(img_resp.content)
        # f.write(resp.content)
        # f.close()
