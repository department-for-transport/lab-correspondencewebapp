import urllib.request
import xmltodict
import pprint
import xml.etree.ElementTree as ET
import json



pp = pprint.PrettyPrinter(indent = 4)

def check_name(name):
    """gets rid of Rt Hon, MP etc and passes name to check_api"""

    try:
        if name[0] == 'Rt' or name[0] == 'RT':
            del(name[0])
        if name[0] == 'HON' or name[0] == 'Hon':
            del(name[0])
        if name[len(name)-1] == 'MP':
            del(name[len(name)-1])
        name = urllib.parse.quote(" ".join(name))
        return check_api(name)

    except IndexError:
        print('No name to check')
        pass



def check_api(nametocheck):
    """Checks API"""
    req = urllib.request.Request('http://data.parliament.uk/membersdataplatform/services/mnis/members/query/house=all|name*{}/GovernmentPosts'.format(nametocheck), headers = {'Accept':'application/json'})
    try:
        response = urllib.request.urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            return None
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
            return None
    else:

        str_response = response.read().decode('utf-8-sig')
        json_data = json.loads(str_response)
        response.close()
        if json_data['Members'] is not None:
            try:
                json_data = json_data['Members']['Member'][1]
            except KeyError:
                json_data = json_data['Members']['Member']
            mp_data = []

            mp_data.append(json_data['FullTitle'])
            try:
                mp_data.append(json_data['GovernmentPosts']['GovernmentPost']['Name'])
            except TypeError:
                pass
            return mp_data
        else:
            return None




if __name__ == '__main__':
    names = ['Chris', 'Grayling']
    info = check_name(names)
    print(info)
