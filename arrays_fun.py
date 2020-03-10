import numpy as np
import pandas as pd


def get_cusum_df(in_arr):
    c1 = pd.Series(in_arr).cumsum()
    c2 = list(reversed(pd.Series(reversed(in_arr)).cumsum().values))
    c3 = in_arr

    max_fcs = c1.max()
    max_bcs = max(c2)

    fmi = c1.values.argmax()
    if c1.iloc[-1] < 0 and max_fcs >= max_bcs:
        bmi = pd.Series(c2[:fmi + 1]).values.argmax()
    elif c1.iloc[-1] < 0 and max_fcs < max_bcs:
        bmi = pd.Series(c2).values.argmax()
        fmi = c1.iloc[bmi:].values.argmax()
    else:
        if fmi == 0 and pd.Series(in_arr).argmax() != 0:
            fmi = c1.iloc[1:].values.argmax()
        bmi = pd.Series(c2[:-1]).values.argmax() if c2[-1] < 0 else pd.Series(c2).values.argmax()

    return bmi, fmi, pd.DataFrame({'csf': c1, 'csb': c2, 'orig': c3})


if __name__ == '__main__':
    arr = np.random.randint(-100, 100, 10)
    # arr = [89, -59, -75,  21,  41,  82,  -4, -78, -64, -96]
    # arr = [4, -97, -65,  88,  47, -31,  28, -66,  94, -99]
    # arr = [-56,  79, -38,  93, -95, -89, -82,  25,   7, -78]
    # arr = [-93,  56,  -3,   4, -42,  77, -77, -78,  55,  50]
    print(arr)
    bmi, fmi, res_df = get_cusum_df(arr)
    print('{} -> {}'.format(bmi, fmi))
    res_df['csdiff'] = res_df['csf'] - (res_df['csb'] - res_df['orig'])
    print(res_df)

    if bmi > fmi:
        result = arr[:fmi + 1] if res_df['csf'].max() >= res_df['csb'].max() else arr[bmi:]
        #     result = arr[:fmi + 1]
        # else:
        #     result = arr[bmi:]
    elif bmi == fmi:
        result = arr[bmi]
    else:
        result = arr[bmi:fmi + 1]

    print('result')
    print(result)
    print('res sum:')
    print(sum(result))


