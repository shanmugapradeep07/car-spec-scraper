import json
import os
import random
import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from scrapingbee import ScrapingBeeClient
from vp3.scrape_easy import open_html_file

def save_json(json_data, file_name):
    """Saves json data of page. Takes 2 arguments json data and file name without extension"""
    html_path = os.path.join(os.getcwd(), 'Html')  # html folder path
    if not os.path.exists(html_path):
        os.makedirs(html_path)
    json_file_name = os.path.join(html_path, f"{file_name}.json")
    json_obj = json.dumps(json_data, indent=3)
    with open(f'{json_file_name}', "w", encoding='utf-8') as file:
        file.write(json_obj)


def status_log(r):
    """Pass response as a parameter to this function"""
    url_log_file = 'url_log.txt'
    if not os.path.exists(os.getcwd() + '\\' + url_log_file):
        with open(url_log_file, 'w') as f:
            f.write('url, status_code\n')
    with open(url_log_file, 'a') as file:
        file.write(f'{r.url}, {r.status_code}\n')


def retry(func, retries=10):
    """Decorator function"""
    retry.count = 0

    def retry_wrapper(*args, **kwargs):
        attempt = 0
        while attempt < retries:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                attempt += 1
                total_time = attempt * 10
                print(f'Retrying {attempt}: Sleeping for {total_time} seconds, error: ', e)
                time.sleep(total_time)
            if attempt == retries:
                retry.count += 1
                url_log_file = 'url_log.txt'
                if not os.path.exists(os.getcwd() + '\\' + url_log_file):
                    with open(url_log_file, 'w') as f:
                        f.write('url, status_code\n')
                with open(url_log_file, 'a') as file:
                    file.write(f'{args[0]}, requests.exceptions.ConnectionError\n')
            # if retry.count == 3:
            #     print("Stopped after retries, check network connection")
            #     raise SystemExit

    return retry_wrapper


# @retry
def get_json_response(url, headers):
    """returns the soup of the page when given with the of an url and headers"""
    paid_api = 'UULGVA6441OBGSS5R9GGJ2ACXVF8F3NDVTLPP9M84F4N44RASF1JDKT4MAMH98PXIJKH1LQIPLYFAO1N'
    params = {
        'render_js': 'False',
    }
    client = ScrapingBeeClient(
        api_key=paid_api)
    # r = client.get(url, headers=headers, params=params)
    r = requests.get(url, headers=headers)
    r.encoding = r
    if r.status_code == 200:
        return r.json()
    elif 499 >= r.status_code >= 400:
        print(f'client error response, status code {r.status_code} \nrefer: {r.url}')
        status_log(r)
    elif 599 >= r.status_code >= 500:
        print(f'server error response, status code {r.status_code} \nrefer: {r.url}')
        count = 1
        while count != 1:
            print('while', count)
            # r = client.get(url, headers=headers)
            r = requests.get(url, headers=headers)
            r.encoding = r
            print('status_code: ', r.status_code)
            if r.status_code == 200:
                return r.json()
                # print('done', count)
            else:
                print('retry ', count)
                count += 1
                # print(count * 2)
                time.sleep(count * 3)
    else:
        status_log(r)
        return None


@retry
def post_json_response(url, headers, data):
    """returns the soup of the page when given with the of an url and headers"""
    # paid_api = 'G07W0JORAD5FN6QO03MBQI1BBFQ77FQ8UWVKKD40VYS0ZDB3VB4EDFJQVEOM7OCOBFCSQ3ZO885648WX'
    paid_api = 'UULGVA6441OBGSS5R9GGJ2ACXVF8F3NDVTLPP9M84F4N44RASF1JDKT4MAMH98PXIJKH1LQIPLYFAO1N'
    params = {
        'render_js': 'False',
    }
    client = ScrapingBeeClient(
        api_key=paid_api)
    r = client.post(url, headers=headers, data=json.dumps(data), params=params)
    # random_number = random.randint(1,10)
    # print(f"Sleeping for {random_number} seconds...!")
    # time.sleep(random_number)
    r.encoding = r
    if r.status_code == 200:
        return r.json()
    elif 499 >= r.status_code >= 400:
        print(f'client error response, status code {r.status_code} \nrefer: {r.url}')
        status_log(r)
    elif 599 >= r.status_code >= 500:
        print(f'server error response, status code {r.status_code} \nrefer: {r.url}')
        count = 1
        while count != 1:
            print('while', count)
            r = client.post(url, headers=headers, data=json.dumps(data))
            r.encoding = r
            print('status_code: ', r.status_code)
            if r.status_code == 200:
                return r.json()
                # print('done', count)
            else:
                print('retry ', count)
                count += 1
                # print(count * 2)
                time.sleep(count * 3)
    else:
        status_log(r)
        return None


