from encryption import do_s1, do_s2, do_s3

def dtob(number, width):
    format_string = '{:0' + str(width) + 'b}'
    return format_string.format(number)


def btod(binary_string):
    return int(binary_string, base=2)


def foo(delta_a, block):
    if block == 's1':
        do_replace = do_s1
        delta_c_width = 3
    elif block == 's2':
        do_replace = do_s2
        delta_c_width = 3
    elif block == 's3':
        do_replace = do_s3
        delta_c_width = 2
    else:
        raise RuntimeError('Unknown s-block')
    
    input_block1 = [dtob(i, 4) for i in range(16)]
    output_block1 = [do_replace(i) for i in input_block1]
    input_block2 = [dtob(btod(i) ^ btod(delta_a), 4) for i in input_block1]
    output_block2 = [do_replace(i) for i in input_block2]
    delta_c_lst = list(map(lambda x, y: dtob(btod(x) ^ btod(y), delta_c_width), output_block1, output_block2))
    return input_block1, input_block2, delta_c_lst


def parse():
    xl1_lst, xr1_lst, yl1_lst, yr1_lst = [], [], [], []
    xl2_lst, xr2_lst, yl2_lst, yr2_lst = [], [], [], []
    
    with open('save.txt', 'r') as f:
        line_cnt = 1
        for line in f:
            if line.startswith(' --- '):
                continue
            if line_cnt == 1:
                xl1, xr1, yl1, yr1 = line.split(' --- ')[0:4]
                xl1_lst.append(xl1)
                xr1_lst.append(xr1)
                yl1_lst.append(yl1)
                yr1_lst.append(yr1)
                line_cnt += 1
            elif line_cnt == 2:
                xl2, xr2, yl2, yr2 = line.split(' --- ')[0:4]
                xl2_lst.append(xl2)
                xr2_lst.append(xr2)
                yl2_lst.append(yl2)
                yr2_lst.append(yr2)
                line_cnt += 1
            else:
                line_cnt = 1
    return xl1_lst, xr1_lst, yl1_lst, yr1_lst, xl2_lst, xr2_lst, yl2_lst, yr2_lst
