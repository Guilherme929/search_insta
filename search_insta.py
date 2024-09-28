#!/usr/bin/env python3

"""Recomendo que crie uma conta de teste, para sua conta pessoal não ser banida!"""

import requests
import os
import sys
import random
import json
from time import sleep
import banner
import instaloader
import logs

class OsintInstagram: 
    """Aqui estou passando uns valores de cores"""
    def __init__(self):
        self.RESET = "\033[0m"
        self.GREEN = "\033[32m"
        self.BOLD = "\033[1m"
        self.BRANCO = '\033[37m'
        self.VERMELHO = "\033[91m"
        self.AMARELO_BRILHANTE = "\033[93m"

    def apagando_proxy_velho(self, file):
        """Aqui essa função irá apagar o arquivo dos proxies"""
        if os.path.exists(file):
            os.remove(file)
            sleep(3)

    def gerando_proxies(self, file):
        """Aqui essa função irá pegar proxies da página JSON."""
        url = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=protocolipport&format=json&timeout=20000"
        response = requests.get(url)

        try:
            response.raise_for_status()
            estrair_proxies = response.json()
            coluna = estrair_proxies.get("proxies")

            if not coluna:
                print(f"{self.VERMELHO}Erro ao obter proxies: chave 'proxies' não encontrada.{self.RESET}")
                return

            os.makedirs(os.path.dirname(file), exist_ok=True)

            with open(file, "a") as f:
                for proxies in coluna:
                    proxy = proxies["proxy"]
                    f.write(f"{proxy}\n")
        except requests.RequestException as e:
            print(f"{self.VERMELHO}Erro ao obter proxies: {e}{self.RESET}")
        except json.JSONDecodeError:
            print(f"{self.VERMELHO}Erro ao decodificar JSON.{self.RESET}")

    def carregar_proxies(self, proxy):
        try:
            proxies = []
            with open(proxy, 'r') as file:
                for line in file:
                    linha = line.strip()
                    if linha:
                        proxies.append(linha)
            return proxies
        except :
            print(f'{self.BOLD}Não tem o arquivo dos proxies, para obter digite: search_insta -a{self.RESET}')
            sys.exit(0)

    """Aqui essa função irá guardar informações """
    def guarda_informacao_conta(self, informacao, diretorio):
        caminho_arquivo = os.path.join("OsintInfo", f"{diretorio}.txt")
        os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

        if not isinstance(informacao, str):
            with open(caminho_arquivo, 'a') as file:
                file.write(caminho_arquivo)  

        print(f"Informação armazenada com sucesso em: {caminho_arquivo}")



    def baixar_img_jpg(self, link, nome_pasta, nome_imagem):
        """Essa função detecta se o link é uma imagem e guarda em um arquivo na pasta do usuário."""
        resposta = requests.get(link)
        resposta.raise_for_status()

        if "image" not in resposta.headers["Content-Type"]:
            print('Link fornecido não é uma imagem.')
            return

        destino = f'OsintFoto/{nome_pasta}/{nome_imagem}'
        os.makedirs(destino, exist_ok=True)

        arquivo_img = os.path.join(destino, f'{nome_imagem}.jpg')

        if os.path.exists(arquivo_img):
            return

        with open(arquivo_img, 'wb') as file:
            file.write(resposta.content)


    def salvar_credenciais(self, username, session_id, csrftoken, file="credenciais.json"):
        credenciais = {}
        
        if os.path.exists(f"SearchInsta/OsintInsta/{file}"):
            with open(f"SearchInsta/OsintInsta/{file}", 'r') as f:
                credenciais = json.load(f)

        credenciais[username] = {
            'session_id': session_id,
            'csrftoken': csrftoken
        }

        caminho_arquivo = f"SearchInsta/OsintInsta/{file}"
        os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
        
        with open(caminho_arquivo, 'w') as f:
            json.dump(credenciais, f)



    def carregar_credenciais(self, username, file='credenciais.json'):
        if os.path.exists(f"SearchInsta/OsintInsta/{file}"):
            with open(f"SearchInsta/OsintInsta/{file}", 'r') as f:
                credenciais = json.load(f)
            
            if username in credenciais:
                return credenciais[username]["session_id"], credenciais[username]["csrftoken"]

        print(f"Nenhuma credencial encontrada para {username}.")
        return None, None


    def get_csrftoken(self):
        """Obter csrftoken"""
        url = 'https://www.instagram.com/'
        r = requests.get(url)
        csrftoken = r.cookies.get('csrftoken')
        if not csrftoken:
            print(f"{self.BOLD}[{self.VERMELHO + self.BOLD}!{self.RESET + self.BOLD}]{self.RESET + self.BOLD}Não foi possível obter o csrftoken.{self.RESET}")
        return csrftoken

    def login_instagram(self, username, password, arquivo_credenciais="credenciais.json"):
        """Fazer login no Instagram e salvar as credenciais"""

        session_id, csrftoken = self.carregar_credenciais(username, arquivo_credenciais)
        
        if session_id and csrftoken:
            print(f'{self.BOLD + self.GREEN}[{self.BOLD}+{self.RESET + self.BOLD + self.GREEN}]{self.RESET} {self.BOLD}Usando credenciais salvas.{self.RESET}')
            return session_id, csrftoken

        print('Fazendo login para {}'.format(username))
        login_url = 'https://www.instagram.com/accounts/login/ajax/'
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "X-CSRFToken": self.get_csrftoken(),
            "Referer": "https://www.instagram.com/accounts/login/"
        }

        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:0:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        with requests.Session() as session:
            try:
                response = session.post(login_url, data=payload, headers=headers)
                response.raise_for_status()

                response_data = response.json()

                if response_data.get('authenticated'):
                    self.salvar_credenciais(username, session.cookies.get('sessionid'), headers["X-CSRFToken"])
                    print(f'{self.BOLD + self.GREEN}[{self.BOLD}+{self.RESET + self.BOLD + self.GREEN}]{self.RESET} {self.BOLD}Login bem-sucedido!{self.RESET}')
                    return session.cookies.get('sessionid'), headers["X-CSRFToken"]
                else:
                    print(f"{self.VERMELHO}Falha no login. Verifique suas credenciais.{self.RESET}")
                    return None, None
            except requests.RequestException as e:
                print(f"{self.VERMELHO + self.BOLD}Erro na requisição: {e}{self.RESET}\n")
                return None, None
            except json.JSONDecodeError:
                print(f"{self.VERMELHO}Erro ao fazer login. Resposta não é um JSON válido: {response.text}{self.RESET}")
                return None, None


    def search_instagram_user(self, name, session_id, csrftoken, name_fotos, proxies=None):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrftoken
        }

        cookies = {
            "sessionid": session_id,
            "csrftoken": csrftoken
        }

        if proxies:
            proxy_dinamico = random.choice(proxies)
            variavel = {
                "http": f"{proxy_dinamico}"
            }
            print(f'Usando proxy: {variavel}')
        else:
            variavel = None

        query_url = f"https://www.instagram.com/web/search/topsearch/?query={name}"
        
        try:
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
                self.baixar_img_jpg(profile_pic_url, name_fotos, username)

                """Aqui estou chamando o instaloader para complementar as informações."""

                l = instaloader.Instaloader()

                try:
                    perfil = instaloader.Profile.from_username(l.context, username)
                    bio = perfil.biography
                    seguindo = perfil.followees
                    seguidores = perfil.followers
                except instaloader.exceptions.ProfileNotExistsException:
                    bio = "N/A"
                    print('Perfil não encontrado via instaloader.')

                print(f"Username: {username}\n")
                print(f"Nome Completo: {full_name}\n")
                print(f"Link: {profile_link}\n")
                print(f"Foto do Perfil: {profile_pic_url}\n")
                print(f"Status da conta: {'Privado' if status_publico else 'Público'}")
                print(f'Seguindo: {seguindo}')
                print(f'seguidores: {seguidores}')
                print(f'Bio: {bio}')
                print(f"Cidade: {social_context}")
                print('-' * 60)

                """Gerando relatorio de informações"""

                profile = {f"""
Name: {username}
Nome Completo: {full_name}
Link: {profile_link}
Foto De perfil: {profile_pic_url}
Seguindo: {seguindo}
Seguidores: {seguidores}
Cidade: {social_context}
Bio: {bio}
"""}
                self.guarda_informacao_conta(profile, username)


        except requests.exceptions.RequestException as e:
            print(f"Erro durante a requisição: {str(e)}")


        except requests.RequestException as e:
            print("Erro ao buscar usuário:", e)

        except requests.RequestException as e:
            print("Erro ao buscar usuário:", e)

    def search_expecifico_instagram_anonimous(self, nome):
        """Buscar por uma conta específica de forma anônima"""
        loader = instaloader.Instaloader()
        
        profile = instaloader.Profile.from_username(loader.context, nome)

        try:
            bio = profile.biography
            nome = profile.username
            foto = profile.profile_pic_url
            seguidores = profile.followers
            seguindo = profile.followees 
        except instaloader.exceptions.ProfileNotExistsException:
            bio = "N/A"
            nome = "N/A"
            foto = "N/A"
            seguidores = "N/A"
            seguindo = "N/A" 
            print('Perfil não encotrado via instaloader.')


        if profile:
            print(f"{self.BOLD + self.GREEN}Username{self.RESET}: {profile.full_name}\n")
            print(f"{self.BOLD + self.GREEN}Nome{self.RESET}: {nome}\n")
            print(f'{self.BOLD + self.GREEN}Bio{self.RESET}: {bio}\n')
            print(f'{self.BOLD + self.GREEN}Foto{self.RESET}: {foto}')
            print(f'{self.BOLD + self.GREEN}Seguidores(a){self.RESET}: {seguidores}')
            print(f'{self.BOLD + self.GREEN}Seguindo-(a):{self.RESET}: {seguindo}')
            print(f'')
            print('-' * 50)
        elif instaloader.exceptions in profile:
            print('Ocorreu um erro!')
        
        profile_file = f"""
Name: {profile.username}\n
Nome Completo: {profile.full_name}\n
Link: {profile.profile_pic_url}\n
Foto De perfil: {profile.profile_pic_url}\n
Seguindo: {profile.followers}\n
Seguidores: {profile.followees}\n
Cidade: {profile.has_viewable_story}\n
Bio: {profile.biography}\n
        """
        self.guarda_informacao_conta(profile_file, nome)
        sys.exit(0)


    def help(self):
        print("""
Essa ferramenta é uma ferramenta de OSINT no Instagram. Recomenda-se criar uma conta nova para evitar problemas com sua conta pessoal.

Essa ferramenta consiste em buscar informações sobre uma conta, como status social da conta, foto, cidade, nome.

Como usar:
        searchinsta <usuario> <senha>

Exemplo:
        searchinsta exemple123@gmail.com teste.123

Outros:
        -a, --atualizar: Atualiza os proxies da ferramenta!
        -p, --proxy: Utiliza proxies para buscar informações do usuário
        -h, --help: Exibe essa ajuda
        -e, --expecifico: Busca por um usuário específico
        """)

