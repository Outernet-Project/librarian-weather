#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import json
from time import sleep
from urllib import urlopen, quote_plus

# List of world capitals and larger cities for countries that span large
# teritorries (US, Canada, Russia, China, Australia).
#
# Note that tehse are search query strings, so some of the names migth be
# slightly different from the real names.
#
CITIES = [
    # World capitals
    "Kabul, Afghanistan",
    "Tirana, Albania",
    "Algiers, Algeria",
    "Andorra la Vella, Andorra",
    "Luanda, Angola",
    "St. John's, Antigua and Barbuda",
    "Buenos Aires, Argentina",
    "Yerevan, Armenia",
    "Canberra, Australia",
    "Vienna, Austria",
    "Baku, Azerbaijan",
    "Nassau, Bahamas",
    "Al Manámah, Bahrain",
    "Dhaka, Bangladesh",
    "Bridgetown, Barbados",
    "Minsk, Belarus",
    "Brussels, Belgium",
    "Belmopan, Belize",
    "Porto Novo, Benin",
    "Thimphu, Bhutan",
    "Sucre, Bolivia",
    "Sarajevo, Bosnia",
    "Gaborone, Botswana",
    "Brasília, Brazil",
    "Bandar Seri Begawan, Brunei",
    "Sofia, Bulgaria",
    "Ouagadougou, Burkina Faso",
    "Bujumbura, Burundi",
    "Phnom Penh, Cambodia",
    "Yaounde, Cameroon",
    "Ottawa, Canada",
    "Praia, Cape Verde",
    "Bangui, Central African Republic",
    "N'Djamena, Chad",
    "Santiago, Chile",
    "Beijing, China",
    "Santa Fe, Colombia",
    "Moroni, Comoros",
    "Kinshasa, Democratic Congo",
    "Brazzaville, Republic of Congo",
    "San Jose, Costa Rica",
    "Yamoussoukro, Cote d'Ivoire",
    "Zagreb, Croatia",
    "Havana, Cuba",
    "Lefkosia, Cyprus",
    "Prague, Czech Republic",
    "Copenhagen, Denmark",
    "Djibouti, Djibouti",
    "Roseau, Dominica",
    "Santo Domingo, Dominican Republic",
    "Dili, East Timor",
    "Quito 1, Ecuador",
    "Cairo, Egypt",
    "San Salvador, El Salvador",
    "Malabo, Equatorial Guinea",
    "Asmara, Eritrea",
    "Tallinn, Estonia",
    "Addis Ababa, Ethiopia",
    "Suva, Fiji",
    "Helsinki, Finland",
    "Paris, France",
    "Libreville, Gabon",
    "Banjul, Gambia",
    "Tbilisi, Georgia",
    "Berlin, Germany",
    "Accra, Ghana",
    "Athens, Greece",
    "St. George's, Grenada",
    "Guatemala City, Guatemala",
    "Conakry, Guinea",
    "Bissau, Guinea-Bissau",
    "Georgetown, Guyana",
    "Port-au-Prince, Haiti",
    "Tegucigalpa, Honduras",
    "Budapest, Hungary",
    "Reykjavik, Iceland",
    "New Delhi, India",
    "Jakarta, Indonesia",
    "Tehran, Iran",
    "Baghdad, Iraq",
    "Dublin, Ireland",
    "Jerusalem, Israel",
    "Rome, Italy",
    "Kingston, Jamaica",
    "Tokyo, Japan",
    "Amman, Jordan",
    "Astana, Kazakhstan",
    "Nairobi, Kenya",
    "Tarawa, Kiribati",
    "Pyongyang, Korea, North",
    "Seoul, Korea, South",
    "Pristina, Kosovo",
    "Kuwait, Kuwait",
    "Bishkek, Kyrgyzstan",
    "Vientiane, Laos",
    "Riga, Latvia",
    "Beirut, Lebanon",
    "Maseru 173, Lesotho",
    "Monrovia, Liberia",
    "Tripoli, Libya",
    "Vaduz, Liechtenstein",
    "Vilnius, Lithuania",
    "Luxembourg, Luxembourg",
    "Skopje, Macedonia",
    "Antananarivo, Madagascar",
    "Lilongwe, Malawi",
    "Kuala Lumpur, Malaysia",
    "Male, Maldives",
    "Bamako, Mali",
    "Valletta, Malta",
    "Majuro, Marshall Islands",
    "Nouakchott, Mauritania",
    "Port Louis, Mauritius",
    "Mexico City, Mexico",
    "Palikir, Micronesia",
    "Chisinau, Moldova",
    "Monaco, Monaco",
    "Ulan Bator, Mongolia",
    "Podgorica, Montenegro",
    "Rabat, Morocco",
    "Maputo, Mozambique",
    "Yangon, Myanmar",  # Rangoon
    "Windhoek, Namibia",
    "Yaren, Nauru",
    "Kathmandu, Nepal",
    "Amsterdam, Netherlands",
    "Wellington, New Zealand",
    "Managua, Nicaragua",
    "Niamey, Niger",
    "Abuja, Nigeria",
    "Oslo, Norway",
    "Muscat, Oman",
    "Islamabad, Pakistan",
    "Koror, Palau",
    "Jerusalem, Israel",  # Still part of Israel in database
    "Panama City, Panama",
    "Port Moresby, Papua New Guinea",
    "Asunción, Paraguay",
    "Lima, Peru",
    "Manila, Philippines",
    "Warsaw, Poland",
    "Lisbon, Portugal",
    "Doha, Qatar",
    "Bucharest, Romania",
    "Moscow, Russia",
    "Kigali, Rwanda",
    "Basseterre, St. Kitts and Nevis",
    "Castries, St. Lucia",
    "Kingstown, St. Vincent and the Grenadines",
    "Apia, Samoa",
    "San Marino, San Marino",
    "São Tome, Sao Tome and Príncipe",
    "Riyadh, Saudi Arabia",
    "Dakar, Senegal",
    "Belgrade, Serbia",
    "Victoria, Seychelles",
    "Freetown, Sierra Leone",
    "Singapore, Singapore",
    "Bratislava, Slovakia",
    "Ljubljana, Slovenia",
    "Honiara, Solomon Islands",
    "Mogadishu, Somalia",
    "Pretoria, South Africa",
    "Juba, South Sudan",
    "Madrid, Spain",
    "Colombo, Sri Lanka",
    "Khartoum, Sudan",
    "Paramaribo, Suriname",
    "Mbabane, Swaziland",
    "Stockholm, Sweden",
    "Bern, Switzerland",
    "Damascus, Syria",
    "Taipei, Taiwan",
    "Dushanbe, Tajikistan",
    "Dodoma, Tanzania",
    "Bangkok, Thailand",
    "Lomé, Togo",
    "Nuku'alofa, Tonga",
    "Port of Spain, Trinidad and Tobago",
    "Tunis, Tunisia",
    "Ankara, Turkey",
    "Ashgabat, Turkmenistan",
    "Funafuti, Tuvalu",
    "Kampala, Uganda",
    "Kiev, Ukraine",
    "Abu Dhabi, United Arab Emirates",
    "London, United Kingdom",
    "Washington, United States",
    "Montevideo, Uruguay",
    "Tashkent, Uzbekistan",
    "Port Vila, Vanuatu",
    "Caracas, Venezuela",
    "Hanoi, Vietnam",
    "Sanaa, Yemen",
    "Lusaka, Zambia",
    "Harare, Zimbabwe",

    # US state capitals
    "Montgomery, AL, United States",
    "Juneau, AK, United States",
    "Phoenix, AZ, United States",
    "Little Rock, AR, United States",
    "Sacramento, CA, United States",
    "Denver, CO, United States",
    "Hartford, CT, United States",
    "Dover, DE, United States",
    "Tallahassee, FL, United States",
    "Atlanta, GA, United States",
    "Honolulu, HI, United States",
    "Boise, ID, United States",
    "Springfield, IL, United States",
    "Indianapolis, IN, United States",
    "Des Moines, IA, United States",
    "Topeka, KS, United States",
    "Frankfort, KY, United States",
    "Baton Rouge, LA, United States",
    "Augusta, ME, United States",
    "Annapolis, MD, United States",
    "Boston, MA, United States",
    "Lansing, MI, United States",
    "Saint Paul, MN, United States",
    "Jackson, MS, United States",
    "Jefferson City, MO, United States",
    "Helena, MT, United States",
    "Lincoln, NE, United States",
    "Carson City, NV, United States",
    "Concord, NH, United States",
    "Trenton, NJ, United States",
    "Santa Fe, NM, United States",
    "Albany, NY, United States",
    "Raleigh, NC, United States",
    "Bismarck, ND, United States",
    "Columbus, OH, United States",
    "Oklahoma City, OK, United States",
    "Salem, OR, United States",
    "Harrisburg, PA, United States",
    "Providence, RI, United States",
    "Columbia, SC, United States",
    "Pierre, SD, United States",
    "Nashville, TN, United States",
    "Austin, TX, United States",
    "Salt Lake City, UT, United States",
    "Montpelier, VT, United States",
    "Richmond, VA, United States",
    "Olympia, WA, United States",
    "Charleston, WV, United States",
    "Madison, WI, United States",
    "Cheyenne, WY, United States",

    # Canadian privince capitals
    "Toronto, ON, Canada",
    "Quebec City, QC, Canada",
    "Halifax, NS, Canada",
    "Fredericton, NB, Canada",
    "Winnipeg, MB, Canada",
    "Victoria, BC, Canada",
    "Charlottetown, PE, Canada",
    "Regina, SK, Canada",
    "Edmonton, AB, Canada",
    "St. John's, NL, Canada",

    # Largest cities in Russia (except Moscow)
    "Saint Petersburg, Russia",
    "Novosibirsk, Russia",
    "Yekaterinburg, Russia",
    "Nizhny Novgorod, Russia",
    "Samara, Russia",
    "Omsk, Russia",
    "Kazan, Russia",
    "Chelyabinsk, Russia",
    "Rostov-on-Don, Russia",
    "Ufa, Russia",
    "Volgograd, Russia",
    "Perm, Russia",
    "Krasnoyarsk, Russia",
    "Voronezh, Russia",
    "Saratov, Russia",
    "Krasnodar, Russia",
    "Tolyatti, Russia",
    "Izhevsk, Russia",
    "Ulyanovsk, Russia",
    "Barnaul, Russia",
    "Vladivostok, Russia",
    "Yaroslavl, Russia",
    "Irkutsk, Russia",
    "Tyumen, Russia",
    "Khabarovsk, Russia",
    "Makhachkala, Russia",
    "Orenburg, Russia",
    "Novokuznetsk, Russia",
    "Kemerovo, Russia",
    "Ryazan, Russia",
    "Tomsk, Russia",
    "Astrakhan, Russia",
    "Penza, Russia",
    "Naberezhnye Chelny, Russia",
    "Lipetsk, Russia",
    "Tula, Russia",
    "Kirov, Russia",
    "Cheboksary, Russia",
    "Kaliningrad, Russia",
    "Bryansk, Russia",
    "Kursk, Russia",
    "Ivanovo, Russia",
    "Magnitogorsk, Russia",
    "Ulan-Ude, Russia",
    "Tver, Russia",
    "Stavropol, Russia",
    "Nizhny Tagil, Russia",
    "Belgorod, Russia",
    "Arkhangelsk, Russia",
    "Vladimir, Russia",
    "Sochi, Russia",
    "Kurgan, Russia",
    "Smolensk, Russia",
    "Kaluga, Russia",
    "Chita, Russia",
    "Oryol, Russia",
    "Volzhsky, Russia",
    "Cherepovets, Russia",
    "Vladikavkaz, Russia",
    "Murmansk, Russia",
    "Surgut, Russia",
    "Vologda, Russia",
    "Saransk, Russia",
    "Tambov, Russia",
    "Sterlitamak, Russia",
    "Grozny, Russia",
    "Yakutsk, Russia",
    "Kostroma, Russia",
    "Komsomolsk-on-Amur, Russia",
    "Petrozavodsk, Russia",
    "Taganrog, Russia",
    "Nizhnevartovsk, Russia",
    "Yoshkar-Ola, Russia",
    "Bratsk, Russia",
    "Novorossiysk, Russia",
    "Dzerzhinsk, Russia",
    "Nalchik, Russia",
    "Shakhty, Russia",
    "Orsk, Russia",
    "Syktyvkar, Russia",
    "Nizhnekamsk, Russia",
    "Angarsk, Russia",
    "Stary Oskol, Russia",
    "Veliky Novgorod, Russia",
    "Balashikha, Russia",
    "Blagoveshchensk, Russia",
    "Prokopyevsk, Russia",
    "Biysk, Russia",
    "Khimki, Russia",
    "Pskov, Russia",
    "Engels, Russia",
    "Rybinsk, Russia",

    # Largest cities in China (Except Beijing)
    "Guangzhou, China",
    "Shanghai, China",
    "Shantou, China",
    "Shenzhen, China",
    "Tianjin, China",
    "Chengdu, China",
    "Dongguan, China",
    "Hangzhou, China",
    "Wuhan, China",
    "Shenyang, China",
    "Xi'an, China",
    "Nanjing, China",
    "Hong Kong, China",
    "Chongqing, China",
    "Quanzhou, China",
    "Wenzhou, China",
    "Qingdao, China",
    "Suzhou, China",
    "Harbin, China",
    "Qiqihar, China",
    "Xiamen, China",
    "Zhengzhou, China",
    "Jinan, China",
    "Nanchang, China",
    "Dalian, China",
    "Changsha, China",
    "Taiyuan, China",
    "Shijiazhuang, China",
    "Kunming, China",
    "Wuxi, China",
    "Changchun, China",
    "Ningbo, China",
    "Zibo, China",
    "Hefei, China",
    "Changzhou, China",
    "Taizhou, China",
    "Tangshan, China",
    "Nantong, China",
    "Nanning, China",
    "Guiyang, China",
    "Ürümqi, China",
    "Fuzhou, China",
    "Huai'an, China",
    "Xuzhou, China",
    "Linyi, China",
    "Lanzhou, China",
    "Yangzhou, China",
    "Huizhou, China",
    "Anshan, China",
    "Huaibei, China",
    "Haikou, China",
    "Yiwu, China",
    "Baotou, China",
    "Liuzhou, China",
    "Anyang, China",
    "Hohhot, China",
    "Jilin City, China",
    "Putian, China",
    "Xiangtan, China",
    "Yantai, China",
    "Luoyang, China",
    "Huainan, China",
    "Nanchong, China",
    "Jiangmen, China",
    "Nanyang, China",
    "Baoding, China",
    "Fuyang, China",
    "Tai'an, China",
    "Suzhou, China",
    "Lu'an, China",
    "Datong, China",
    "Yancheng, China",
    "Zhanjiang, China",
    "Tengzhou, China",
    "Huangshi, China",
    "Jiangyin, China",
    "Weifang, China",
    "Yinchuan, China",
    "Changshu, China",
    "Zhuhai, China",
    "Dengzhou, China",
    "Cixi, China",
    "Changde, China",
    "Pizhou, China",
    "Baoji, China",
    "Suqian, China",
    "Daqing, China",
    "Bozhou, China",
    "Handan, China",
    "Panjin, China",
    "Wenling, China",
    "Ma'anshan, China",
    "Zigong, China",
    "Fushun, China",
    "Mianyang, China",
    "Yingkou, China",
    "Yichang, China",
    "Heze, China",
    "Chifeng, China",
    "Guilin, China",
    "Yingkou, China",
    "Xiangyang, China",
    "Haicheng, China",
    "Rugao, China",
    "Xuchang, China",
    "Neijiang, China",
    "Zhangjiagang, China",
    "Yixing, China",
    "Fuqing, China",
    "Zhaoqing, China",
    "Xinyang, China",
    "Liaocheng, China",
    "Maoming, China",
    "Jiaxing, China",
    "Zhenjiang, China",
    "Xining, China",
    "Tianshui, China",
    "Ganzhou, China",
    "Huazhou, China",
    "Qujing, China",
    "Dingzhou, China",
    "Wuhu, China",
    "Zhuji, China",
    "Xingtai, China",
    "Jingzhou, China",
    "Shouguang, China",
    "Yuzhou, China",
    "Bazhong, China",
    "Zoucheng, China",
    "Jining, China",
    "Zunyi, China",
    "Jinzhou, China",
    "Guigang, China",
    "Zhucheng, China",
    "Jinhua, China",
    "Hengyang, China",
    "Taixing, China",
    "Zhangqiu, China",
    "Zhuzhou, China",
    "Lianyungang, China",
    "Ezhou, China",
    "Pingdingshan, China",
    "Qinhuangdao, China",
    "Linhai, China",
    "Benxi, China",
    "Wuwei, China",
    "Hezhou, China",
    "Zaoyang, China",
    "Xiangcheng, China",
    "Dongying, China",
    "Yueyang, China",
    "Laiwu, China",
    "Bengbu, China",
    "Qidong, China",
    "Mudanjiang, China",
    "Danyang, China",
    "Wuchuan, China",
    "Feicheng, China",
    "Xianyang, China",
    "Linfen, China",
    "Xinyi, China",
    "Weihai, China",
    "Haimen, China",
    "Xinxiang, China",
    "Zaozhuang, China",
    "Kaifeng, China",
    "Hengyang, China",
    "Shaoxing, China",
    "Jiamusi, China",
    "Suihua, China",
    "Langfang, China",
    "Jiaozuo, China",
    "Rizhao, China",
    "Zhoushan, China",
    "Yibin, China",
    "Kashgar, China",
    "Dandong, China",
    "Panzhihua, China",
    "Anqing, China",
    "Huludao, China",
    "Shaoyang, China",
    "Binzhou, China",
    "Zhangzhou, China",
    "Fuxin, China",
    "Dezhou, China",
    "Yangjiang, China",
    "Tieling, China",
    "Liaoyang, China",
    "Puyang, China",
    "Yulin, China",
    "Jingjiang, China",
    "Zhangzhou, China",
    "Jiujiang, China",
    "Taizhou, China",
    "Chuzhou, China",
    "Macau, China",
    "Cangzhou, China",
    "Aksu, China",
    "Beihai, China",
    "Zhoukou, China",
    "Hegang, China",
    "Nanping, China",
    "Chaozhou, China",
    "Lishui, China",
    "Lhasa, China",
    "Karamay, China",
    "Altay, China",
    "Lijiang, China",

    # Largest cities in Australia (except Sidney)
    "Melbourne, Australia",
    "Brisbane, Australia",
    "Perth, Australia",
    "Adelaide, Australia",
]

