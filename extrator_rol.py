import os
import zipfile
import pandas as pd
import pdfplumber

def extrair_tabelas_pdf(caminho_pdf):
    # codigo usado para estrair dados do anexos_ans.zip
    print(f"Extraindo tabelas do arquivo: {caminho_pdf}")
    tabelas = []
    
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            for tabela in pagina.extract_tables():
                tabelas.append(pd.DataFrame(tabela))
    
    if not tabelas:
        print("Nenhuma tabela encontrada.")
        return pd.DataFrame()

    df = pd.concat(tabelas, ignore_index=True)
    return df.dropna(how="all")  

def substituir_abreviacoes(df):
    
    substituicoes = {"OD": "SEGMENTAÇÃO ASSISTENCIAL (Seg.)", "AMB": "PADRÃO DE UTILIZAÇÃO (PAD)"}
    df.rename(columns=substituicoes, inplace=True)
    return df

def compactar_arquivo(arquivo_csv, nome_zip):
    
    with zipfile.ZipFile(nome_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(arquivo_csv, os.path.basename(arquivo_csv))
    print(f"Arquivo compactado: {nome_zip}")

def main():
    pasta_anexos = "anexos_ans"
    pdfs = [f for f in os.listdir(pasta_anexos) if f.endswith(".pdf")]
    
    if not pdfs:
        print("Nenhum PDF encontrado na pasta.")
        return
    
    
    caminho_pdf = os.path.join(pasta_anexos, pdfs[0])
    df = extrair_tabelas_pdf(caminho_pdf)
    
    if df.empty:
        print("Nenhum dado extraído.")
        return
    
    df = substituir_abreviacoes(df)
    arquivo_csv = "rol_procedimentos.csv"
    df.to_csv(arquivo_csv, index=False, encoding="utf-8-sig")
    
    
    compactar_arquivo(arquivo_csv, f"Teste_{os.getlogin()}.zip")

if __name__ == "__main__":
    main()
