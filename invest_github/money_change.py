def currency_change(data):
    data['real_money'] = 1
    for i in range(data.shape[0]):
        a = data.iloc[i, 7]
        if a == 'RMB':
            data.iloc[i, 13] = RMB_change(data.iloc[i, 8])
        if a == 'USD':
            data.iloc[i, 13] = USD_change(data.iloc[i, 8])
        if a == 'HKD':
            data.iloc[i, 13] = HKD_change(data.iloc[i, 8])
        if a == 'EUR':
            data.iloc[i, 13] = EUR_change(data.iloc[i, 8])
        if a == 'SGD':
            data.iloc[i, 13] = SGD_change(data.iloc[i, 8])
        if a == 'INR':
            data.iloc[i, 13] = INR_change(data.iloc[i, 8])
        if a == 'JPY':
            data.iloc[i, 13] = JPY_change(data.iloc[i, 8])
        if a == 'GBP':
            data.iloc[i, 13] = GBP_change(data.iloc[i, 8])
        if a == 'CAD':
            data.iloc[i, 13] = CAD_change(data.iloc[i, 8])
    return data


def RMB_change(x):
    import re
    a = re.findall('(\d+)', x)  # 匹配数字
    b = re.findall('\D+', x)  # 匹配字符串单位
    if len(a) == 1:
        if b[0] == '万':
            x = float(a[0]) * 10000
            return x
        if b[0] == '十万':
            x=float(a[0])*100000
            return x
        if b[0] == '百万':
            x = float(a[0]) * 1000000
            return x
        if b[0] == '千万':
            x = float(a[0]) * 10000000
            return x
        if b[0] == '亿':
            x = float(a[0]) * 100000000
            return x
    if len(a) == 2:
        if b[1] == '万':
            x = float('.'.join(a)) * 10000
            return x
        if b[1] == '百万':
            x = float('.'.join(a)) * 1000000
            return x
        if b[1] == '千万':
            x = float('.'.join(a)) * 10000000
            return x
        if b[1] == '亿':
            x = float('.'.join(a)) * 100000000
            return x
    if len(a) == 0:
        return b[0]


def USD_change(x):
    import re
    a = re.findall('(\d+)', x)  # 匹配数字
    b = re.findall('\D+', x)  # 匹配字符串单位
    if len(a) == 1:
        if b[0] == '万':
            x = float(a[0]) * 10000 * 6.5
            return x
        if b[0] == '十万':
            x=float(a[0]) * 100000 * 6.5
            return x
        if b[0] == '百万':
            x = float(a[0]) * 1000000 * 6.5
            return x
        if b[0] == '千万':
            x = float(a[0]) * 10000000 * 6.5
            return x
        if b[0] == '亿':
            x = float(a[0]) * 100000000 * 6.5
            return x
    if len(a) == 2:
        if b[1] == '万':
            x = float('.'.join(a)) * 10000 * 6.5
            return x
        if b[1] == '百万':
            x = float('.'.join(a)) * 1000000 * 6.5
            return x
        if b[1] == '千万':
            x = float('.'.join(a)) * 10000000 * 6.5
            return x
        if b[1] == '亿':
            x = float('.'.join(a)) * 100000000 * 6.5
            return x
    if len(a) == 0:
        return b[0]


def HKD_change(x):
    import re
    a = re.findall('(\d+)', x)  # 匹配数字
    b = re.findall('\D+', x)  # 匹配字符串单位
    if len(a) == 1:
        if b[0] == '万':
            x = float(a[0]) * 10000 * 0.8
            return x
        if b[0] == '十万':
            x = float(a[0]) * 100000 * 0.8
            return x
        if b[0] == '百万':
            x = float(a[0]) * 1000000 * 0.8
            return x
        if b[0] == '千万':
            x = float(a[0]) * 10000000 * 0.8
            return x
        if b[0] == '亿':
            x = float(a[0]) * 100000000 * 0.8
            return x
    if len(a) == 2:
        if b[1] == '万':
            x = float('.'.join(a)) * 10000 * 0.8
            return x
        if b[1] == '百万':
            x = float('.'.join(a)) * 1000000 * 0.8
            return x
        if b[1] == '千万':
            x = float('.'.join(a)) * 10000000 * 0.8
            return x
        if b[1] == '亿':
            x = float('.'.join(a)) * 100000000 * 0.8
            return x
    if len(a) == 0:
        return b[0]


def EUR_change(x):
    import re
    a = re.findall('(\d+)', x)  # 匹配数字
    b = re.findall('\D+', x)  # 匹配字符串单位
    if len(a) == 1:
        if b[0] == '万':
            x = float(a[0]) * 10000 * 7.8
            return x
        if b[0] == '十万':
            x = float(a[0]) * 100000 *7.8
            return x
        if b[0] == '百万':
            x = float(a[0]) * 1000000 * 7.8
            return x
        if b[0] == '千万':
            x = float(a[0]) * 10000000 * 7.8
            return x
        if b[0] == '亿':
            x = float(a[0]) * 100000000 * 7.8
            return x
    if len(a) == 2:
        if b[1] == '万':
            x = float('.'.join(a)) * 10000 * 7.8
            return x
        if b[1] == '百万':
            x = float('.'.join(a)) * 1000000 * 7.8
            return x
        if b[1] == '千万':
            x = float('.'.join(a)) * 10000000 * 7.8
            return x
        if b[1] == '亿':
            x = float('.'.join(a)) * 100000000 * 7.8
            return x
    if len(a) == 0:
        return b[0]


