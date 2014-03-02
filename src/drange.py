def drange(L, A):
    L.sort()
    i = 0
    iMax = len(L)
    r = L[i]
    isBelow = True
    while r < A:
        i += 1
        r = L[i]
    i -= 1
    return [L[j] for j in range(i,iMax)]
