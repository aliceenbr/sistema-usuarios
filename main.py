import json
import os
import hashlib
import re
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

ARQUIVO_DADOS = "usuarios.json"

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(senha, hash_banco):
    return criptografar_senha(senha) == hash_banco

def validar_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def email_existe(dados, email):
    return any(u["email"] == email for u in dados)

def validar_senha(senha):
    if len(senha) < 6:
        return False, "Senha deve ter pelo menos 6 caracteres"
    return True, ""

def limpar_campo(valor, nome_campo):
    valor = valor.strip()
    if not valor:
        raise ValueError(f"{nome_campo} nao pode estar vazio")
    return valor

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input(f"\n{Fore.CYAN}Pressione Enter para continuar...{Style.RESET_ALL}")

def cabecalho(titulo):
    print(f"\n{Fore.CYAN}{'═' * 45}")
    print(f"  {titulo}")
    print(f"{'═' * 45}{Style.RESET_ALL}")

def mensagem(tipo, texto):
    if tipo == "sucesso":
        print(f"{Fore.GREEN}✓ {texto}{Style.RESET_ALL}")
    elif tipo == "erro":
        print(f"{Fore.RED}✗ {texto}{Style.RESET_ALL}")
    elif tipo == "info":
        print(f"{Fore.YELLOW}ℹ {texto}{Style.RESET_ALL}")
    elif tipo == "alerta":
        print(f"{Fore.MAGENTA}⚠ {texto}{Style.RESET_ALL}")

def mostrar_banner():
    limpar_tela()
    print(f"""
{Fore.CYAN}╔{'═' * 43}╗
║{Fore.WHITE}       🔐 SISTEMA DE CADASTRO SEGuro 🔐      {Fore.CYAN}║
╚{'═' * 43}╝{Style.RESET_ALL}
""")

def mostrar_menu():
    print(f"""
{Fore.MAGENTA}╔{'═' * 43}╗
║{Fore.WHITE}              MENU PRINCIPAL              {Fore.MAGENTA}║
╠{'═' * 43}╣
║{Fore.WHITE}  [1] 📝 Cadastrar usuario                 {Fore.MAGENTA}║
║{Fore.WHITE}  [2] 📋 Listar usuarios                   {Fore.MAGENTA}║
║{Fore.WHITE}  [3] 🔍 Buscar usuario                    {Fore.MAGENTA}║
║{Fore.WHITE}  [4] ✏️  Atualizar usuario                 {Fore.MAGENTA}║
║{Fore.WHITE}  [5] 🗑️  Deletar usuario                   {Fore.MAGENTA}║
║{Fore.WHITE}  [6] 📊 Estatisticas                       {Fore.MAGENTA}║
║{Fore.WHITE}  [0] 🚪 Sair                               {Fore.MAGENTA}║
╚{'═' * 43}╝{Style.RESET_ALL}
""")

