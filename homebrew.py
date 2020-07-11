import requests
import json
import time

r = requests.get('https://formulae.brew.sh/api/formula.json')
packages_json = r.json()

results = []

t1 = time.perf_counter()

for package in packages_json:
    packages_name = package['name']
    packages_desc = package['desc']

    packages_url = f'https://formulae.brew.sh/api/formula/{packages_name}.json'

    r = requests.get(packages_url)

    packages_json = r.json()

    install_30 = packages_json['analytics']['install_on_request']['30d'][packages_name]
    install_90 = packages_json['analytics']['install_on_request']['90d'][packages_name]
    install_365 = packages_json['analytics']['install_on_request']['365d'][packages_name]

    data = {
        'name': packages_name,
        'desc': packages_desc,
        'analytics':{
            '30d': install_30,
            '90d': install_90,
            '365d': install_365
        }
    }

    results.append(data)

    time.sleep(r.elapsed.total_seconds())
    print(f'Got {packages_name} in {r.elapsed.total_seconds()}')


t2 = time.perf_counter()
print(f'Finished in {t2-t1} seconds')

with open('package_info.json','w') as f:
    json.dump(results,f,indent=2)

