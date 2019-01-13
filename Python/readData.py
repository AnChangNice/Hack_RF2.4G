"""
    read csv test
"""

REG_MAP = {
    0x00: 'CONFIG',
    0x01: 'EN_AA',
    0x02: 'EN_RXADDR',
    0x03: 'SETUP_AW',
    0x04: 'SETUP_RETR',
    0x05: 'RF_CH',
    0x06: 'RF_SETUP',
    0x07: 'NRF_STATUS',
    0x08: 'OBSERVE_TX',
    0x09: 'CD',
    0x0A: 'RX_ADDR_P0',
    0x0B: 'RX_ADDR_P1',
    0x0C: 'RX_ADDR_P2',
    0x0D: 'RX_ADDR_P3',
    0x0E: 'RX_ADDR_P4',
    0x0F: 'RX_ADDR_P5',
    0x10: 'TX_ADDR',
    0x11: 'RX_PW_P0',
    0x12: 'RX_PW_P1',
    0x13: 'RX_PW_P2',
    0x14: 'RX_PW_P3',
    0x15: 'RX_PW_P4',
    0x16: 'RX_PW_P5',
    0x17: 'FIFO_STATUS',
    0x1C: 'DYNPD',
    0x1D: 'FEATURE',
}

def str_format(time, ID, MOSI, CMD, MISO, STATE):
    str = ''

    str = str + time + ','
    str = str + ID + ','

    for value in MOSI:
        str = str + value + '|'
    str = str[:-1]

    str = str + ','
    str = str + CMD + ','
    str = str + ','

    for value in MISO:
        str = str + value + '|'
    str = str[:-1]

    str = str + ','
    str = str + STATE + ','
    str = str + ','

    str = str + '\n'
    return str


def cmd_interpret(cmd_str):
    cmd = int(cmd_str, 16)

    print("CMD :")
    # decode
    if cmd & 0xE0 == 0x00:
        print("----R_REGISTER:", cmd & 0x1F, '-', REG_MAP[cmd & 0x1F])

    if cmd & 0xE0 == 0x20:
        print("----W_REGISTER:", cmd & 0x1F, '-', REG_MAP[cmd & 0x1F])

    if cmd == 0x61:
        print("----R_RX_PAYLOAD")
    if cmd == 0xA0:
        print("----W_TX_PAYLOAD")
    if cmd == 0xE1:
        print("----FLUSH_TX")
    if cmd == 0xE2:
        print("----FLUSH_RX")
    if cmd == 0xE3:
        print("----REUSE_TX_PL")
    if cmd == 0x50:
        print("----ACTIVATE")
    if cmd == 0x60:
        print("----R_RX_PL_WID")

    if cmd & 0xF8 == 0xA8:
        print("----W_ACK_PAYLOAD:", cmd & 0x07)

    if cmd == 0xB0:
        print("----W_TX_PAYLOAD_NOACK")
    if cmd == 0xFF:
        print("----NOP")


def state_interpret(state_str):
    state = int(state_str, 16)

    print("STATE :")
    if state & 0x01 == 0x01:
        print("----TX_FULL")

    if state & 0x0E == 0x0E:
        print("----RX_P_NO - Not used")
    elif state & 0x0E == 0x0C:
        print("----RX_P_NO - RX FIFO Empty")
    else:
        print("----RX_P_NO - ", ((state & 0x0E) / 2))

    if state & 0x10 == 0x10:
        print("----MAX_RT")

    if state & 0x20 == 0x20:
        print("----TX_DS - Data Sent TX FIFO interrupt")

    if state & 0x40 == 0x40:
        print("----RX_DR - Data Ready RX FIFO interrupt")

    if state & 0x80 == 0x80:
        print("----REG_BANK - 1")


f = open("dataPacked.csv", 'r')
f2 = open("dataPackedPlusCmd.csv", 'w+')

lastID = '0'
lastTime = '0'
MOSI = []
MISO = []

f.readline()
title_str = 'time, ID, MOSI, CMD, MISO, STATE\n'
f2.write(title_str)

index = 0

while f.readable():
    line = f.readline()
    line = line.replace('\n', '')
    line = line.split(',')

    temp_time = line[0]
    temp_ID = line[1]
    temp_MOSI = line[2]
    temp_MISO = line[3]

    temp_cmd = line[2].split('|')
    temp_state = line[3].split('|')

    #
    # if temp_ID != lastID:
    #     w_str = str_format(lastTime, lastID, MOSI, MISO)
    #     f2.write(w_str)
    #     print(w_str)
    #     lastID = temp_ID
    #     lastTime = temp_time
    #     MOSI.clear()
    #     MISO.clear()
    #
    # MOSI.append(temp_MOSI)
    # MISO.append(temp_MISO)

    print(line)
    print(temp_cmd[0], temp_state[0])
    cmd_interpret(temp_cmd[0])
    state_interpret(temp_state[0])
    # index = index + 1
    # if index > 100:
    #     break

    # if int(temp_ID) > 20:
    #     break

f.close()
f2.close()






