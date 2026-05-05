from tkinter import Tk, Label, Button, filedialog
import os
import subprocess
from PIL import Image, ImageTk  # Importar a biblioteca PIL para a conversão de imagens

# Variáveis globais para armazenar os caminhos das pastas
pasta_entrada = None
pasta_saida = None

# Função para escolher a pasta de entrada
def escolher_pasta_entrada():
    global pasta_entrada  # Usar a variável global
    caminho_entrada = filedialog.askdirectory(title="Escolher Pasta de Entrada")
    if caminho_entrada:
        pasta_entrada = caminho_entrada  # Armazenar o caminho na variável global
        pasta_entrada_nome = os.path.basename(caminho_entrada)  # Extrai o nome da pasta
        print(f"Pasta de entrada escolhida: {caminho_entrada}")  # Mensagem de depuração
        label_pasta_entrada.config(text=f"Pasta de entrada escolhida: {pasta_entrada_nome}")
    else:
        print("Erro: Nenhuma pasta de entrada foi selecionada.")
        label_pasta_entrada.config(text="Erro ao escolher a pasta de entrada.")

# Função para escolher a pasta de saída
def escolher_pasta_saida():
    global pasta_saida  # Usar a variável global
    caminho_saida = filedialog.askdirectory(title="Escolher Pasta de Saída")
    if caminho_saida:
        pasta_saida = caminho_saida  # Armazenar o caminho na variável global
        pasta_saida_nome = os.path.basename(caminho_saida)  # Extrai o nome da pasta
        print(f"Pasta de saída escolhida: {caminho_saida}")  # Mensagem de depuração
        label_pasta_saida.config(text=f"Pasta de saída escolhida: {pasta_saida_nome}")
    else:
        print("Erro: Nenhuma pasta de saída foi selecionada.")
        label_pasta_saida.config(text="Erro ao escolher a pasta de saída.")

# Função para realizar a conversão
def converter_para_pdf():
    print("Convertendo imagens para PDF...")

    if pasta_entrada and pasta_saida:
        # Obter as imagens da pasta de entrada, incluindo arquivos .jfif
        imagens = [f for f in os.listdir(pasta_entrada) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.jfif'))]
        
        if imagens:
            for img_name in imagens:
                # Criar um PDF para cada imagem individualmente
                img_path = os.path.join(pasta_entrada, img_name)
                img = Image.open(img_path)
                img = img.convert("RGB")  # Convertendo para RGB se necessário

                # Gerar o caminho do PDF
                pdf_path = os.path.join(pasta_saida, f"{os.path.splitext(img_name)[0]}.pdf")

                # Salvar a imagem como PDF
                img.save(pdf_path, "PDF")
                print(f"PDF criado para {img_name}: {pdf_path}")

            # Atualiza o status na interface
            label_status.config(text=f"Conversão concluída com sucesso! PDFs salvos em: {pasta_saida}")

            # **Aqui é a modificação para garantir que a pasta certa seja aberta**
            pasta_saida_absoluta = os.path.abspath(pasta_saida)  # Garantir que o caminho seja absoluto
            print(f"Abrindo a pasta de saída: {pasta_saida_absoluta}")  # Mensagem de depuração
            
            # Abrir a pasta de saída automaticamente
            subprocess.Popen(f'explorer "{pasta_saida_absoluta}"')  # Abre a pasta no Windows
        else:
            print("Não há imagens válidas na pasta de entrada.")
            label_status.config(text="Nenhuma imagem encontrada na pasta de entrada.")
    else:
        label_status.config(text="Erro ao selecionar pastas.")

# Criando a janela principal
root = Tk()
root.title("Conversor Universal para PDF")

# Estilo da Janela
root.geometry("600x500")  # Tamanho da janela
root.config(bg="#2e2e2e")  # Cor de fundo escura

# Ícone da Janela (opcional, caso queira colocar um ícone de aplicativo)
# root.iconbitmap('icon.ico')  # Substitua 'icon.ico' pelo caminho do seu ícone

# Labels para mostrar as pastas
label_pasta_entrada = Label(root, text="Escolha a pasta de entrada", fg="white", bg="#2e2e2e", font=("Arial", 14, "bold"))
label_pasta_entrada.pack(pady=15)

label_pasta_saida = Label(root, text="Escolha a pasta de saída", fg="white", bg="#2e2e2e", font=("Arial", 14, "bold"))
label_pasta_saida.pack(pady=15)

# Botões para escolher as pastas
button_entrada = Button(root, text="Escolher Pasta de Entrada", command=escolher_pasta_entrada, fg="white", bg="dodgerblue", font=("Arial", 12, "bold"), relief="solid", bd=2, width=25)
button_entrada.pack(pady=15)

button_saida = Button(root, text="Escolher Pasta de Saída", command=escolher_pasta_saida, fg="white", bg="dodgerblue", font=("Arial", 12, "bold"), relief="solid", bd=2, width=25)
button_saida.pack(pady=15)

# Botão para iniciar a conversão
button_converter = Button(root, text="Converter para PDF", command=converter_para_pdf, fg="white", bg="green", font=("Arial", 12, "bold"), relief="solid", bd=2, width=25)
button_converter.pack(pady=15)

# Label para mostrar o status da conversão
label_status = Label(root, text="", fg="white", bg="#2e2e2e", font=("Arial", 12, "bold"))
label_status.pack(pady=15)

# Função principal para rodar a interface gráfica
root.mainloop()
