import os
import argparse
import threading
from banners import banners
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from colorama import Fore, Style
import random
import datetime

def print_banner():
    chosen_banner = random.choice(banners)
    print(f"{Fore.BLUE}")
    print(chosen_banner)
    print(Style.RESET_ALL)
    print("Screen and Code font Capture")
    print("Made by: Domingos Toko Muanda alias @KellyBlue :)")

current = datetime.datetime.now()
current_time = f'[{current:%d/%m/%Y %H:%M:%S}]'

def get_page_source(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"{Fore.BLUE}{current_time}{Style.RESET_ALL}{Fore.RED} [ERROR] Erro ao obter {url}. Código de resposta: {response.status_code}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.BLUE}{current_time}{Style.RESET_ALL}{Fore.RED} [ERROR] Ocorreu um erro ao processar {url}: {e}{Style.RESET_ALL}")

def save_page_source(url, page_source, output_folder):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        file_path = os.path.join(output_folder, f"{url.replace('http://', '').replace('https://', '').replace('/', '_')}_source.html")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(page_source)

        print(f"{Fore.BLUE}{current_time}{Style.RESET_ALL}{Fore.YELLOW} [NOTICE]{Style.RESET_ALL}{Fore.GREEN} Código-fonte para {url} salvo em {file_path}{Style.RESET_ALL}", end='\n')
    except Exception as e:
        print(f"{Fore.BLUE}{current_time}{Style.RESET_ALL}{Fore.RED} [ERROR] Ocorreu um erro ao salvar o código-fonte de {url}: {e}{Style.RESET_ALL}", end='\n')

def take_screenshot(url, output_folder):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--remote-debugging-port=0")  # Impede a exibição do DevTools
        chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)

        screenshot_path = os.path.join(output_folder, f"{url.replace('http://', '').replace('https://', '').replace('/', '_')}_screenshot.png")
        driver.save_screenshot(screenshot_path)

        print(f"{Fore.BLUE}{current_time}{Style.RESET_ALL}{Fore.YELLOW} [NOTICE] Screenshot para {url} salvo em {screenshot_path}{Style.RESET_ALL}", end='\n')

    except Exception as e:
        print(f"{Fore.BLUE}{current_time}{Style.RESET_ALL}{Fore.RED} [ERROR] Ocorreu um erro ao processar {url}: {e}{Style.RESET_ALL}", end='\n')

    finally:
        driver.quit()

def process_url(url, output_folder):
    print(f"{Fore.BLUE}{current_time}{Style.RESET_ALL}{Fore.YELLOW} [WARNING]{Style.RESET_ALL}{Fore.CYAN} Processando {url}{Style.RESET_ALL}", end='\n')

    page_source = get_page_source(url)

    if page_source:
        save_page_source(url, page_source, output_folder)
        take_screenshot(url, output_folder)

def main():
    parser = argparse.ArgumentParser(description="Ferramenta para capturar screenshots e código-fonte de URLs.")
    parser.add_argument('-w', '--wordlist', required=True, help="Caminho para a wordlist de URLs.")
    parser.add_argument('-o', '--output', default="output", help="Caminho para o diretório de saída (padrão: output).")

    args = parser.parse_args()

    # Verificar se o diretório de saída foi fornecido
    if not args.output:
        output_folder = "output"
    else:
        output_folder = os.path.expanduser(args.output)

    if not os.path.exists(args.wordlist):
        print(f"{Fore.BLUE}{current_time}{Style.RESET_ALL}{Fore.RED} [ERROR] A wordlist '{args.wordlist}' não foi encontrada ou não existe.{Style.RESET_ALL}")
        return

    with open(args.wordlist, 'r') as file:
        urls = file.read().splitlines()

    threads = []

    for url in urls:
        thread = threading.Thread(target=process_url, args=(url, output_folder))
        threads.append(thread)
        thread.start()

    # Aguardar todas as threads terminarem
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    print_banner()
    main()
