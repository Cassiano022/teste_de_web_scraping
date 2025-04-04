import os
import requests
from bs4 import BeautifulSoup
import zipfile
import re
from urllib.parse import urljoin

def create_directory(directory):
    #codigo usado para acessar o site, e extrair os pdf
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Diretório '{directory}' criado com sucesso.")
    return directory

def download_file(url, save_path):
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  
        
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        print(f"Arquivo baixado com sucesso: {save_path}")
        return True
    except Exception as e:
        print(f"Erro ao baixar o arquivo {url}: {str(e)}")
        return False

def compress_files(files_to_compress, output_zip_path):
    
    try:
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files_to_compress:
                if os.path.exists(file):
                    zipf.write(file, os.path.basename(file))
                    print(f"Arquivo {file} adicionado ao ZIP.")
                else:
                    print(f"Arquivo {file} não encontrado.")
        print(f"Arquivos compactados com sucesso em: {output_zip_path}")
        return True
    except Exception as e:
        print(f"Erro ao compactar os arquivos: {str(e)}")
        return False

def main():
    
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    print(f"Acessando o site: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        
        download_dir = create_directory("anexos_ans")
        
        
        downloaded_files = []
        
        
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            text = link.get_text().lower()
            
            
            if ('anexo i' in text or 'anexo ii' in text) and '.pdf' in href:
                
                if not href.startswith(('http://', 'https://')):
                    href = urljoin(url, href)
                
                
                filename = os.path.basename(href)
                if not filename or not filename.endswith('.pdf'):
                    
                    clean_text = re.sub(r'[^a-zA-Z0-9]', '_', text)
                    filename = f"{clean_text}.pdf"
                
                file_path = os.path.join(download_dir, filename)
                
                
                if download_file(href, file_path):
                    downloaded_files.append(file_path)
                    print(f"Anexo encontrado e baixado: {text} -> {filename}")
        
        
        if len(downloaded_files) < 2:
            print("Poucos anexos encontrados. Tentando busca alternativa...")
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                text = link.get_text().lower()
                
                
                if 'anexo' in text and '.pdf' in href:
                    if not href.startswith(('http://', 'https://')):
                        href = urljoin(url, href)
                    
                    filename = os.path.basename(href)
                    if not filename or not filename.endswith('.pdf'):
                        clean_text = re.sub(r'[^a-zA-Z0-9]', '_', text)
                        filename = f"{clean_text}.pdf"
                    
                    file_path = os.path.join(download_dir, filename)
                    
                    if file_path not in downloaded_files and download_file(href, file_path):
                        downloaded_files.append(file_path)
                        print(f"Anexo adicional encontrado e baixado: {text} -> {filename}")
        
        
        if downloaded_files:
            zip_path = "anexos_ans.zip"
            if compress_files(downloaded_files, zip_path):
                print(f"\nProcesso concluído com sucesso!")
                print(f"Total de arquivos baixados: {len(downloaded_files)}")
                print(f"Arquivos compactados em: {zip_path}")
            else:
                print("Falha ao compactar os arquivos.")
        else:
            print("Nenhum anexo foi encontrado para download.")
            
    except Exception as e:
        print(f"Erro ao acessar o site: {str(e)}")

if __name__ == "__main__":
    main()
    
    #comando python script.py o terminal 