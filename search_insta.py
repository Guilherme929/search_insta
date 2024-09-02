#!/usr/bin/env python3
import requests
import sys

def get_csrftoken():
    url = 'https://instagram.com/'

    r = requests.get(url)

    csrftoken = r.cookies.get('csrftoken')
    if not csrftoken:
        print("Não foi possível obter o csrftoken.")
    return csrftoken

def search_instagram_user(name, cookies):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": cookies.get('csrftoken')
    }
    query_url = f"https://www.instagram.com/web/search/topsearch/?query={name}"
    
    try:
        response = requests.get(query_url, headers=headers, cookies=cookies)
        response.raise_for_status()

        try:
            data = response.json()
        except ValueError as e:
            print(f"Erro ao decodificar JSON: {e}")
            print("Conteúdo da resposta:", response.text)
            return


        users = data.get('users', [])
        if not users:
            print("Nenhum usuário encontrado.")
            return

        for user in users:
            user_data = user['user']
            username = user_data['username']
            full_name = user_data.get('full_name', 'N/A')
            profile_link = f"https://www.instagram.com/{username}/"
            profile_pic_url = user_data.get('profile_pic_url', 'N/A')
            social_context = user.get('social_context', 'Não há informação da cidade/bairro.')

            print(f"Username: {username}\n")
            print(f"Nome Completo: {full_name}\n")
            print(f"Link: {profile_link}\n")
            print(f"Foto do Perfil: {profile_pic_url}\n")
            print(f"Informações Extra: {social_context}\n")
            print('-' * 60)
        
    except requests.RequestException as e:
        print("Erro ao buscar usuário:", e)

if __name__ == '__main__':
    print('''
  ____        _         _     _____              _          __      ___
 / __ \      (_)       | |   |_   _|            | |         \ \    |  _|
| |  | | ___  _  _ __  | |_    | |   _ __   ___ | |_   __ _  \ \   | |
| |  | |/ __|| || '_ \ | __|   | |  | '_ \ / __|| __| / _` |  \ \  | |
| |__| |\__ \| || | | || |_   _| |_ | | | |\__ \| |_ | (_| |   \ \ | |
 \____/ |___/|_||_| |_| \__| |_____||_| |_||___/ \__| \__,_|    \_\| |_
                                                                   |___|
                                                by_name: {https://github.com/Guilherme929}
''')

    if len(sys.argv) != 2:
        print('Uso: search_insta <NOME>')
        sys.exit()

    nome = sys.argv[1]
    csrftoken_value = get_csrftoken()
    cookies = {
        "sessionid": "seu_id_meunobre",
        "csrftoken": csrftoken_value
    }

    search_instagram_user(nome, cookies)
