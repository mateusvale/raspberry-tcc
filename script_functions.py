import requests
import json
import math
import os
import time

# linha = "600"
# onibus_ordem = "C47588"
# address_img_files = "/Users/mateus/Personal/raspberry/img_files"
# address_in_circle = "/Users/mateus/Personal/raspberry/in_circle"

########################################################################################################

## GPS onibus ##
def get_bus_gps(linha_onibus = 'all', ordem = "none"):
    url = f'https://db-postgress-tcc.herokuapp.com/onibus/{linha_onibus}'
    x = requests.get(url)
    results = json.loads(x.text)
    if ordem != "none":
        for entry in results:
            if entry['ordem'] == ordem:
                return entry 
    # print(results)
    return results

def are_points_in_the_circle(checkPoint, centerPoint, m): #(circle, bus, radius)
    km = m/1000
    ky = 40000 / 360
    kx = math.cos(math.pi * centerPoint['lat'] / 180.0) * ky
    dx = abs(centerPoint['lng'] - checkPoint['lng']) * kx
    dy = abs(centerPoint['lat'] - checkPoint['lat']) * ky
    return math.sqrt(dx * dx + dy * dy) <= km


########################################################################################################

## gerenciamento do DB ##

def get_all_marketing_from_db(linha):
    url = 'https://db-postgress-tcc.herokuapp.com/marketing'
    x = requests.get(url)
    results = json.loads(x.text)
    marketing = []
    for result in results:
        if result['bus_line'] == linha:
            marketing.append(result)
    return marketing

def get_marketing_from_db(marketing_id):
    url = f'https://db-postgress-tcc.herokuapp.com/marketing/{marketing_id}'
    x = requests.get(url)
    return json.loads(x.text)

def download_image(image_url, name = 'image'):
    response = requests.get(image_url)
    file = f'./img_files/{name}.jpeg'
    open(file, "wb").write(response.content)


########################################################################################################

## gerenciamento do internal_db ##

def new_marketing_in_internal_db(marketings):
    # marketings = get_all_marketing_from_db(linha)
    internal_db = read_internal_db()
    for marketing in marketings:
        new_marketing = True
        for entry in internal_db:
            if entry["user_id"] == marketing["user_id"] and entry["marketing_id"] == marketing["id"]:
                new_marketing = False
                break
        if new_marketing == True:
            name = f'{marketing["user_id"]}-{marketing["id"]}'
            download_image(marketing["image_url"], name)
            internal_db.append({
                "user_id": marketing["user_id"],
                "marketing_id": marketing["id"],
                "code": 0 
            })
    json_data = json.dumps(internal_db)
    write_internal_db(json_data)

def write_internal_db(internal_db):
    file = open("internal_db.json", "w")
    file.write(internal_db)
    file.close()

def read_internal_db():
    file = open("/home/pi/TCC/raspberry-tcc/internal_db.json", "r")
    internal_db = file.read()
    internal_db = json.loads(internal_db)
    return internal_db


########################################################################################################

## reading in img_files folder ##

def read_img_files_folder(address_img_files, linha):
    files = os.listdir(address_img_files)
    marketing_list = get_all_marketing_from_db(linha)
    info_files = []

    for file in files:
        user_id = file.split('.')[0].split('-')[0]
        marketing_id = file.split('.')[0].split('-')[1]
        marketing = {}
        marketing = [x for x in marketing_list if str(x['id']) == marketing_id][0]
        info_files.append({
            'name': file,
            'user_id': user_id,
            'marketing_id': marketing_id,
            'radius': marketing['radius'],
            'lat': marketing['lat'],
            'lng': marketing['lng']
        })
    return info_files


########################################################################################################

## managing in in_circle folder ##

# def manage_in_circle_folder(source_folder, destination_folder, linha, onibus_ordem):
#     bus_location = get_bus_gps(linha, onibus_ordem)
#     # print(bus_location)
#     files = read_img_files_folder(source_folder, linha)
#     queue = manage_file('queue.txt', 'r')
#     queue = transform_str_to_arr(queue)
#     for file in files:
#         # print(bus_location)
#         destination = f'{destination_folder}/{file["name"]}' #address_in_circle
#         bus = {'lat': float(bus_location['latitude']), 'lng': float(bus_location['longitude'])}
#         inside_circle = are_points_in_the_circle(file, bus, file['radius'])
#         if (inside_circle):
#             if queue.count(file['name']) == 0:
#                 copy_code = f'cp {source_folder}/{file["name"]} {destination}' #address_img_files
#                 os.system(copy_code)
#                 queue = [file['name']] + queue
#         elif os.path.exists(destination):
#             os.remove(destination)
#             arr = []
#             for i in queue:
#                 if i != file['name']:
#                     arr.append(i)
#             queue = arr.copy() 

#     manage_file('queue.txt', 'w', str(queue))


def manage_in_circle_folder(source_folder, destination_folder, linha, onibus_ordem):
    bus_location = get_bus_gps(linha, onibus_ordem)
    # print(bus_location)
    files = read_img_files_folder(source_folder, linha)
    for file in files:
        # print(bus_location)
        destination = f'{destination_folder}/{file["name"]}' #address_in_circle
        bus = {'lat': float(bus_location['latitude']), 'lng': float(bus_location['longitude'])}
        inside_circle = are_points_in_the_circle(file, bus, file['radius'])
        if (inside_circle):
            if os.path.exists(destination) == False:
                os.system(f'cp {source_folder}/{file["name"]} {destination}' )

        elif os.path.exists(destination):
            os.remove(destination)

########################################################################################################

## desktop background ##

def desktop_background(folder_in_circle, img_default_location, log_file):
    image_circle_folder = os.listdir(folder_in_circle)

    if len(image_circle_folder) == 0:
        os.system(f'pcmanfm --set-wallpaper {img_default_location}')
        logging(False, log_file)
    else:
        os.system(f'pcmanfm --set-wallpaper {folder_in_circle}/{image_circle_folder[0]}')
        logging(True, log_file)
        
def logging(is_image_in_circle, log_file):
    jump_line = f'echo ############## >> {log_file}'
    if is_image_in_circle:
        os.system(f'echo $(date) -- ônibus dentro do círculo de propaganda >> {log_file}')
    else:
        os.system(f'echo $(date) -- ônibus fora do círculo de propaganda >> {log_file}')
    #os.system(message)
    os.system(f'echo ############## >> {log_file}')

########################################################################################################

## reading and writing files

def manage_file(file_name, action, content = ""):
    file = open(file_name, 'r')
    if action == 'r' or action == 'read':
        return file.read()
    else:
        file = open(file_name, "w")
        file.write(content)
        file.close()

########################################################################################################

## transform string to array

def transform_str_to_arr(string):
    aux = string.replace('[','')
    aux = aux.replace(']','')
    if aux == '':
        return []
    return aux.split(',')