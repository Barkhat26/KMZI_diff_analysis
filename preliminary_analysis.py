from encryption import do_s1, do_s2, do_s3, do_ep, do_p
from utils import dtob, btod, parse
from collections import Counter
from itertools import product
from init_data import E_PERM

def get_most_probable_delta_a_delta_c_for_block(lst):
    result = []
    maximum = max([i[1] for i in lst])
    for i in range(len(lst)):
        if lst[i][1] == maximum: result.append((dtob(i+1, 4), lst[i][0]))
    return result


def analyze_s1_block():
    delta_c_count = []
    input_block1 = [dtob(i, 4) for i in range(16)]
    output_block1 = [do_s1(i) for i in input_block1]
    for delta_a in [dtob(i, 4) for i in range(16)]:
        input_block2 = [dtob(btod(i) ^ btod(delta_a), 4) for i in input_block1]
        output_block2 = [do_s1(i) for i in input_block2]
        delta_c = list(map(lambda x, y: dtob(btod(x) ^ btod(y), 3), output_block1, output_block2))
        delta_c_count.append(Counter(delta_c).most_common(1)[0])
    return get_most_probable_delta_a_delta_c_for_block(delta_c_count[1:])


def analyze_s2_block():
    delta_c_count = []
    input_block1 = [dtob(i, 4) for i in range(16)]
    output_block1 = [do_s2(i) for i in input_block1]
    for delta_a in [dtob(i, 4) for i in range(16)]:
        input_block2 = [dtob(btod(i) ^ btod(delta_a), 4) for i in input_block1]
        output_block2 = [do_s2(i) for i in input_block2]
        delta_c = list(map(lambda x, y: dtob(btod(x) ^ btod(y), 3), output_block1, output_block2))
        delta_c_count.append(Counter(delta_c).most_common(1)[0])
    return get_most_probable_delta_a_delta_c_for_block(delta_c_count[1:])


def analyze_s3_block():
    delta_c_count = []
    input_block1 = [dtob(i, 4) for i in range(16)]
    output_block1 = [do_s3(i) for i in input_block1]
    for delta_a in [dtob(i, 4) for i in range(16)]:
        input_block2 = [dtob(btod(i) ^ btod(delta_a), 4) for i in input_block1]
        output_block2 = [do_s3(i) for i in input_block2]
        delta_c = list(map(lambda x, y: dtob(btod(x) ^ btod(y), 2), output_block1, output_block2))
        delta_c_count.append(Counter(delta_c).most_common(1)[0])
    return get_most_probable_delta_a_delta_c_for_block(delta_c_count[1:])


def get_probable_delta_a_delta_c(s1_anal, s2_anal, s3_anal):
    delta_a_lst = [''.join(i) for i in list(product([i[0] for i in s1_anal], [i[0] for i in s2_anal], [i[0] for i in s3_anal]))]
    delta_c_lst = [''.join(i) for i in list(product([i[1] for i in s1_anal], [i[1] for i in s2_anal], [i[1] for i in s3_anal]))]
    return delta_a_lst, delta_c_lst


def verify_prob_delta_a(prob_delta_a):
    buf = ''
    for i in E_PERM[8:12]:
        buf += prob_delta_a[E_PERM[0:8].index(i)]
    if buf != prob_delta_a[8:12]: return False
    return True


def get_right_delta_a_delta_c(s1_analysis, s2_analysis, s3_analysis):
    prob_delta_a_lst, prob_delta_c_lst = get_probable_delta_a_delta_c(s1_analysis, s2_analysis, s3_analysis)
    delta_a = None
    delta_c = None
    for i in prob_delta_a_lst:
        if verify_prob_delta_a(i):
            delta_a = i
            delta_c = prob_delta_c_lst[prob_delta_a_lst.index(i)]
    return delta_a, delta_c


def get_delta_xr(delta_a):
    delta_xr = ''
    for i in range(1, 9):
        delta_xr += delta_a[E_PERM[0:8].index(i)]
    return delta_xr


def preliminary_analyze():
    s1_analysis = analyze_s1_block()
    s2_analysis = analyze_s2_block()
    s3_analysis = analyze_s3_block()
    delta_a, delta_c = get_right_delta_a_delta_c(s1_analysis, s2_analysis, s3_analysis)
    delta_xr = get_delta_xr(delta_a)
    delta_d = do_p(delta_c)
    return delta_a, delta_c, delta_xr, delta_d
