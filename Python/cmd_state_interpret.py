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
    0x07: 'STATUS',
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
    str_list = [time, ID, MOSI, CMD, MISO, STATE]

    str = ','.join(str_list)

    str = str + '\n'

    return str


def cmd_interpret(cmd_str):
    cmd = int(cmd_str, 16)

    str_list = []
    str_temp = 'CMD :'
    str_list.append(str_temp)
    # decode
    if cmd & 0xE0 == 0x00:
        str_temp = 'R_REGISTER - ' + "0x%02X" % (cmd & 0x1F) + '-' + REG_MAP[cmd & 0x1F]
        str_list.append(str_temp)

    if cmd & 0xE0 == 0x20:
        str_temp = 'W_REGISTER - ' + "0x%02X" % (cmd & 0x1F) + '-' + REG_MAP[cmd & 0x1F]
        str_list.append(str_temp)

    if cmd == 0x61:
        str_temp = 'R_RX_PAYLOAD'
        str_list.append(str_temp)
    if cmd == 0xA0:
        str_temp = 'W_TX_PAYLOAD'
        str_list.append(str_temp)
    if cmd == 0xE1:
        str_temp = 'FLUSH_TX'
        str_list.append(str_temp)
    if cmd == 0xE2:
        str_temp = 'FLUSH_RX'
        str_list.append(str_temp)
    if cmd == 0xE3:
        str_temp = 'REUSE_TX_PL'
        str_list.append(str_temp)
    if cmd == 0x50:
        str_temp = 'ACTIVATE'
        str_list.append(str_temp)

    if cmd == 0x60:
        str_temp = 'R_RX_PL_WID'
        str_list.append(str_temp)

    if cmd & 0xF8 == 0xA8:
        str_temp = 'W_ACK_PAYLOAD - ' + str(cmd & 0x07)
        str_list.append(str_temp)

    if cmd == 0xB0:
        str_temp = 'W_TX_PAYLOAD_NOACK'
        str_list.append(str_temp)
    if cmd == 0xFF:
        str_temp = 'NOP'
        str_list.append(str_temp)

    return ''.join(str_list)



def state_interpret(state_str):
    state = int(state_str, 16)

    str_list = []
    str_head = 'STATE : '
    str_temp = ''

    if state & 0x01 == 0x01:
        str_temp = 'TX_FULL'
        str_list.append(str_temp)

    if state & 0x0E == 0x0E:
        str_temp = 'RX_P_NO - RX FIFO Empty'
        str_list.append(str_temp)
    elif state & 0x0E == 0x0C:
        str_temp = 'RX_P_NO - Not used'
        str_list.append(str_temp)
    else:
        str_temp = 'RX_P_NO - ' + str(int((state & 0x0E) / 2))
        str_list.append(str_temp)

    if state & 0x10 == 0x10:
        str_temp = 'MAX_RT'
        str_list.append(str_temp)

    if state & 0x20 == 0x20:
        str_temp = 'TX_DS - Data Sent TX FIFO interrupt'
        str_list.append(str_temp)

    if state & 0x40 == 0x40:
        str_temp = 'RX_DR - Data Ready RX FIFO interrupt'
        str_list.append(str_temp)

    if state & 0x80 == 0x80:
        str_temp = 'REG_BANK - 1'
        str_list.append(str_temp)

    str_temp = ' | '.join(str_list)
    return 'STATE : ' + str_temp


f = open("dataPacked.csv", 'r')
f2 = open("dataPackedPlusCmd.csv", 'w+')

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


    print(line)
    print(temp_cmd[0], temp_state[0])
    cmd = cmd_interpret(temp_cmd[0])
    state = state_interpret(temp_state[0])
    out_str = str_format(temp_time, temp_ID, temp_MOSI, cmd, temp_MISO, state)
    f2.write(out_str)


f.close()
f2.close()






