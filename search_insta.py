#!/usr/bin/env python3
import requests
import sys

def search_instagram_user(name, cookies):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "X-Requested-With": "XMLHttpRequest",
    }
    query_url = f"https://www.instagram.com/web/search/topsearch/?query={name}"
    
    response = requests.get(query_url, headers=headers, cookies=cookies)
    
    if response.status_code == 200:
        users = response.json().get('users', [])
        for user in users:
            username = user['user']['username']
            full_name = user['user']['full_name']
            profile_link = f"https://www.instagram.com/{username}/"
            print(f"Username: {username}, sobrenome: {full_name}")
            print(f"Link: {profile_link}")
            print('-' * 40)
    else:
        print("Erro ao buscar usuário:", response.status_code)


cookies = {
    "sessionid": "seu_id_meunobre",
    "csrftoken": "seu_token_meunobre",    
}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('search_insta <NOME>')
        sys.exit()

    nome = sys.argv[1]
    search_instagram_user(nome, cookies)