API_BASE = b'http://api.openweathermap.org/data/2.5/'
FORECAST_URL = b'forecast/daily'
FORECAST_PARAMS = b'?q=%(query)s&mode=json&units=metric&cnt=14&APPID=%(key)s'


def get_url(api_key, location):
    location = quote_plus(location.encode('utf8'))
    api_key = api_key.encode('utf8')
    params = FORECAST_PARAMS % {'query': location, 'key': api_key}
    return API_BASE + FORECAST_URL + params


def parse_weather(data):
    try:
        location = '%s, %s' % (data['city']['name'], data['city']['country'])
        weather_data = data['list']
    except KeyError:
        print(data)
        raise
    if location == ', ':
        raise RuntimeError('Missing location data')
    print('--> %s (%s datapoints)' % (location, len(weather_data)))
    return location, weather_data


def fetch_data(url, tries=5, errors=[], timeout=1):
    if not tries:
        errors = '\n'.join([str(e) for e in errors])
        raise RuntimeError("ERROR '%s':\n%s" % ( url, errors))
    tries -= 1
    try:
        data = urlopen(url).read()
        return parse_weather(json.loads(data))
    except Exception as err:
        errors.append(err)
        print("Error, retrying with %s tries left" % tries)
        sleep(timeout)
        return fetch_data(url, tries, errors, timeout + 1)


def get_weather(api_key):
    all_data = {}
    cities = []
    skipped = []
    print("Fetching weather forecast for %s cities" % len(CITIES))
    for idx, place in enumerate(CITIES):
        print('[%03d] %s' % (idx, place))
        try:
            location, weather = fetch_data(get_url(api_key, place))
        except RuntimeError:
            skipped.append(place)
            continue
        all_data[location] = weather
        cities.append(location)
    data = json.dumps(all_data)
    with open('weather.json', 'w') as f:
        f.write(data)
    print('Written weather.json')
    with open('cities.json', 'w') as f:
        f.write(json.dumps(cities))
    print('Written cities.json')
    with open('skipped.txt', 'w') as f:
        f.write('\n'.join(skipped))
    print('Written skipped.txt')

if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description='Fetch weather data from openweathermap.org')
    parser.add_argument('--key', metavar='API_KEY')
    args = parser.parse_args(sys.argv[1:])
    get_weather(args.key)