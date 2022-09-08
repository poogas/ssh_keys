#!/usr/bin/env python3

from os import environ, listdir, system
from sh import ssh_agent, pkill, git
from yaml import safe_load


file_key = '~/.ssh/id_ed25519'
inventory = '~/ssh_keys/hosts'

user_name = environ['USER']
user_ip = environ['SSH_CLIENT'].split()[0]

file_name_in_users = [user for user in listdir('users') if user.endswith('.yml')]

for key, value in enumerate(file_name_in_users):
    print(f'{key})', value)

selected_key = int(input('choose one of user: '))
selected_user = file_name_in_users[selected_key]
print(f'ok, work with {selected_user}')

out = ssh_agent('-s')
get_value = [el.split(';')[0].split('=') for el in out if 'SSH' in el]

for item in get_value:
    environ[item[0]] = item[1]

print('ssh-agent started')

system(f'ssh-add {file_key}')

def get_content(path):
    with open(path) as file:
        return safe_load(file)


dict_content = get_content(f'users/{selected_user}')
content_in_dict = dict_content[str(*dict_content)]

action = ['add', 'del']

def git_push(action):
    git('add', '.')
    git('commit', '-m', f'auto: {user_name} from ip {user_ip} has changed some files and run {action} command for {selected_user}')
    git('push', 'origin', 'master')


def play(content, action):
    user = content['user']
    key = content['pub_ssh_key']

    payload = {"servers": content[f'{action}_servers'], 
               "user": user, 
               "key": key}

    system(f'ansible-playbook -i {inventory} {action}.yml -e "{payload}"')
    try:
        git_push(action)
    except:
        pass


try:
    if dict(*content_in_dict)['del_servers']:
        for key, value in enumerate(action):
            print(f'{key})', value)

        selected_action_key = int(input('choose one of action: '))
        action = action[selected_action_key]

        play(*content_in_dict, action)
    else:
        play(*content_in_dict, action[0])
except TypeError:
    for key, value in enumerate(content_in_dict):
        user = value[f'{[*value][0]}']

        try:
            user = f"{user} ({value['comment']})"
        except KeyError:
            pass

        print(f'{key})', user)

    selected_key_for_user_host = int(input('choose one of user for host: '))
    user_data_for_host = content_in_dict[selected_key_for_user_host]

    if user_data_for_host['del_servers']:
        for key, value in enumerate(action):
            print(f'{key})', value)

        selected_action_key = int(input('choose one of action: '))
        action = action[selected_action_key]

        play(user_data_for_host, action)
    else:
        play(user_data_for_host, action[0])


pkill('-f', 'ssh-agent -s')
print('ssh-agent finished')
