import requests
import argparse



def fetch_proxy(targetURL, count):
    URL = f'https://proxylist.geonode.com/api/proxy-list?limit={count}&page=1&sort_by=lastChecked&sort_type=desc&protocols=http' # proxy database

    response = requests.get(URL).json()
    data, available = response['data'], response['total']

    proxies = []
    try:
        if count <= available:
            for i in range(count):
                proxies.append((data[i]['ip'],data[i]['port'])) # Appends tuple (ip, port) to proxies.
        else:
            print(f'There are only {available} available proxies atm. your requested: {count}.')
    finally:
        row = 0
        for proxy in proxies:
            row += 1
            proxy_dict = {'http': f'http://{proxy[0]}:{proxy[1]}'}

            _response = requests.get(targetURL, proxies=proxy_dict)
            print(row, _response.status_code, proxy)

            if _response.status_code == 200:
                with open(f'proxies/{targetURL[8:]}-proxies.txt', 'a') as f:
                    f.write(f'{proxy[0]}:{proxy[1]}\n')
                f.close()
            


parser = argparse.ArgumentParser(description='Proxy checker')
parser.add_argument('targetURL', type=str, help='targetURL example: https://example.com')
parser.add_argument('proxyCount', type=int, help='proxy count')
args = parser.parse_args()

fetch_proxy(args.targetURL, args.proxyCount)