def read_log_file():
    if os.path.exists('Visited_urls.txt'):
        with open('Visited_urls.txt', 'r', encoding='utf-8') as read_file:
            return read_file.read().split('\n')
    return []


def write_visited_log(url):
    with open('Visited_urls.txt', 'a', encoding='utf-8') as write_obj:
        write_obj.write(f"{url}\n")


def read_combination_pattern():
    if os.path.exists('Combination_Log.txt'):
        with open('Combination_Log.txt', 'r', encoding='utf-8') as read_file:
            return read_file.read()
    return ''


def write_combination_pattern(pattern):
    with open('Combination_Log.txt', 'a', encoding='utf-8') as write_obj:
        write_obj.write(f"{pattern}\n")


def open_json_file(file_name):
    '''Opens a html file and read it to return the soup of that page'''
    with open(fr'Html\{file_name}.json', 'r') as f:  # Folder name should be Json in the cwd
        data = f.read()
        json_data = json.loads(data)
        return json_data


# @retry
def get_soup(url, headers):
    """returns the soup of the page when given with the of an url and headers"""
    # paid_api = 'G07W0JORAD5FN6QO03MBQI1BBFQ77FQ8UWVKKD40VYS0ZDB3VB4EDFJQVEOM7OCOBFCSQ3ZO885648WX'
    paid_api = 'UULGVA6441OBGSS5R9GGJ2ACXVF8F3NDVTLPP9M84F4N44RASF1JDKT4MAMH98PXIJKH1LQIPLYFAO1N'
    client = ScrapingBeeClient(
        api_key=paid_api)
    parameters = {
        'country_code': 'us',
        'render_js': False
    }
    # r = client.get(url, headers=headers, params=parameters)
    r = requests.get(url, headers=headers)
    r.encoding = r
    if r.status_code == 200:
        return BeautifulSoup(r.text, 'html.parser')
    elif 499 >= r.status_code >= 400:
        print(f'client error response, status code {r.status_code} \nrefer: {r.url}')
        status_log(r)
    elif 599 >= r.status_code >= 500:
        print(f'server error response, status code {r.status_code} \nrefer: {r.url}')
        count = 1
        while count != 1:
            print('while', count)
            # r = client.get(url, headers=headers)
            r = requests.get(url, headers=headers)
            r.encoding = r
            print('status_code: ', r.status_code)
            if r.status_code == 200:
                return BeautifulSoup(r.text, 'html.parser')
                # print('done', count)
            else:
                print('retry ', count)
                count += 1
                # print(count * 2)
                time.sleep(count * 3)
    else:
        status_log(r)
        return None


def save_html(soup, file_name):
    """Saves html of the page. Takes 2 arguments soup and file name"""
    html_path = os.path.join(os.getcwd(), 'Html')  # html folder path
    if not os.path.exists(html_path):
        os.makedirs(html_path)
    html_file_name = os.path.join(html_path, f"{file_name}.html")
    with open(f'{html_file_name}', "w", encoding='utf-8') as file:
        file.write(str(soup))


def strip_it(text):
    return re.sub('\s+', ' ', text).strip()


def create_url(row):
    base_url = 'https://www.courts.mo.gov/cnet/cases/newHeader.do?'
    params = f'inputVO.caseNumber={row["caseNumber"]}&inputVO.courtId={row["dbSource"]}'
    return base_url + params


from vp3.scrape_easy import clean_header