def GBP_change(x):
    import re
    a = re.findall('(\d+)', x)  # 匹配数字
    b = re.findall('\D+', x)  # 匹配字符串单位
    if len(a) == 1:
        if b[0] == '万':
            x = float(a[0]) * 10000 * 9
            return x
        if b[0] == '十万':
            x = float(a[0]) * 100000 * 9
            return x
        if b[0] == '百万':
            x = float(a[0]) * 1000000 * 9
            return x
        if b[0] == '千万':
            x = float(a[0]) * 10000000 * 9
            return x
        if b[0] == '亿':
            x = float(a[0]) * 100000000 * 9
            return x
    if len(a) == 2:
        if b[1] == '万':
            x = float('.'.join(a)) * 10000 * 9
            return x
        if b[1] == '百万':
            x = float('.'.join(a)) * 1000000 * 9
            return x
        if b[1] == '千万':
            x = float('.'.join(a)) * 10000000 * 9
            return x
        if b[1] == '亿':
            x = float('.'.join(a)) * 100000000 * 9
            return x
    if len(a) == 0:
        return b[0]


def SGD_change(x):
    import re
    a = re.findall('(\d+)', x)  # 匹配数字
    b = re.findall('\D+', x)  # 匹配字符串单位
    if len(a) == 1:
        if b[0] == '万':
            x = float(a[0]) * 10000 * 4.8
            return x
        if b[0] == '十万':
            x = float(a[0]) * 100000 * 4.8
            return x
        if b[0] == '百万':
            x = float(a[0]) * 1000000 * 4.8
            return x
        if b[0] == '千万':
            x = float(a[0]) * 10000000 * 4.8
            return x
        if b[0] == '亿':
            x = float(a[0]) * 100000000 * 4.8
            return x
    if len(a) == 2:
        if b[1] == '万':
            x = float('.'.join(a)) * 10000 * 4.8
            return x
        if b[1] == '百万':
            x = float('.'.join(a)) * 1000000 * 4.8
            return x
        if b[1] == '千万':
            x = float('.'.join(a)) * 10000000 * 4.8
            return x
        if b[1] == '亿':
            x = float('.'.join(a)) * 100000000 * 4.8
            return x
    if len(a) == 0:
        return b[0]


def JPY_change(x):
    import re
    a = re.findall('(\d+)', x)  # 匹配数字
    b = re.findall('\D+', x)  # 匹配字符串单位
    if len(a) == 1:
        if b[0] == '万':
            x = float(a[0]) * 10000 * 0.06
            return x
        if b[0] == '十万':
            x = float(a[0]) * 100000 * 0.06
            return x
        if b[0] == '百万':
            x = float(a[0]) * 1000000 * 0.06
            return x
        if b[0] == '千万':
            x = float(a[0]) * 10000000 * 0.06
            return x
        if b[0] == '亿':
            x = float(a[0]) * 100000000 * 0.06
            return x
    if len(a) == 2:
        if b[1] == '万':
            x = float('.'.join(a)) * 10000 * 0.06
            return x
        if b[1] == '百万':
            x = float('.'.join(a)) * 1000000 * 0.06
            return x
        if b[1] == '千万':
            x = float('.'.join(a)) * 10000000 * 0.06
            return x
        if b[1] == '亿':
            x = float('.'.join(a)) * 100000000 * 0.06
            return x
    if len(a) == 0:
        return b[0]


def CAD_change(x):
    import re
    a = re.findall('(\d+)', x)  # 匹配数字
    b = re.findall('\D+', x)  # 匹配字符串单位
    if len(a) == 1:
        if b[0] == '万':
            x = float(a[0]) * 10000 * 5.1
            return x
        if b[0] == '十万':
            x = float(a[0]) * 100000 * 5.1
            return x
        if b[0] == '百万':
            x = float(a[0]) * 1000000 * 5.1
            return x
        if b[0] == '千万':
            x = float(a[0]) * 10000000 * 5.1
            return x
        if b[0] == '亿':
            x = float(a[0]) * 100000000 * 5.1
            return x
    if len(a) == 2:
        if b[1] == '万':
            x = float('.'.join(a)) * 10000 * 5.1
            return x
        if b[1] == '百万':
            x = float('.'.join(a)) * 1000000 * 5.1
            return x
        if b[1] == '千万':
            x = float('.'.join(a)) * 10000000 * 5.1
            return x
        if b[1] == '亿':
            x = float('.'.join(a)) * 100000000 * 5.1
            return x
    if len(a) == 0:
        return b[0]


def INR_change(x):
    import re
    a = re.findall('(\d+)', x)  # 匹配数字
    b = re.findall('\D+', x)  # 匹配字符串单位
    if len(a) == 1:
        if b[0] == '万':
            x = float(a[0]) * 10000 * 0.08
            return x
        if b[0] == '十万':
            x = float(a[0]) * 100000 * 0.08
            return x
        if b[0] == '百万':
            x = float(a[0]) * 1000000 * 0.08
            return x
        if b[0] == '千万':
            x = float(a[0]) * 10000000 * 0.08
            return x
        if b[0] == '亿':
            x = float(a[0]) * 100000000 * 0.08
            return x
    if len(a) == 2:
        if b[1] == '万':
            x = float('.'.join(a)) * 10000 * 0.08
            return x
        if b[1] == '百万':
            x = float('.'.join(a)) * 1000000 * 0.08
            return x
        if b[1] == '千万':
            x = float('.'.join(a)) * 10000000 * 0.08
            return x
        if b[1] == '亿':
            x = float('.'.join(a)) * 100000000 * 0.08
            return x
    if len(a) == 0:
        return b[0]

