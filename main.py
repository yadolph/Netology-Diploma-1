import requests
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


def get_friend_group_list(user_friend_list):
    print('Запрашиваем списки групп друзей пользователя...')
    friend_group_list = []
    req_count = 1
    for friend in user_friend_list:
        friend_gl = friend.group_list()
        print(f'Запрос № {req_count} из {len(user_friend_list)} ({round(req_count / len(user_friend_list) * 100, 1)}%)\r', end='')
        req_count += 1
        time.sleep(0.333)
        if friend_gl:
            friend_group_list.extend(friend_gl)
        else:
            continue
    friend_group_list = list(set(friend_group_list))
    return friend_group_list


def get_different_group_list(user_group_list, friend_group_list):
    diff_group_list = [Group(x) for x in user_group_list if x not in friend_group_list]
    if diff_group_list:
        print('Запрашиваем информацию об уникальных группах пользователя...')
        group_list_clean = []
        req_count = 1
        for group in diff_group_list:
            print(f'Запрос № {req_count} из {len(diff_group_list)} ({round(req_count / len(diff_group_list) * 100, 1)}%)\r', end='')
            ginfo = group.get_info()
            ginfo_clean = {key: ginfo[key] for key in ['name', 'id', 'members_count']}
            group_list_clean.append(ginfo_clean)
            time.sleep(0.333)
            req_count += 1
        return group_list_clean
    else:
        print('У данного пользователя нет уникальных групп')
        return 'У данного пользователя нет уникальных групп'


user1 = User(input('Введите идентификатор пользователя в сети VK: '))

output = get_different_group_list(user1.group_list(), get_friend_group_list(user1.friend_list()))

with open('groups.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)
    print('Данные об уникальный группах пользователя записаны в файл groups.json')









