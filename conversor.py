from PIL import Image
import os
import time
import sys

PASTA_ENTRADA = "entrada"
PASTA_SAIDA = "saida"

# Função para garantir que as pastas existam
def garantir_pastas():
    os.makedirs(PASTA_ENTRADA, exist_ok=True)
    os.makedirs(PASTA_SAIDA, exist_ok=True)

# Função para exibir o menu de opções
def mostrar_menu():
    print("\n" + "=" * 40)
    print(" CONVERSOR UNIVERSAL → PDF")
    print("=" * 40)
    print("1 - Converter imagens para PDFs (separados)")
    print("2 - Converter várias imagens em UM PDF")
    print("0 - Sair")
    print()

# Função para listar as imagens na pasta de entrada
def listar_imagens():
    arquivos = os.listdir(PASTA_ENTRADA)
    return [f for f in arquivos if f.lower().endswith((".jpg", ".jpeg", ".png"))]

# Função para escolher as imagens a serem convertidas
def escolher_imagens(imagens):
    print("\nImagens encontradas:")
    for i, img in enumerate(imagens, start=1):
        print(f"{i} - {img}")

    print("\nEscolha:")
    print("1 - Uma imagem")
    print("2 - Todas as imagens")
    print("3 - Várias imagens")

    opcao = input("Opção: ")

    selecionadas = []

    if opcao == "1":
        n = input("Número da imagem: ")
        if n.isdigit() and 1 <= int(n) <= len(imagens):
            selecionadas.append(imagens[int(n) - 1])

    elif opcao == "2":
        selecionadas = imagens.copy()

    elif opcao == "3":
        nums = input("Números separados por vírgula (ex: 1,3): ")
        for n in nums.split(","):
            n = n.strip()
            if n.isdigit() and 1 <= int(n) <= len(imagens):
                selecionadas.append(imagens[int(n) - 1])

    if not selecionadas:
        print("❌ Nenhuma imagem válida selecionada.")

    return selecionadas

# Função para abrir a pasta automaticamente
def abrir_pasta(caminho):
    try:
        if sys.platform.startswith("win"):
            os.startfile(caminho)  # Para Windows
        elif sys.platform.startswith("darwin"):
            os.system(f"open {caminho}")  # Para macOS
        else:
            os.system(f"xdg-open {caminho}")  # Para Linux
    except:
        pass

# Função para converter imagens para PDF
def converter_imagens(lista_imagens, modo_unico_pdf=False):
    if not lista_imagens:
        return

    if modo_unico_pdf:
        if len(lista_imagens) < 2:
            print("❌ Selecione pelo menos 2 imagens.")
            return

        nome_pdf = input("Nome do PDF final (sem .pdf): ").strip()
        if not nome_pdf:
            print("❌ Nome inválido.")
            return

        caminho_pdf = os.path.join(PASTA_SAIDA, nome_pdf + ".pdf")
        imagens_pdf = []

        try:
            for i, nome in enumerate(lista_imagens, start=1):
                print(f"🔄 Processando {i}/{len(lista_imagens)}: {nome}")
                img = Image.open(os.path.join(PASTA_ENTRADA, nome)).convert("RGB")
                imagens_pdf.append(img)

            imagens_pdf[0].save(
                caminho_pdf,
                save_all=True,
                append_images=imagens_pdf[1:]
            )

            print(f"\n✅ PDF único criado: {caminho_pdf}")
            abrir_pasta(PASTA_SAIDA)  # Abre a pasta de saída

        except Exception as erro:
            print(f"❌ Erro: {erro}")

    else:
        total = len(lista_imagens)

        for i, nome in enumerate(lista_imagens, start=1):
            print(f"🔄 Convertendo {i}/{total}: {nome}")
            caminho_img = os.path.join(PASTA_ENTRADA, nome)
            caminho_pdf = os.path.join(
                PASTA_SAIDA,
                os.path.splitext(nome)[0] + ".pdf"
            )

            try:
                img = Image.open(caminho_img).convert("RGB")
                img.save(caminho_pdf, "PDF")
                print(f"✅ Gerado: {os.path.basename(caminho_pdf)}")
                time.sleep(0.3)
            except Exception as erro:
                print(f"❌ Erro em {nome}: {erro}")

        print(f"\n🎉 {total} PDF(s) gerado(s) com sucesso!")
        abrir_pasta(PASTA_SAIDA)  # Abre a pasta de saída

# Função principal que coordena tudo
def main():
    garantir_pastas()

    # Mensagem explicativa
    print("\n📂 A pasta ENTRADA foi aberta automaticamente.")
    print("➡ Coloque os arquivos que deseja converter ali.\n")
    abrir_pasta(PASTA_ENTRADA)  # Abre a pasta de entrada automaticamente

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ")

        if opcao in ("1", "2"):
            imagens = listar_imagens()
            if not imagens:
                print("❌ Nenhuma imagem na pasta 'entrada'.")
                continue

            selecionadas = escolher_imagens(imagens)

            if opcao == "1":
                converter_imagens(selecionadas)
            else:
                converter_imagens(selecionadas, modo_unico_pdf=True)

        elif opcao == "0":
            print("👋 Programa finalizado.")
            break

        else:
            print("❌ Opção inválida.")

# Rodando o programa
if __name__ == "__main__":
    main()
