#!/usr/bin/python

import csv
import sys
import pprint


# http://www.linuxtopia.org/online_books/programming_books/python_programming/python_ch16s03.html
# http://www.python-course.eu/sets_frozensets.php
# http://www.dotnetperls.com/set-python
def createItemsDict():
    itemRestPrice = {}
    itemPrice = {}
    item = {}
    cr = csv.reader(open("sample_data_5.csv", "rb"))
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


def comboSrch(allPriceDet, asked):
    ret = {}
    for idx, val in allPriceDet.iteritems():
        allPrice = val.keys()
        items = []
        itemsPrice = []
        itemSubPri = []
        thePric = dict([(i, 0) for i in asked])
        while allPrice != []:
            minV = min(allPrice)
            temp = [kk for k in val[minV].values() for kk in k if kk in asked]
            if temp:
                tempPrice = len(val[minV]) * minV
                avgVal = minV/len(val[minV].values())
                for i in temp:
                    if thePric[i]:
                        if avgVal < thePric[i]:
                            thePric[i] = avgVal  # val is min then the existing so replacing
                            # t = tempPrice - avgVal  # have to chk
                            # itemSubPri.append(avgVal)  # added to list to substracting the val
                    else:
                        thePric[i] = avgVal
                if avgVal <= sum([thePric[i] or 0 for i in temp]):
                    items.extend(temp)
                    itemsPrice.append(tempPrice)
            if set(items) == asked:
                ret[idx] = sum(itemsPrice) - sum(itemSubPri)
                allPrice = []
            else:
                allPrice.remove(minV)
    ret = dict([(i, j) for i, j in ret.iteritems() if j == min(ret.values())])
    return ret


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
    pprint.pprint(itemRestPrice)
    res_set_sing = itemsAtOnePlace(itemRestPrice, asked)
    res_set_srch = comboSrch(itemRestPrice, asked)
    print res_set_sing, res_set_srch

if __name__ == "__main__":
    sys.exit(main())
