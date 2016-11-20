from encryption import encrypt
from preliminary_analysis import preliminary_analyze
from post_analysis import post_analyze
from utils import parse


def main():
    delta_a, delta_c, delta_xr, delta_d = preliminary_analyze()
    print('Results of preliminary analysis:')
    print('Delta XR(YR): {}: '.format(delta_xr))
    print('Delta XL: {}: '.format(delta_d))
    print('Enter these values into a program for generation text pairs and after press Enter...')
    input()
    xl1_lst, xr1_lst, yl1_lst, yr1_lst, xl2_lst, xr2_lst, yl2_lst, yr2_lst = parse()
    for i in range(7, len(xl1_lst)):
        prob_keys = post_analyze(delta_a, delta_c, xr1_lst[0:i], xr2_lst[0:i], yr1_lst[0:i], yr2_lst[0:i])

        input_block = xl1_lst[0] + xr1_lst[0]
        output_block = yl1_lst[0] + yr1_lst[0]
        for k in prob_keys:
            if output_block == encrypt(input_block, k):
                print('Found key: {}'.format(k))
                print('Used {} text pairs'.format(i))
                exit(0)
    print('Not found a key')

if __name__ == '__main__':
    main()