if __name__ == '__main__':
    osint = OsintInstagram()
    banner.banner_search_insta()

    ARQUIVO_PROXY = "SearchInsta/OsintInsta/proxies.txt"
    ARQUIVO_LOGS = "SearchInsta/OsintInsta/logs.txt"

    if "-a" in sys.argv or "--atualizar" in sys.argv:
        print(f'{osint.BOLD}{osint.GREEN}[{osint.RESET}{osint.BOLD}{osint.BRANCO}+{osint.RESET}{osint.BOLD}{osint.GREEN}]{osint.RESET}{osint.BOLD} Atualizando proxy!{osint.RESET}')
        osint.apagando_proxy_velho(ARQUIVO_PROXY)
        osint.gerando_proxies(ARQUIVO_PROXY)
        logs.logs_insta("Usuário atualizou os proxies da ferramenta.", ARQUIVO_LOGS)
        sleep(3)
    
    if "-h" in sys.argv:
        osint.help()
        sys.exit(0)

    if len(sys.argv) < 3:
        print('Uso: searchinsta <NOME> <SENHA>')
        print('Ou digite: -h para mais informações!')
        logs.logs_insta("Erro nos argumentos: número insuficiente.", ARQUIVO_LOGS)
        sys.exit(2)

    if '-e' in sys.argv or '--expecifico' in sys.argv:
        osint.search_expecifico_instagram_anonimous(sys.argv[2])
        sys.exit(0)

    username = sys.argv[1]
    password = sys.argv[2] 

    try:
        session_id, csrftoken = osint.login_instagram(username, password)
    except Exception as error:
        print('Erro ao fazer login: {}'.format(error))


    if session_id:
        if "-p" in sys.argv or "--proxy" in sys.argv:
            ler_proxy = ARQUIVO_PROXY
            logs.logs_insta("Usuário optou por usar proxies da ferramenta.", ARQUIVO_LOGS)
        else:
            ler_proxy = None
            logs.logs_insta("Usuário não optou por usar proxies da ferramenta.", ARQUIVO_LOGS)

        nome_usuario = input("Digite um nome de usuário: ")
        if nome_usuario:
            osint.search_instagram_user(nome_usuario, session_id, csrftoken, nome_usuario, ler_proxy)
        else:
            print("Nome de usuário não pode ser vazio!")
            logs.logs_insta("Nome de usuário não pode ser vazio.", ARQUIVO_LOGS)
    else:
        print(f"{osint.BOLD}[{osint.VERMELHO + osint.BOLD}!{osint.RESET + osint.BOLD}]{osint.RESET + osint.BOLD} Não foi possível obter o session-id.{osint.RESET}")
        logs.logs_insta("Não foi possível obter session-id após a tentativa de login.", ARQUIVO_LOGS)