def cadastrar_usuario(dados):
    cabecalho("NOVO CADASTRO")
    
    try:
        nome = limpar_campo(input(f"{Fore.WHITE}Nome completo: {Style.RESET_ALL}"), "Nome")
        email = limpar_campo(input(f"{Fore.WHITE}Email: {Style.RESET_ALL}"), "Email")
        
        if not validar_email(email):
            mensagem("erro", "Email invalido! Formato: exemplo@email.com")
            return dados
        
        if email_existe(dados, email):
            mensagem("erro", "Este email ja esta cadastrado!")
            return dados
        
        senha = input(f"{Fore.WHITE}Senha: {Style.RESET_ALL}")
        valida, erro = validar_senha(senha)
        if not valida:
            mensagem("erro", erro)
            return dados
        
        usuario = {
            "id": len(dados) + 1,
            "nome": nome,
            "email": email,
            "senha": criptografar_senha(senha),
            "data_cadastro": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
        dados.append(usuario)
        salvar_dados(dados)
        mensagem("sucesso", f"Usuario '{nome}' cadastrado com sucesso!")
        
    except ValueError as e:
        mensagem("erro", str(e))
    
    pausar()
    return dados

def listar_usuarios(dados):
    cabecalho("LISTA DE USUARIOS")
    
    if not dados:
        mensagem("info", "Nenhum usuario cadastrado ainda.")
        pausar()
        return
    
    ordenar = input(f"{Fore.WHITE}Ordenar por nome? (s/n): {Style.RESET_ALL}").strip().lower()
    
    lista = dados.copy()
    if ordenar == 's':
        lista = sorted(lista, key=lambda x: x["nome"].lower())
    
    print(f"\n{Fore.GREEN}Total de usuarios: {len(lista)}{Style.RESET_ALL}\n")
    
    for i, u in enumerate(lista, 1):
        print(f"{Fore.CYAN}┌{'─' * 41}┐{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.WHITE} #{i}                                         {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.YELLOW}  Nome:   {u['nome']:<32}{Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.YELLOW}  Email:  {u['email']:<32}{Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.YELLOW}  Desde:  {u['data_cadastro']:<32}{Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}└{'─' * 41}┘{Style.RESET_ALL}\n")

def buscar_usuario(dados):
    cabecalho("BUSCAR USUARIO")
    
    termo = input(f"{Fore.WHITE}Digite nome ou email: {Style.RESET_ALL}").strip()
    
    if not termo:
        mensagem("erro", "Digite um termo de busca.")
        pausar()
        return
    
    resultados = [
        u for u in dados 
        if termo.lower() in u["nome"].lower() or termo.lower() in u["email"].lower()
    ]
    
    if resultados:
        print(f"\n{Fore.GREEN}Encontrados: {len(resultados)} resultado(s){Style.RESET_ALL}\n")
        for u in resultados:
            print(f"{Fore.CYAN}┌{'─' * 41}┐{Style.RESET_ALL}")
            print(f"{Fore.CYAN}│{Fore.YELLOW}  Nome:   {u['nome']:<32}{Fore.CYAN}│{Style.RESET_ALL}")
            print(f"{Fore.CYAN}│{Fore.YELLOW}  Email:  {u['email']:<32}{Fore.CYAN}│{Style.RESET_ALL}")
            print(f"{Fore.CYAN}│{Fore.YELLOW}  Desde:  {u['data_cadastro']:<32}{Fore.CYAN}│{Style.RESET_ALL}")
            print(f"{Fore.CYAN}└{'─' * 41}┘{Style.RESET_ALL}\n")
    else:
        mensagem("info", "Nenhum usuario encontrado.")
    
    pausar()

def atualizar_usuario(dados):
    cabecalho("ATUALIZAR USUARIO")
    
    if not dados:
        mensagem("info", "Nenhum usuario para atualizar.")
        pausar()
        return dados
    
    listar_usuarios(dados)
    email_busca = input(f"\n{Fore.WHITE}Digite o email do usuario: {Style.RESET_ALL}").strip()
    
    for u in dados:
        if u["email"] == email_busca:
            print(f"\n{Fore.GREEN}Editando: {u['nome']}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}(Deixe vazio para manter o valor atual){Style.RESET_ALL}\n")
            
            try:
                novo_nome = input(f"Novo nome [{u['nome']}]: ").strip() or u['nome']
                
                novo_email = input(f"Novo email [{u['email']}]: ").strip()
                if novo_email and novo_email != u['email']:
                    if not validar_email(novo_email):
                        mensagem("erro", "Email invalido!")
                        pausar()
                        return dados
                    if email_existe(dados, novo_email):
                        mensagem("erro", "Este email ja esta em uso!")
                        pausar()
                        return dados
                    u['email'] = novo_email
                
                nova_senha = input("Nova senha (deixe vazio): ").strip()
                if nova_senha:
                    valida, erro = validar_senha(nova_senha)
                    if not valida:
                        mensagem("erro", erro)
                        pausar()
                        return dados
                    u['senha'] = criptografar_senha(nova_senha)
                
                u['nome'] = novo_nome
                salvar_dados(dados)
                mensagem("sucesso", "Usuario atualizado com sucesso!")
                
            except Exception as e:
                mensagem("erro", f"Erro: {e}")
            
            pausar()
            return dados
    
    mensagem("erro", "Usuario nao encontrado.")
    pausar()
    return dados

def deletar_usuario(dados):
    cabecalho("DELETAR USUARIO")
    
    if not dados:
        mensagem("info", "Nenhum usuario para deletar.")
        pausar()
        return dados
    
    listar_usuarios(dados)
    email_busca = input(f"\n{Fore.WHITE}Digite o email do usuario: {Style.RESET_ALL}").strip()
    
    for i, u in enumerate(dados):
        if u["email"] == email_busca:
            mensagem("alerta", f"Voce esta preste a excluir: {u['nome']}")
            confirmacao = input(f"\n{Fore.RED}Confirmar exclusao? (s/n): {Style.RESET_ALL}").strip().lower()
            
            if confirmacao == "s":
                dados.pop(i)
                salvar_dados(dados)
                mensagem("sucesso", "Usuario excluido com sucesso!")
            else:
                mensagem("info", "Operacao cancelada.")
            
            pausar()
            return dados
    
    mensagem("erro", "Usuario nao encontrado.")
    pausar()
    return dados

def estatisticas(dados):
    cabecalho("ESTATISTICAS")
    
    print(f"{Fore.WHITE}Total de usuarios: {Fore.GREEN}{len(dados)}{Style.RESET_ALL}")
    
    if dados:
        nomes = [u['nome'].split()[0] for u in dados]
        mais_curto = min(nomes, key=len)
        mais_longo = max(nomes, key=len)
        print(f"Primeiro nome mais curto: {Fore.YELLOW}{mais_curto}{Style.RESET_ALL}")
        print(f"Primeiro nome mais longo: {Fore.YELLOW}{mais_longo}{Style.RESET_ALL}")
        
        emails_unicos = len(set(u['email'] for u in dados))
        print(f"Emails unicos: {Fore.GREEN}{emails_unicos}{Style.RESET_ALL}")
    
    pausar()

def login(dados):
    mostrar_banner()
    print(f"{Fore.CYAN}         🔒 AREA DE LOGIN 🔒{Style.RESET_ALL}\n")
    
    if not dados:
        mensagem("info", "Nenhum usuario cadastrado. Faca o primeiro cadastro!")
        email = input(f"\n{Fore.WHITE}Email: {Style.RESET_ALL}").strip()
        senha = input(f"{Fore.WHITE}Senha: {Style.RESET_ALL}")
        
        if not validar_email(email):
            mensagem("erro", "Email invalido!")
            return None
        
        valida, erro = validar_senha(senha)
        if not valida:
            mensagem("erro", erro)
            return None
        
        usuario = {
            "id": 1,
            "nome": "Admin",
            "email": email,
            "senha": criptografar_senha(senha),
            "data_cadastro": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        dados.append(usuario)
        salvar_dados(dados)
        mensagem("sucesso", "Conta criada com sucesso!")
        pausar()
        return dados
    
    max_tentativas = 3
    for tentativa in range(max_tentativas, 0, -1):
        email = input(f"{Fore.WHITE}Email: {Style.RESET_ALL}").strip()
        senha = input(f"{Fore.WHITE}Senha: {Style.RESET_ALL}")
        
        for u in dados:
            if u["email"] == email and verificar_senha(senha, u["senha"]):
                mensagem("sucesso", f"Bem-vindo(a), {u['nome']}!")
                return dados
        
        if tentativa > 1:
            mensagem("erro", f"Email ou senha incorretos. Tentativas restantes: {tentativa - 1}")
        else:
            mensagem("erro", "Limite de tentativas excedido.")
    
    return None

def menu_principal(dados):
    while True:
        mostrar_menu()
        opcao = input(f"{Fore.WHITE}Escolha uma opcao: {Style.RESET_ALL}").strip()
        
        if opcao == "1":
            dados = cadastrar_usuario(dados)
        elif opcao == "2":
            listar_usuarios(dados)
        elif opcao == "3":
            buscar_usuario(dados)
        elif opcao == "4":
            dados = atualizar_usuario(dados)
        elif opcao == "5":
            dados = deletar_usuario(dados)
        elif opcao == "6":
            estatisticas(dados)
        elif opcao == "0":
            print(f"\n{Fore.CYAN}Ate logo! :){Style.RESET_ALL}\n")
            break
        else:
            mensagem("erro", "Opcao invalida!")
            pausar()

def main():
    dados = carregar_dados()
    dados = login(dados)
    
    if dados is not None:
        menu_principal(dados)
    else:
        print(f"\n{Fore.RED}Sessao encerrada.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
