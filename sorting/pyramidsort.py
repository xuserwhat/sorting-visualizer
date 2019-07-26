import copy
from .data import Data
import math

H = []

def pyramid_sort(data_set):
    frames = [data_set]
    ds = copy.deepcopy(data_set)
    pyramidize_min(ds, frames, 0, len(ds), len(ds))
    frames.append(copy.deepcopy(ds))
    return frames

def pyramidize_min(h, frames, cut, delta, length):
    if len(h) == 1 or len(h) == 0:
        return h
    h0 = getdepth(h, 0, 1)
    i = int(math.floor(len(h) / 2)) - 1
    while i != -1:
        heapify_min(h, i, frames, cut, delta)
        i -= 1
    X = h
    for i in range(1, h0 + 1):
        pc1 = int(math.pow(2, i - 1))
        pc2 = pc1 << 1
        if i == h0:
            if len(h) == length:
                globalH = H
                globalH = copy.deepcopy(h)
            X[(pc1 - 1):(len(h))] = pyramidize_min(h[(pc1 - 1):(len(h))], frames, cut + (pc1 - 1), len(h) - (pc1 - 1), length)
        else:
            if len(h) == length:
                globalH = H
                globalH = copy.deepcopy(h)
            X[(pc1 - 1):(pc2 - 1)] = pyramidize_min(h[(pc1 - 1):(pc2 - 1)], frames, cut + (pc1 - 1), (pc2) - (pc1), length)
    for i in range(1, h0):
        pc1 = int(math.pow(2, i - 1))
        pc2 = pc1 << 1
        pc3 = pc2 << 1
        if i == h0 - 1:
            M = merge_min(X[(pc1 - 1):(pc2 - 1)], X[(pc2 - 1):(len(h))])
            
            X[(pc1 - 1):(len(h))] = M[0:(len(h) - pc1 + 1)]
            globalH = H
            globalH[cut:cut + delta] = copy.deepcopy(X)
            frames.append(copy.deepcopy(H))
        else:
            M = merge_min(X[(pc1 - 1):(pc2 - 1)], X[(pc2 - 1):(pc3 - 1)])
            X[(pc1 - 1):(pc3 - 1)] = M[0:(pc3 - pc1)]
            globalH = H
            globalH[cut:cut + delta] = copy.deepcopy(X)
            frames.append(copy.deepcopy(H))
    return X

def heapify_min(h, i, frames, cut, delta):
    visit = i
    while True:
        least = visit
        if 2*visit + 1 < len(h) and h[least].value > h[2*visit + 1].value:
            least = 2*visit + 1
        if 2*visit + 2 < len(h) and h[least].value > h[2*visit + 2].value:
            least = 2*visit + 2
        if visit != least:
            tmp = h[least]
            h[least] = h[visit]
            h[visit] = tmp
            H[cut:cut + delta] = copy.deepcopy(h)
            frames.append(copy.deepcopy(H))
            visit = least
        else:
            break

def merge_min(x, y):
    X = copy.deepcopy(x)
    Y = copy.deepcopy(y)
    M = []
    while len(X) != 0 and len(Y) != 0:
        if X[0].value > Y[0].value:
            M.append(Y[0])
            Y.pop()
        else:
            M.append(X[0])
            X.pop()
    
    if len(X) == 0:
        return M + Y
    else:
        return M + X

def getdepth(t, i, depth):
    if 2*i + 1 >= len(t):
        return depth
    else:
        ldepth = getdepth(t, 2*i + 1, depth + 1)
        rdepth = 0
        if 2*i + 2 < len(t):
            rdepth = getdepth(t, 2*i + 2, depth + 1)
        if ldepth > rdepth:
            return ldepth
        else:
            return rdepth

def find_min(p, height):
    h0 = getdepth(p, 0, 1)
    return p[int(math.pow(2, h0 - height)) - 1]

def find_max(p, height):
    if height > 1:
        h0 = getdepth(p, 0, 1)
        return p[int(math.pow(2, h0 + 1 - height)) - 2]
    else:
        return p[len(p) - 1]

def insert(p, x):
    merge_min(p, [x])

def status(p):
    if len(p) > 1:
        s = 0
        h0 = getdepth(p, 0, 1)
        for i in range(h0, 2, -1):
            max = find_max(p, i)
            min = find_min(p, i - 1)
            print(max)
            print(min)
            if max <= min and ((s == 0 and i == h0) or s == 1):
                s = 1
            elif max >= min and ((s == 0 and i == h0) or s == 2):
                s = 2
            else:
                return 0
        return s
    else:
        return 0
