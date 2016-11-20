from encryption import do_ep
from utils import dtob, btod, foo
from itertools import product


def get_prob_parts_of_round_key(exr1, exr2, prob_inputs):
    prob_keys1 = set()
    prob_keys2 = set()
    for i in prob_inputs:
        prob_keys1.add(dtob(btod(i[0]) ^ btod(exr1), 4))
        prob_keys2.add(dtob(btod(i[1]) ^ btod(exr2), 4))
    return list(prob_keys1 & prob_keys2)


def analyze_round_key_part(part, first_texts, second_texts, delta_a, delta_c):
    if part == 1:
        s_block = 's1'
    elif part == 2:
        s_block = 's2'
    elif part == 3:
        s_block = 's3'
    else:
        raise RuntimeError('Unknown part: {:}'.format(part))

    input_block1, input_block2, delta_c_lst = foo(delta_a, s_block)
    prob_inputs = []
    for i in range(len(delta_c_lst)):
        if delta_c_lst[i] == delta_c:
            prob_inputs.append((input_block1[i], input_block2[i]))
    result_row = [0]*16
    for i in range(len(first_texts)):
        if part == 1:
            exr1 = do_ep(first_texts[i])[0:4]
            exr2 = do_ep(second_texts[i])[0:4]
        if part == 2:
            exr1 = do_ep(first_texts[i])[4:8]
            exr2 = do_ep(second_texts[i])[4:8]
        if part == 3:
            exr1 = do_ep(first_texts[i])[8:12]
            exr2 = do_ep(second_texts[i])[8:12]
        for j in get_prob_parts_of_round_key(exr1, exr2, prob_inputs):
            result_row[btod(j)] += 1

    more_prob_parts_of_round_key = []
    max_value = max(result_row)
    for i in range(len(result_row)):
        if result_row[i] == max_value:
            more_prob_parts_of_round_key.append(dtob(i, 4))
    return more_prob_parts_of_round_key


def analyze_round(first_texts, second_texts, delta_a, delta_c):
    first_parts = analyze_round_key_part(1, first_texts, second_texts, delta_a[0:4], delta_c[0:3])
    second_parts = analyze_round_key_part(2, first_texts, second_texts, delta_a[4:8], delta_c[3:6])
    third_parts = analyze_round_key_part(3, first_texts, second_texts, delta_a[8:12], delta_c[6:8])
    probable_round_keys = [''.join(i) for i in list(product(first_parts, second_parts, third_parts))]
    return probable_round_keys


def post_analyze(delta_a, delta_c, xr1_lst, xr2_lst, yr1_lst, yr2_lst):
    prob_round1_keys = analyze_round(xr1_lst, xr2_lst, delta_a, delta_c)
    prob_round3_keys = analyze_round(yr1_lst, yr2_lst, delta_a, delta_c)
    prob_keys = [''.join(i) for i in list(product(prob_round1_keys, prob_round3_keys))]
    return prob_keys