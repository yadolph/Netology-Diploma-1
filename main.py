import requests
import pprint
import time
import json


TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'

class User:

    def __init__(self,screen_name):
        if isinstance(screen_name, int):
            self.user_id = screen_name
        else:
            try:
                params = {
                    'user_ids': screen_name,
                    'access_token': TOKEN,
                    'v': '5.89',
                    'lang': 'ru',
                    'fields': 'id'
                }
                response = requests.get('https://api.vk.com/method/users.get', params=params)
                self.user_id = response.json()['response'][0]['id']
            except KeyError:
                exit('Проверьте правильность написания индентификаторов')

    def __str__(self):
        return f'https://vk.com/id{self.user_id}'

    def friend_list(self):
        params = {
            'user_id': self.user_id,
            'access_token': TOKEN,
            'v': '5.89',
            'lang': 'ru'
        }
        response = requests.get('https://api.vk.com/method/friends.get', params=params)
        friend_list = []
        for friend in response.json()['response']['items']:
            friend_list.append(User(friend))
        return friend_list


    def group_list(self):
        params = {
            'user_id': self.user_id,
            'access_token': TOKEN,
            'v': '5.89',
            'lang': 'ru',
            'extended': '0'
        }
        response = requests.get('https://api.vk.com/method/groups.get', params=params)
        print('-', end='')
        if 'response' in response.json():
            return response.json()['response']['items']
        else:
            return None

class Group:

    def __init__(self, id):
        self.id = id

    def get_info(self):
        params = {
            'group_id': self.id,
            'access_token': TOKEN,
            'v': '5.89',
            'lang': 'ru',
            'fields': 'members_count'
        }
        response = requests.get('https://api.vk.com/method/groups.getById', params=params)
        return response.json()['response'][0]

user1 = User('oleksin')

user_friend_list = user1.friend_list()

user_group_list = user1.group_list()

friend_group_list = []

print('Requesting group lists of friends...')

for friend in user_friend_list:
    friend_gl = friend.group_list()
    time.sleep(0.33)
    if friend_gl:
        friend_group_list.extend(friend_gl)
    else:
        continue

friend_group_list = list(set(friend_group_list))

diff_group_list = [x for x in user_group_list if x not in friend_group_list]

dgl = []

for group in diff_group_list:
    dgl.append(Group(group))

glist = []

for group in dgl:
    ginfo = group.get_info()
    ginfo_clean = {key : ginfo[key] for key in ['name','id','members_count']}
    glist.append(ginfo_clean)

print(glist)

with open('groups.json', 'w', encoding='utf-8') as output:
    json.dump(glist, output, ensure_ascii=False, indent=4)









