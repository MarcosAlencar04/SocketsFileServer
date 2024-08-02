---
# Socket File Server

Este é um programa que utiliza sockets para fazer controle de arquivos, permitindo upload e download de arquivos entre um cliente e um servidor.

## Requisitos

Certifique-se de que você tenha:

- Python 3 ou superior instalado.
- As seguintes bibliotecas instaladas:
  - `socket`
  - `tkinter`
  - `os`
  - `threading`
  - `datetime`

## Configuração Inicial

1. Crie duas pastas no diretório do projeto:
   - `ArquivosCliente` para salvar os arquivos baixados pelo cliente.
   - `ArquivosServidor` para salvar os arquivos enviados pelo cliente.

## Arquivo de Logs

O programa gera um arquivo de logs chamado `server_log.txt`, que registra o IP e a ação (upload ou download), seguido do nome do arquivo.

## Executando o Programa

Para iniciar o servidor e o cliente, execute os seguintes comandos na ordem:

1. Inicie o servidor:
   ```sh
   python server.py
   ```

2. Inicie o cliente:
   ```sh
   python client.py
   ```

---
