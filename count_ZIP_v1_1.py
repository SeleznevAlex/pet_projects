import csv
import re
import pprint

path_archive = input("Введите путь до ConfigurationReport: ")
path_archive = r'C:\Users\aa.seleznev\Desktop\E990_Report_220720-CreateConfigurationReport'
#path_archive = r'C:\Users\aa.seleznev\PycharmProjects\stepik2\analyze_Hitachi\470970-Report_220506-CreateConfigurationReport'


def unzip_file(path):
    pass


def get_info(path):
    file = path + r'\CSV\DkcInfo.csv'
    storage = []
    with open(file) as f:
        for line in f:
            if 'VSP' in line:
                storage = line.split(sep=',')
    model = storage[0]
    print('Model: ', model)
    print('sn: ', storage[1] + '\n')


def count_ctl(path):
    file = path + r'\CSV\CacheInfo.csv'
    ctls = []
    with open(file) as f:
        for line in f:
            if 'CTL' in line:
                result = re.match(r'CTL[\d]', line)
                ctls.append(result.group(0))
    print('controller - Контроллер - ', len(ctls))
    print('controller chassis - Шасси контроллерной полки - 1')
    print('BKMF - Бэкапный модуль с вентиляторами, для батарей - 3289036-A - 8 - 3292322-A для E990')


def count_bat(path):
    file = path + r'\CSV\DeviceEquipInfo.csv'
    bats = []
    with open(file) as f:
        for line in f:
            if 'BAT' in line and 'Not Equipped' not in line:
                bats.append(line[:7])
    print('Battery - Батарея - 3289081-A - ', len(bats))


def count_cfm(path):
    file = path + r'\CSV\CacheInfo.csv'
    cfms = []
    with open(file) as f:
        for line in f:
            if 'BM' in line:
                result = re.findall(r'BM\d{2}', line)
                cfms.extend(result)
    print('CFM (cache flash memory) ' + cfms[0] + ' - Диск для сохраннеия информации при обесточивании - ', len(cfms))


def count_dimm(path):
    file = path + r'\CSV\PcbRevInfo.csv'
    dimms = []
    with open(file) as f:
        for line in f:
            if 'DIMM' in line:
                dimms.append(line.split(sep=',')[2][:-2])
    type_dimm = dimms[0][2:]
    print('CACHE MEMORY ' + type_dimm + ' - Модуль памяти ОЗУ ' + type_dimm + ' - ', len(dimms))


def count_chb(path):
    file = path + r'\CSV\PcbRevInfo.csv'
    chbs = []
    with open(file) as f:
        for line in f:
            if 'CHB' in line:
                chbs.append(line.split(sep=',')[1])
    file2 = path + r'\CSV\PkInfo.csv'
    with open(file2) as f2:
        for line in f2:
            if 'CHB-' in line:
                type_chb = line.split(sep=',')[3]
    print('CHB(Channel Board) ' + type_chb[:2] + 'G - Плата для SFP - ', len(chbs))


def count_sfp(path):
    file = path + r'\CSV\PkInfo.csv'
    sfps = []
    with open(file) as f:
        for line in f:
            if 'CHB-' in line:
                sfps.append(line.strip().split(sep=',')[-1])
        type_sfp = line.strip().split(sep=',')[4]
    speed_sfp = sfps[0]
    print('SFP ' + speed_sfp + ' ' + type_sfp + '- Модуль передачи оптического сигнала - ', len(sfps))


def count_dkb(path):
    file = path + r'\CSV\DkaInfo.csv'
    dkbs = []
    with open(file) as f:
        for line in f:
            if 'DKB-' in line:
                dkbs.append(line.strip().split(sep=',')[0])
    print('DKB (Disk Board)- Плата для подключения SAS-кабелей - ', len(dkbs))


def count_dbs(path):
    file = path + r'\CSV\HduInfo.csv'
    dbs = {}
    type_dbs = []
    count_dbs = {}
    with open(file) as f:
        for line in f:
            if 'DB ' not in line and 'Not Installed' not in line:
                local_db = line.strip().split(sep=',')[0]
                type_db = line.strip().split(sep=',')[-1]
                type_dbs.append(type_db)
                dbs[local_db] = type_db
    print('Всего полок: ', len(dbs))
    type_dbs = list(set(type_dbs))
    for type_db in type_dbs:
        for value, key in dbs.items():
            if type_db == key:
                if type_db  in count_dbs:
                    count_dbs[type_db] += 1
                else:
                    count_dbs[type_db] = 1
    for db, qty in count_dbs.items():
        print(db, '=', qty)
    for db, qty in count_dbs.items():
        print('Drive Box '+ db +' - Шасси для полки ' + db + ' - ' + str(qty))
        print('ENC '+ db +' - Плата для подключения SAS-кабелей полки ' + db + ' - ' + str(int(qty)*2))
        print('Power Supply ' + db + ' - Блок питания для полки ' + db + ' - ' + str(int(qty) * 2) + '\n')

def count_disks(path):
    file = path + r'\CSV\PdevInfo.csv'
    disks = {}
    type_disks = []
    with open(file) as f:
        for line in f:
            if 'HDD' in line:
                type_hdd = line.strip().split(sep=',')[6]
                if type_hdd in disks:
                    disks[type_hdd] += 1
                else:
                    disks[type_hdd] = 1
    for key, value in disks.items():
        print(key, '=', value)


print('*******************************')
print('***** PARTS OF CONTROLLER *****')
print('*******************************')
get_info(path_archive)
count_ctl(path_archive)
count_bat(path_archive)
count_cfm(path_archive)
count_dimm(path_archive)
print('Power Supply - Блок питания контроллерной полки - 2')
count_chb(path_archive)
count_sfp(path_archive)
count_dkb(path_archive)
print('LAN board - Плата для подключения Ethernet-кабелей RJ45 - 3289044-A - 2')
print('SVP - Управляющий модуль - 3919435-P - 1')
print('*******************************')
print('*****     DISK BOARDS     *****')
print('*******************************')
count_dbs(path_archive)
print('*******************************')
print('*****       DISKS         *****')
print('*******************************')
count_disks(path_archive)
