import requests


def get_page():
    url = "http://api.wandoudl.com/api/ip?app_key=a9ba52aa5db36e05fbb595bbccf1bd60&pack=0&num=1&xy=1&type=1&lb=\r\n&mr=1&"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36" 
    }
    response = requests.get(url, headers=headers)
    # print(response.status_code)
    if response.status_code == 200:
        return response.text


def get_proxies():
    json_result = get_page()
    # print(json_result)
    # ip = json_result['msg'][0]['ip']
    # port = json_result['msg'][0]['port']
    proxy = json_result
    proxies = {
        'http': 'http://' + proxy, 
        'https': 'https://' + proxy 
    }
    return proxies
    # return proxy


if __name__ == '__main__':
    proxies = get_proxies()
    print(proxies)


