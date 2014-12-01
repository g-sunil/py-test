#!/usr/bin/python

import csv
import sys


# http://www.linuxtopia.org/online_books/programming_books/python_programming/python_ch16s03.html
# http://www.python-course.eu/sets_frozensets.php
# http://www.dotnetperls.com/set-python
def createItemsDict():
    itemRestPrice = {}
    itemPrice = {}
    item = {}
    cr = csv.reader(open("/gsunil/py-learn/py-test-loc/report/jurgensville_testcase_98441.csv", "rb"))
    for row in cr:
        if row:
            row[0] = int(row[0])
            row[1] = float(row[1])
            row[2:] = [i.lower().strip() for i in row[2:]]
            if row[0] in itemRestPrice:
                ek = 1
                if row[1] in itemPrice:
                    ek = max(itemPrice[row[1]].keys()) + 1
                    itemPrice[row[1]].update({ek: row[2:]})
                else:
                    item = {1: row[2:]}
                    temp = {row[1]: item}
                    itemRestPrice[row[0]].update(temp)
            else:
                item = {1: row[2:]}
                itemPrice = {row[1]: item}
                itemRestPrice.update({row[0]: itemPrice})
    return itemRestPrice


def comboSelect(price, items, items_det, asked):
    price_list = []
    for pri, itmd in items_det.iteritems():
        temp = []
        c = 0
        for itm in itmd:
            c += 1
            temp.extend(items)
            temp.extend(itmd[itm])
            if asked.issubset(set(temp)):
                t = (pri*c) + price
                price_list.append(t)
    return min(price_list) if price_list else 0


def comboSrch(allPriceDet, asked):
    id_minprice = {}
    res_ans = {}
    for idx, val in allPriceDet.iteritems():
        price_vals = []
        for pri, itmd in val.iteritems():
            for itm in itmd:
                vl = comboSelect(pri, itmd[itm], val, asked)
                if vl:
                    price_vals.append(vl)
                    id_minprice[idx] = price_vals
    res_det = dict([(i, min(id_minprice[i])) for i in id_minprice])
    if res_det:
        res_minV = min(res_det.values())
        for i, j in res_det.iteritems():
            if res_minV == j:
                res_ans = {i: j}
    return res_ans


def itemsAtOnePlace(itemRestPrice, asked):
    avlItem = {}
    ret = {}
    for ii in itemRestPrice:
        avlItem[ii] = []
        for jj, k in itemRestPrice[ii].iteritems():
            for m, nn in k.iteritems():
                setN = set(nn)
                if asked.issubset(setN) or setN == asked:
                    avlItem[ii].append(jj)
        if avlItem[ii]:
            avlItem[ii] = min(avlItem[ii])
    avlMin = min(avlItem.values())
    if avlItem > 1 and avlMin != []:
        for i, j in avlItem.iteritems():
            if avlMin == j:
                ret = {i: j}
    return ret


def main():
    """Method to find less price
    either single or in combo selection
    of the items in a hotel"""
    asked = set([i.lower().strip() for i in sys.argv[1:]])
    itemRestPrice = createItemsDict()
    res_set_sing = itemsAtOnePlace(itemRestPrice, asked)
    res_set_srch = comboSrch(itemRestPrice, asked)
    f_res = {}
    if res_set_sing and res_set_srch:
        minV = min(res_set_sing.values(), res_set_srch.values())
        for i, j in res_set_sing.iteritems():
            if j == minV[0]:
                f_res[i] = j
        for i, j in res_set_srch.iteritems():
            if j == minV[0]:
                f_res[i] = j
    elif res_set_sing and not res_set_srch:
        f_res = res_set_sing
    elif res_set_srch and not res_set_sing:
        f_res = res_set_srch
    else:
        "I think to try again"
    if not f_res:
        print "No Result"
    else:
        print '{Restaurant ID: Price} = ', f_res

if __name__ == "__main__":
    sys.exit(main())
