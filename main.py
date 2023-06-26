from script_functions import *

linha = "600"
onibus_ordem = "C47601"
address_img_files = "/home/pi/TCC/raspberry-tcc/img_files"
address_in_circle = "/home/pi/TCC/raspberry-tcc/in_circle"
address_image_default = '/home/pi/image_default/Pi-logo'
address_log_file = "/home/pi/TCC/raspberry-tcc/logs.txt"
status = "/home/pi/TCC/raspberry-tcc/status.txt"

# le as informacoes da API de marketing, transforma em um array de json e retorna
##marketings = get_all_marketing_from_db(linha)

# com as informacoes de marketing, faca o download dos arquivos para pasta img_files
# o arquivo internal_db auxiliara para verificar caso um arquivo ja foi baixado.
##new_marketing_in_internal_db(marketings)

# coloca o status como running
##manage_file(status, 'w', 'running')

# le as informacoes do onibus e tenta verificar se ele se encontra dentro do
# circulo do marketing. Caso sim, copio o arquivo de imagem para pasta in_circle. Caso contrario, removo
# da pasta caso exista
##manage_in_circle_folder(address_img_files,address_in_circle,linha,onibus_ordem)

# coloca o status como stopped
##manage_file(status, 'w', 'stopped')

desktop_background(address_in_circle, address_image_default, address_log_file)
