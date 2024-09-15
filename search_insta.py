"""Recomendo que crie uma conta de teste, para sua conta não ser banida!"""
#!/usr/bin/env python3
import requests
import os
import sys
import random
import banner

RESET = "\033[0m"
GREEN = "\033[32m"
BOLD = "\033[1m"
BRANCO = '\033[37m'
VERMELHO = "\033[91m"
AMARELO_BRILHANTE = "\033[93m"

def apagando_proxy_velho(file):
    if os.path.exists("proxies.txt"):
        os.remove(file)
        sleep(3)

def gerando_proxies(file):
    url = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=protocolipport&format=json&timeout=20000"
    response = requests.get(url)

    estrair_proxies = response.json()

    coluna = estrair_proxies.get("proxies")
    if not os.path.exists(file):
        if response.status_code == 200:
            for proxies in coluna:
                proxy = proxies["proxy"]
                with open(file, "a") as f:
                    f.write(f"{proxy}\n")

            

def carregando_proxies(proxy):
    proxies = []
    with open(proxy, 'r') as file:
        for line in file:
            linha = line.strip()
            if linha:
                proxies.append(linha)
    return proxies

def get_csrftoken():
    url = 'https://www.instagram.com/'
    r = requests.get(url)
    csrftoken = r.cookies.get('csrftoken')
    if not csrftoken:
        print("Não foi possível obter o csrftoken.")
    return csrftoken

def login_instagram(username, password):
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "X-CSRFToken": get_csrftoken(),
        "Referer": "https://www.instagram.com/accounts/login/"
    }

    payload = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:0:{password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }

    with requests.Session() as session:
        response = session.post(login_url, data=payload, headers=headers)
        
        if response.status_code == 200 and response.json().get('authenticated'):
            print("Login bem-sucedido!")
            session_id = session.cookies.get('sessionid')
            csrftoken = session.cookies.get('csrftoken')
            return session_id, csrftoken
        else:
            print("Falha no login:", response.text)
            return None, None

def search_instagram_user(name, session_id, csrftoken, proxies):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrftoken
    }

    cookies = {
        "sessionid": session_id,
        "csrftoken": csrftoken
    }

    proxy = carregando_proxies(proxies)
    proxy_dinanmico = random.choice(proxy)

    variavel = {
        "http": f"{proxy_dinanmico}"
    }
    
    query_url = f"https://www.instagram.com/web/search/topsearch/?query={name}"
    
    try:
        if variavel['http']:
            print('Usando proxy: {}'.format(variavel))
            print('-' * 40)
            print('\n')
        else:
            print('O proxy não é funcional!')
            
        response = requests.get(query_url, headers=headers, cookies=cookies, proxies=variavel, timeout=5)
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
            status_publico = user_data['is_private']
            full_name = user_data.get('full_name', 'N/A')
            profile_link = f"https://www.instagram.com/{username}/"
            profile_pic_url = user_data.get('profile_pic_url', 'N/A')
            social_context = user.get('social_context', 'Não há informações sobre localização!')

            print(f"Username: {username}\n")
            print(f"Nome Completo: {full_name}\n")
            print(f"Link: {profile_link}\n")
            print(f"Foto do Perfil: {profile_pic_url}\n")
            print(f"Status da conta: {'Privado' if status_publico else 'Público'}")
            print(f"Cidade: {social_context}")
            print('-' * 60)

    except requests.RequestException as e:
        print("Erro ao buscar usuário:", e)

if __name__ == '__main__':
    banner.banner_search_insta()
    """Essa função gerará um arquico com proxies http"""
    from time import sleep
    print(f'{BOLD}{GREEN}[{RESET}{BOLD}{BRANCO}+{RESET}{BOLD}{GREEN}]{RESET}{BOLD} Atualizando proxy!{RESET}')
    arquivo = "proxies.txt"
    apagando_proxy_velho(arquivo)
    gerando_proxies(arquivo)
    sleep(3)

    """Essa parte é a parte de argumentos"""    
    if len(sys.argv) != 3:
        print('Uso: search_insta <NOME> <SENHA>') # Obs: Você devera colocar suas credenciais.
        sys.exit()

    username = sys.argv[1]
    password = sys.argv[2]

    session_id, csrftoken = login_instagram(username, password)

    
    if session_id:
        ler_proxies = "proxies.txt"
        nome_usuario = input("Digite o nome do usuário para pesquisar: ")
        search_instagram_user(nome_usuario, session_id, csrftoken, ler_proxies)
    else:
        print("Não foi possível obter o session-id.")
