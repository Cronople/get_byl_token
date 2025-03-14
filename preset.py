def getPreset():
    with open('preset.txt', 'r', encoding='utf-8') as idpwFile:
        preset_data = {}

        data = idpwFile.readlines()
        for i in data:
            tempdata = i.split(']')
            value = tempdata[1].strip()
            key = tempdata[0].strip()
            if value == '':
                preset_data[key] = ''
            else:
                preset_data[key] = value
        idpwFile.close()
    
    
    print('-' * 20)
    print(preset_data)
    print('-' * 20)

    return preset_data

getPreset()