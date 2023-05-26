
#pylint: disable=all
import requests,json,os
from selectorlib import Extractor


extractor = Extractor.from_yaml_file('config.yml')

def scrape(url):
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    print("Downloading {}".format(url))
    obj = requests.get(url, headers=headers)

    if obj.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in obj.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,obj.status_code))
        return None
    return extractor.extract(obj.text)


def utils():
    with open("urls.txt",'r') as urllist, open('results.json','w') as outfile:
        for url in urllist.read().splitlines():
            data = scrape(url)
            if data:
                for idx, product in enumerate(data['products']):
                    product['search_url'] = url
                    response = requests.get(product['image'])
                    print(idx)
                    print(response.status_code)
                    dir_path = './imgs/'
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)
                    with open(f'{dir_path}{idx+1}.jpg', 'wb') as fp:
                            fp.write(response.content)
                    print("Saving Product: {}".format(product['title']))
                    json.dump(product,outfile)
                    outfile.write(",\n")


def main():
    utils()

main()