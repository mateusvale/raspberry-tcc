from script_functions import *

folder_in_circle = "/home/pi/TCC/raspberry-tcc/in_circle"
img_default_location = '/home/pi/image_default'

image_circle_folder = os.listdir(folder_in_circle)

#primeira versao - não pode haver mais de uma propaganda no mesmo circulo

# colocar a imagem -> caso tenha duas ou mais imagens dentro do circulo

# primeiro olha o arquivo de status. Caso ele esteja em running, espere 3 segundos e
# veja novamente. Caso continue em running, retorn null. Caso esteja stopped, continue
# com o comando.