if __name__ == '__main__':
    file_name = 'Comparison_Budgeted'
    budget = 8_00_000
    max_compromise = 30_000
    car_dict = {
        # 'nissan':['magnite'],
        'tata':['punch','altroz','tiago'],
        # 'maruti':['baleno'],
        # 'hyundai':['exter'],
    }
    data_list = []
    for company_name,models in car_dict.items():
        # company_name = 'nissan'
        for model in models:
            # model = 'magnite'
            # file_name = company_name.title() + '_' + model.title() + '_All_Variants_Specs'
            car_model_url = f'https://www.cardekho.com/{company_name}/{model}'
            # car_json_url = 'https://www.cardekho.com/api/v1/model/pwamodelspecs?'
            car_json_url = 'https://www.cardekho.com/api/v1/car-variant/detail?'
            header = {
                'Accept': 'application/json, text/plain, */*',
                'Referer': car_model_url,
                'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Source': 'WEB',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                }
            car_soup = get_soup(car_model_url,headers=header)
            required_columns = ['Power Steering','Power Windows-Front','Power Windows-Rear','Air Conditioner','Heater','Adjustable Steering','Low Fuel Warning Light','Accessory Power Outlet','Rear Seat Headrest','Rear Seat Centre Arm Rest','Parking Sensors','Engine Start/Stop Button','USB Charger','Gear Shift Indicator','Drive Modes','Leather Steering Wheel','Digital Clock','Digital Odometer','Dual Tone Dashboard','Power Adjustable Exterior Rear View Mirror','Wheel Covers','Alloy Wheels','Projector Headlamps','Halogen Headlamps','Tyre Size','Tyre Type','Wheel Size','LED DRLs','LED Taillights','Anti-Lock Braking System','Child Safety Locks','No. of Airbags','Driver Airbag','Passenger Airbag','Side Airbag-Front','Side Airbag-Rear','Rear Camera','ISOFIX Child Seat Mounts','Global NCAP Safety Rating','Global NCAP Child Safety Rating','Radio','Speakers Front','Speakers Rear','Integrated 2DIN Audio','Bluetooth Connectivity','Touch Screen','Android Auto','Subwoofer','Engine Type','Displacement (cc)','Max Power','Max Torque','No. of Cylinders','Valves Per Cylinder','Transmission Type','Gear Box','Drive Type','Fuel Type','Petrol Mileage (ARAI)','Petrol Fuel Tank Capacity (Litres)','Top Speed (Kmph)','Front Suspension','Rear Suspension','Steering Type','Front Brake Type','Rear Brake Type','Length (mm)','Width (mm)','Height (mm)','Boot Space (Litres)','Seating Capacity','Wheel Base (mm)','No. of Doors','ARAI Mileage','Engine Displacement (cc)','Max Power (bhp@rpm)','Max Torque (nm@rpm)','Fuel Tank Capacity (Litres)','Body Type','Service Cost (Avg. of 5 years)','Multi-function Steering Wheel','Engine Start Stop Button','onRoadPrice','No. of Speakers','Braking (100-0kmph)','0-100Kmph (Tested)','Braking (80-0 kmph)','Leather Seats','Touch Screen size','Connectivity','Sun Roof','Acceleration']
            for script_tag in car_soup.find_all('script'):
                if 'window.__INITIAL_STATE__ =' in script_tag.text:
                    json_data = script_tag.text.split('; window.__INITIAL_STATE__ = ')[-1].split('; window.__isWebp')[0]
                    json_data_decoded = json.loads(json_data)
                    # save_json(json_data_decoded,'json_data_decoded')
                    for variant in json_data_decoded['variantTable']['childs'][0]['items']:
                        variant_name = variant['text']
                        variantSlug = variant['variantSlug']
                        url = variant['url']
                        exShowRoomPrice = variant['exShowRoomPrice']
                        onRoadPrice = variant['onRoadPrice']
                        budget_diff = budget - onRoadPrice
                        if budget_diff < 0 and (budget_diff*-1) > max_compromise:
                            continue

                        modelSlug = url.split('/')[-2]#.split('.htm')[0]
                        print(variant_name,onRoadPrice)

                        car_header = {
                            'authority': 'www.cardekho.com',
                            'method': 'GET',
                            'path': '/api/v1/model/pwamodelspecs?&business_unit=car&country_code=in&_format=json&cityId=416&connectoid=2b066787-6535-d7df-0ad7-807d7bff0b0a&sessionid=a04bb4ac450f3079ce0fc19d1d43e5cc&lang_code=en&regionId=0&otherinfo=all&brandSlug=tata&modelSlug=punch&variantSlug=tata-punch-pure&variantId=0&url=/overview/Tata_Punch/Tata_Punch_Pure.htm',
                            'scheme': 'https',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Accept-Language': 'en-US,en;q=0.9',
                            'Cookie': 'cd_session_id=a04bb4ac450f3079ce0fc19d1d43e5cc; _gcl_au=1.1.1594567077.1699343349; _cc_id=613cd84fbf8ec8ad6aea797bf681520b; identifyCookie=eyJjYXJkZWtobyI6eyJfQ09faWQiOiIyYjA2Njc4Ny02NTM1LWQ3ZGYtMGFkNy04MDdkN2JmZjBiMGEiLCJsb3RhbWVfcGlkIjoiNjEzY2Q4NGZiZjhlYzhhZDZhZWE3OTdiZjY4MTUyMGIiLCJicm93c2VyTGlzdCI6W3siYnJvd3Nlck5hbWUiOiJDaHJvbWUiLCJicm93c2VyVmVyc2lvbiI6IjExNi4wLjAuMCIsIm9zTmFtZSI6IldpbmRvd3MiLCJvc1ZlcnNpb24iOiIxMCIsImRldmljZVR5cGUiOiJkZXNrdG9wIn1dfX0=; cto_bundle=eOQY119QMTBnSFJqbyUyRlgwaExJeG5JWWVEaVNzVGRZSDhEamtKanAlMkZhMDh2b1JnV3VXSzMzWDA5Z2Q1cEliNUc0SXFmTzF3bHNCcnk1WjQxVmVtWG9PQ25selBVUjFKU3dmNzhnZ1c1UGJTczdIS1EweE9ubjl3d3R6TENuUGMyZmtLOWZ6YkdNWklzY2lYMnAlMkY3ckhjRTVPUDljVlRKZkJLJTJCVlVTTXhMU1VGN2tDQm9nR1NvJTJCJTJCTkN0VU9KZTFWZ1FtSTJyMmh0ODlHS3RHamN2Sk14Z3RTOGNmRzMzWVFwRkJxd0lqaFNua2t6dndVOGJHd3lwd29tUXAlMkY2cVJtbU9NendKVXYlMkJSTThISDBiM3hYNSUyQjluNGVVcXpWNnl0NWxoaFhnZHl3SkxsUTVrRld4TWVmMGlIRFpIQ1F6eEpsVXRHcA; amp_6e403e=_H6eX4cW4i6bCaJ4jeyyiY...1hekc3it8.1hekc3it8.0.0.0; firstUTMParamter=https#referral#null; pwa_source={"isDesktop":true,"isMobile":false,"domain":"https://www.cardekho.com","cellId":29}; panoramaIdType=panoDevice; _pbjs_userid_consent_data=3524755945110770; SESSION=NzMyZTU5YjMtY2EyNy00ZjM3LThhY2EtNDFmNDU1NzkzNWZh; lastUTMParamter=google#organic#null; _co_session_active=1; pbjs_debug=0; panoramaId=728276ee5a66d2d629fbda97c1a5185ca02ca7addf9568d9283af3f0699b5197; _fbp=fb.1.1706280372927.2075673644; CityId=416; _gid=GA1.2.1917978534.1706280387; leadForm={"choices":{},"formData":{"cityName":"Tiruppur","cityId":"416","isVerify":false}}; _ga_X7DLD4S06V=GS1.2.1706280388.2.1.1706280456.0.0.0; _ga_ZSG4LZKVNZ=GS1.1.1706280387.2.1.1706280645.0.0.0; _ga=GA1.1.2063714145.1699343350; CONNECTOID=2b066787-6535-d7df-0ad7-807d7bff0b0a; _CO_type=connecto; _CO_anonymousId=2b066787-6535-d7df-0ad7-807d7bff0b0a; _browsee=eyJfaWQiOiIwZWY2MjU1NWIzYzUiLCJfdCI6MTcwNjI4MjQ4NzA3MywiX3IiOjAsIl9wIjp7ImNvIjpmYWxzZSwiZXQiOmZhbHNlLCJwciI6WzFdLCJpdCI6WzFdfX0=; __gads=ID=fea20ccadeb4f556:T=1699343349:RT=1706282486:S=ALNI_MblaheWKy_gpqYTQkwZ8eyRiseelQ; __gpi=UID=00000c81740a3c61:T=1699343349:RT=1706282486:S=ALNI_MZebWpIpaoP5A6vked1DYVjNxhQOQ; panoramaId_expiry=1706887293885; _browseet=eyJfdCI6MTcwNjI4MjQ5NzA5M30=; FCNEC=%5B%5B%22AKsRol9b15hPF4Gspb5C2pGrO8-kR7tSxZ13N4DZvs7BDxVOojq9QZCPTgQV5JMKI5xk9FOG75QDM4431JYqNBUbYqP4bhB5ngjRIn85IFTjXUTFG2-hrBn-R-UvT0nvKdM0GFwn6J4ADBNY8LyD-dLqFVkjuuiwNA%3D%3D%22%5D%5D; _ga_ZSZQ04WHM3=GS1.1.1706280372.3.1.1706282752.59.0.0',
                            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                            'Sec-Ch-Ua-Mobile': '?0',
                            'Sec-Ch-Ua-Platform': '"Windows"',
                            'Sec-Fetch-Dest': 'empty',
                            'Sec-Fetch-Mode': 'navigate',
                            'Sec-Fetch-Site': 'same-origin',
                            'Upgrade-Insecure-Requests': '1',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        }
                        # car_payload = {
                        #     'business_unit': 'car',
                        #     'country_code': 'in',
                        #     '_format': 'json',
                        #     'cityId': '416',
                        #     'connectoid': '2b066787-6535-d7df-0ad7-807d7bff0b0a',
                        #     'sessionid': 'a04bb4ac450f3079ce0fc19d1d43e5cc',
                        #     'lang_code': 'en',
                        #     'regionId': '0',
                        #     'otherinfo': 'all',
                        #     'brandSlug': '',
                        #     'modelSlug': modelSlug,
                        #     'variantSlug': variantSlug.lower().replace(' ','-'),
                        #     'variantId': '0',
                        #     'url': url,
                        # }
                        car_payload = {
                            'cityId': '416',
                            'connectoid': '2b066787-6535-d7df-0ad7-807d7bff0b0a',
                            'sessionid': 'a04bb4ac450f3079ce0fc19d1d43e5cc',
                            'lang_code': 'en',
                            'regionId': '0',
                            'otherinfo': 'all',
                            'url': url.replace('/','%2F'),
                            'brandSlug': '',
                            'modelSlug': modelSlug,
                            'source': 'web',
                            'verified': 'false',
                        }
                        required_url = car_json_url[::]
                        for key,value in car_payload.items():
                            required_url += f"&{key}={value}"
                        print(required_url)
                        car_header['path'] = required_url.split('https://www.cardekho.com')[-1]
                        car_header['Referer'] = 'https://www.cardekho.com' + url
                        category_json = get_json_response(required_url,headers=car_header)

                        variants = category_json['data']['variantTable']['childs']
                        selected_variants = category_json['data']['selectedVariant']
                        spec_keys = ['featured','specification','keySpecs']
                        data_dict = {'variant_name': selected_variants, 'onRoadPrice': onRoadPrice}

                        print(selected_variants)
                        for spec in spec_keys:
                            for feature in category_json['data']['specs'][spec]:
                                for item in feature['items']:
                                    column_name = item['text']
                                    if column_name in required_columns:
                                        data_dict[column_name] = item['value']


                        data_list.append(data_dict)
                # df = pd.DataFrame([data_dict])

                # if os.path.isfile(f'{file_name}.csv'):
                #     df.to_csv(f'{file_name}.csv', index=False, header=False, mode='a')
                # else:
    df = pd.DataFrame(data_list)
    df.to_csv(f'{file_name}.csv', index=False)





