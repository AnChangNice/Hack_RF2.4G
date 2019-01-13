"""
    read csv test
"""

def str_format(time, ID, MOSI, MISO):
    str = ''
    str = str + time + ','
    str = str + ID + ','
    for value in MOSI:
        str = str + value + '|'
    str = str[:-1]
    str = str + ','
    for value in MISO:
        str = str + value + '|'
    str = str[:-1]
    str = str + '\n'
    return str

# open file
f = open("dataPack.csv", 'r')
f2 = open("dataPacked.csv", 'w+')

# global value for store state and value
lastID = '0'
lastTime = '0'
MOSI = []
MISO = []

f.readline()  # read the title

title_str = 'time, ID, MOSI, MISO\n'
f2.write(title_str)  # write title

while f.readable():
    line = f.readline()
    line = line.replace('\n', '')
    line = line.split(',')

    temp_time = line[0]
    temp_ID = line[1]
    temp_MOSI = line[2]
    temp_MISO = line[3]

    if temp_ID != lastID:
        w_str = str_format(lastTime, lastID, MOSI, MISO)
        f2.write(w_str)
        print(w_str)
        lastID = temp_ID
        lastTime = temp_time
        MOSI.clear()
        MISO.clear()

    MOSI.append(temp_MOSI)
    MISO.append(temp_MISO)

    print(line)

f.close()
f2.close()






