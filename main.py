import os

def executar_script(script):
    """Executa um script Python caso ele exista"""
    if os.path.exists(script):
        print(f"Executando {script}...\n")
        os.system(f"python {script}")
    else:
        print(f"Erro: O arquivo {script} não foi encontrado.")

def main():
    print("🚀 Iniciando o processo de web scraping e extração de dados...\n")
    
    # Passo 1: Baixar os PDFs
    executar_script("script.py")

    # Passo 2: Extrair as tabelas dos PDFs
    executar_script("extrair.py")

    print("\n✅ Processo concluído!")

if __name__ == "__main__":
    main()
