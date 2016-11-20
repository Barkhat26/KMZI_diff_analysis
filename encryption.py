from init_data import *


def do_ep(input_block):
    output_block = ''
    for i in E_PERM:
        output_block += input_block[i - 1]
    return output_block


def do_p(input_block):
    output_block = ''
    for i in PERM:
        output_block += input_block[i - 1]
    return output_block


def do_s1(input_block):
    a1 = int(input_block[0], base=2)
    a2a3a4 = int(input_block[1:4], base=2)
    return '{:03b}'.format(S1_BOX_TABLE[a1][a2a3a4])


def do_s2(input_block):
    a1 = int(input_block[0], base=2)
    a2a3a4 = int(input_block[1:4], base=2)
    return '{:03b}'.format(S2_BOX_TABLE[a1][a2a3a4])


def do_s3(input_block):
    a1a4 = int(input_block[0] + input_block[3], base=2)
    a2a3 = int(input_block[1] + input_block[2], base=2)
    return '{:02b}'.format(S3_BOX_TABLE[a1a4][a2a3])


def do_f(input_block, round_key):
    a = '{:012b}'.format(int(do_ep(input_block), base=2) ^ int(round_key, base=2))
    c1 = do_s1(a[0:4])
    c2 = do_s2(a[4:8])
    c3 = do_s3(a[8:12])
    return do_p(c1 + c2 + c3)


def encrypt(input_block, key):
    round1_key = key[0:12]
    round2_key = key[6:18]
    round3_key = key[12:24]

    left_part = input_block[0:8]
    right_part = input_block[8:16]

    # After 1st round
    left_part, right_part = right_part, '{:08b}'.format(int(left_part, base=2) ^ int(do_f(right_part, round1_key), base=2))

    # After 2nd round
    left_part, right_part = right_part, '{:08b}'.format(int(left_part, base=2) ^ int(do_f(right_part, round2_key), base=2))

    # After 3rd round
    return '{:08b}'.format(int(left_part, base=2) ^ int(do_f(right_part, round3_key), base=2)) + right_part

