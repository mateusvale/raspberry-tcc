from script_functions import *

folder_in_circle = "/Users/mateus/Personal/raspberry/in_circle"
img_default_location = ''

# primeiro olha o arquivo de status. Caso ele esteja em running, espere 3 segundos e
# veja novamente. Caso continue em running, retorn null. Caso esteja stopped, continue
# com o comando.