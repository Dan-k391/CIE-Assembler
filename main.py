import csv
import copy

commands = []
command_dict = {}
with open('code.txt', 'r') as f:
    code_txt = f.read()
line_code = code_txt.split('\n')
code_len = len(line_code)
for i in range(code_len):
    in_line_code = line_code[i].split(' ')
    if len(in_line_code) == 3:
        commands.append([int(in_line_code[0]), in_line_code[1], in_line_code[2]])
    else:
        commands.append([int(in_line_code[0]), in_line_code[1]])

for i in range(code_len):
    command_dict[commands[i][0]] = commands[i][1:]
print(commands)

#
data = [['ACC', '']]
data_dict = {}
with open('data.txt', 'r') as f:
    data_txt = f.read()
line_data = data_txt.split('\n')
data_len = len(line_data)
for i in range(data_len):
    in_line_data = line_data[i].split(' ')
    data.append([in_line_data[0], in_line_data[1]])
data.append(['OUT', ''])

for i in range(data_len + 2):
    data_dict[data[i][0]] = data[i][1]
# print(commands)
# print(data_dict)
count = 0

headers = ['line']
for i in data_dict:
    headers.append(i)
rows = []

line = int(commands[0][0])
finish_line = int(commands[-1][0])

print(data_dict.items())
comp = False

while True:
    # print(line, command_dict[line][0])
    operand = ''
    ix = ''
    if command_dict[line][0] != 'OUT' and command_dict[line][0] != 'END':
        operand = command_dict[line][1]
        ix = data_dict['IX']
    if command_dict[line][0] == 'LDM':
        data_dict['ACC'] = operand
    elif command_dict[line][0] == 'LDD':
        data_dict['ACC'] = data_dict[operand]
    elif command_dict[line][0] == 'LDI':
        data_dict['ACC'] = data_dict[data_dict[operand]]
    elif command_dict[line][0] == 'LDX':
        data_dict['ACC'] = data_dict[str(int(operand) + int(ix))]
    elif command_dict[line][0] == 'LDR':
        data_dict['IX'] = operand
    elif command_dict[line][0] == 'MOV':
        data_dict[operand] = data_dict['ACC']
    elif command_dict[line][0] == 'STO':
        data_dict[operand] = data_dict['ACC']
    elif command_dict[line][0] == 'ADD':
        data_dict['ACC'] = str(int(data_dict['ACC']) + int(data_dict[operand]))
    elif command_dict[line][0] == 'INC':
        data_dict[operand] = str(int(data_dict[operand]) + 1)
    elif command_dict[line][0] == 'DEC':
        data_dict[operand] = str(int(data_dict[operand]) - 1)
    elif command_dict[line][0] == 'CMP':
        comp = (int(data_dict['ACC']) == int(data_dict[operand]))
    elif command_dict[line][0] == 'JPE':
        if comp:
            line = int(operand)
            continue
    elif command_dict[line][0] == 'JPN':
        if not comp:
            line = int(operand)
            continue
    elif command_dict[line][0] == 'JMP':
        line = int(operand)
        continue
    elif command_dict[line][0] == 'OUT':
        data_dict['OUT'] = chr(int(data_dict['ACC']))
    elif command_dict[line][0] == 'END':
        break
    else:
        print('No opcode named ' + command_dict[line][0])
        exit()
    
    # store content of each line
    content = [line]
    for i in data_dict:
        content.append(data_dict[i])
    rows.append(content)

    count += 1
    line += 1
    # print(content)
    #
    # content.insert(0, line)

# add the last one
content = [line]
for i in data_dict:
    content.append(data_dict[i])
rows.append(content)

rows_change = copy.deepcopy(rows)
for i in range(len(rows)):
    if i == 0:
        for j in range(len(rows[i])):
            if rows_change[i][j] == '-30000':
                rows_change[i][j] = ' '
        continue
    for j in range(len(rows[i])):
        if rows_change[i][j] == rows[i - 1][j] or rows_change[i][j] == '-30000':
            rows_change[i][j] = ' '

print(rows)
print(rows_change)
with open('table.csv', 'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows_change)

