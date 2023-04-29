import os
import time
import pikepdf
from tqdm import tqdm
from termcolor import colored
import pyfiglet


REQUIRED_MODULES = {
    'pikepdf': 'pip install pikepdf -q -q -q',
    'tqdm': 'pip install tqdm -q -q -q',
    'termcolor': 'pip install termcolor -q -q -q',
    'pyfiglet': 'pip install pyfiglet -q -q -q',
}

def check_requirements():
    print("[*] Checking required modules...")
    for module_name, install_command in REQUIRED_MODULES.items():
        try:
            __import__(module_name)
        except ImportError:
            os.system(install_command)
    print("[*] All required modules are installed.")

def print_header():
    ascii_banner = pyfiglet.figlet_format("{PDF CRACKER}").upper()
    print(colored(ascii_banner.rstrip("\n"), 'cyan', attrs=['bold']))
    print(colored("                                Coded By Gus     \n", 'yellow', attrs=['bold']))
    print(colored("                                Version 1.0     \n", 'magenta', attrs=['bold']))

def crack_pdf():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_header()

    while True:
        pdf_filename = input(colored("[*] Enter path of your PDF file: ", 'cyan'))
        if not os.path.exists(pdf_filename):
            print(colored("\n[ X ] File " + pdf_filename + " was not found, provide a valid filename and path!", 'red'))
        elif not pdf_filename.endswith(".pdf"):
            print(colored("\n[ X ] This is not a valid PDF file.", 'red'))
        else:
            break

    print(colored("\n[*] Analyzing PDF file:", 'blue'), pdf_filename)
    time.sleep(1)

    while True:
        pwd_filename = input(colored("\nEnter path of your wordlist: ", 'yellow'))
        if not os.path.exists(pwd_filename):
            print(colored("\n[ X ] File " + pwd_filename + " was not found, provide a valid filename and path!", 'red'))
        else:
            break

    with open(pwd_filename, 'r', encoding='utf-8') as f:
        passwords = [line.strip() for line in f]

    user_pwd_found = False
    owner_pwd_found = False
    for password in tqdm(passwords, desc=f"Cracking PDF file {pdf_filename}", unit="password"):
        try:
            with pikepdf.open(pdf_filename, password=password) as pdf:
                if pdf.is_encrypted:
                    if pdf.encryption["/Filter"] == "/Standard":
                        user_pwd_found = True
                    else:
                        owner_pwd_found = True
                print(colored("\n[ ✔ ] PDF file password found:", 'cyan'), password)
                if owner_pwd_found:
                    print(colored("\n[ ! ] PDF file is encrypted with an owner password, some operations may be restricted.", 'yellow'))
                return
        except pikepdf._qpdf.PasswordError:
            continue

    if not user_pwd_found and not owner_pwd_found:
        print(colored("\n[ X ] No password found.", 'red'))

def main():
    check_requirements()
    crack_pdf()

if __name__ == '__main__':
    main()
