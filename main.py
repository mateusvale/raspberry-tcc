from script_functions import *

linha = "600"
onibus_ordem = "C47646"
address_img_files = "/Users/mateus/Personal/raspberry/img_files"
address_in_circle = "/Users/mateus/Personal/raspberry/in_circle"
status = "status.txt"

# lê as informações da API de marketing, transforma em json e retorna
marketings = get_all_marketing_from_db(linha)

# com as informações de marketing, faça o download dos arquivos para pasta img_files
# o arquivo internal_db auxiliará para verificar caso um arquivo já foi baixado
new_marketing_in_internal_db(marketings)

# # coloca o status como running
manage_file(status, 'w', 'running')

# lê as informações do onibus da linha e tenta verificar se ele se encontra dentro do
# circulo do marketing. Caso sim, copio-o para pasta in_circle. Caso contrário, removo
# da pasta caso exista
manage_in_circle_folder(address_img_files,address_in_circle,linha,onibus_ordem)

# # coloca o status como stopped
manage_file(status, 'w', 'stopped')