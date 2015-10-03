#!/usr/bin/env python3
import copy

table = [[0, 0, 0, 4, 7, 0, 0, 8, 0],
         [7, 9, 4, 0, 8, 0, 0, 3, 0],
         [0, 0, 8, 0, 0, 5, 4, 0, 7],
         [4, 1, 2, 0, 0, 7, 0, 0, 8],
         [9, 0, 0, 8, 2, 4, 1, 7, 5],
         [5, 8, 7, 9, 0, 0, 3, 4, 2],
         [0, 0, 0, 7, 0, 0, 8, 2, 3],
         [3, 0, 0, 0, 0, 8, 0, 1, 0],
         [8, 0, 0, 0, 0, 3, 0, 5, 0]]

pos = {i for i in range(10)}


def test_explicit(wsp, tab):  # returns list of candidates according to game's rules
    i, j = wsp
    square_x = i - i % 3
    square_y = j - j % 3
    candidates_col = pos.copy()
    candidates_row = pos.copy()
    candidates_square = pos.copy()
    range_row = [ii for ii in range(j)] + [ii for ii in range(j + 1, 9)]
    range_col = [ii for ii in range(i)] + [ii for ii in range(i + 1, 9)]
    for ii in range_col:
        try:
            candidates_col.remove(tab[ii][j])
        except:
            pass
    for ii in range_row:
        try:
            candidates_row.remove(tab[i][ii])
        except:
            pass
    for ii in range(square_x, square_x + 3):
        for jj in range(square_y, square_y + 3):
            try:
                candidates_square.remove(tab[ii][jj])
            except:
                pass
    return candidates_square & candidates_col & candidates_row


def naive_test(tab):
    l = len(tab)
    for i in range(l):
        for j in range(l):
            a = candidates([i, j], tab)
            if len(a) == 1:
                tab[i][j] = a.pop()
    for i in range(1, 10):
        for j in range(9):  # cols
            if i in [a[j] for a in tab]: continue
            prop = None
            for k in range(9):  # position in col
                if i in candidates([k, j], tab):
                    if prop == None:
                        prop = k
                    else:
                        prop = None
                        break
            if prop != None:
                tab[prop][j] = i
        for j in range(9):  # rows
            if i in [a for a in tab[j]]: continue
            prop = None
            for k in range(9):  # position in row
                if i in candidates([j, k], tab):
                    if prop == None:
                        prop = k
                    else:
                        prop = None
                        break
            if prop != None:
                tab[j][prop] = i
                pass
    return tab


def sophisticated_test(wsp, result, tab):
    i, j = wsp
    square_x_start = i - i % 3
    square_y_start = j - j % 3
    prop = result.copy()
    for ii in range(square_x_start, square_x_start + 3):
        for jj in range(square_y_start, square_y_start + 3):
            if i == ii and j == jj: continue
            rest = test_explicit([ii, jj], tab)
            for i in rest:
                try:
                    prop.remove(i)
                except:
                    pass
    if prop:
        return prop
    else:
        return result


def test_lets_dance(t):
    draft = copy.deepcopy(t)
    for i in range(len(draft)):
        for j in range(len(draft)):
            if draft[i][j] == 0:
                for k in test_explicit([i, j], draft):
                    print('dance for {},{}: {}'.format(i, j, k))
                    draft[i][j] = k
                    wyn = solve(draft)
                    if wyn != None:
                        return wyn
    return None


def draw(t):
    l = len(t)
    ret = '====' * l + '\n'
    for i in range(l):
        ret += ''.join(repr(t[i]).replace(', ', ' | ').replace('[', '| ').replace(']', ' |')) + '\n'
        if i % 3 == 2:
            ret += '====' * l + '\n'
        else:
            ret += '----' * l + '\n'
    ret = ret.replace('0', ' ')
    return ret


def candidates(k, tab):
    i, j = k
    if tab[i][j] != 0: return {}
    wyn = test_explicit(k, tab)
    result = sophisticated_test(k, wyn, tab)
    return result


def count_empty(t):
    result = 0
    for i in t:
        for j in i:
            if j == 0: result += 1
    return result


def solve(tab):
    tab = copy.deepcopy(tab)
    l = len(tab)
    t = count_empty(tab)
    hard = -10
    while t > 0:
        tab = naive_test(tab)
        t = count_empty(tab) - hard
        hard += 1
    if count_empty(tab) > 0:
        print("let's dance")
        tab = test_lets_dance(tab)
    if tab == None or count_empty(tab) > 0:
        return None
    else:
        return tab
    pass


print('initial state:\n', draw(table), sep='')
wyn = solve(table)
if wyn == None:
    print('no result');
    print(draw(table))
else:
    print('result:\n', draw(wyn), sep='')
