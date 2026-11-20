# tiny-chess-01 agent: chess engine + env agent loop
import json, os, sys, urllib.request as U, urllib.error as E

# ---------- chess engine ----------
B = [0] * 64
cast = 0
ep = -1
kings = [-1, -1]

def sq(f, r): return r * 8 + f
def tk(p): return p >> 3
def cl(p): return p & 1

def empty():
    global B, cast, ep, kings
    B = [0] * 64; cast = 0; ep = -1; kings = [-1, -1]

def start():
    empty()
    back = (32, 16, 24, 40, 48, 24, 16, 32)
    for i in range(8):
        B[sq(i, 7)] = back[i]; B[sq(i, 0)] = back[i] | 1
    for f in range(8):
        B[sq(f, 6)] = 8; B[sq(f, 1)] = 9
    kings[:] = [sq(4, 7), sq(4, 0)]

def setup(fen):
    global B, cast, ep, kings
    empty()
    p = fen.split(); rows = p[0].split('/')
    for r in range(8):
        f = 0
        for ch in rows[r]:
            if ch.isdigit():
                f += int(ch); continue
            c = ch.lower(); t = 'pnbrqk'.find(c) + 1
            col = 0 if ch.isupper() else 1
            B[sq(f, 7 - r)] = t | (col << 3); f += 1
    cast = 0
    for ch in p[2]:
        if ch in 'KQkq': cast |= 1 << 'KQkq'.find(ch)
    if p[3] != '-':
        ep = sq('abcdefgh'.find(p[3][0]), 7 - int(p[3][1]))
    for s in range(64):
        p2 = B[s]
        if p2 and tk(p2) == 6: kings[cl(p2)] = s

def attacked(s, by):
    if not (0 <= s < 64) or not B[s]: return False
    p = B[s]; t = tk(p); c = cl(p)
    for d in (17, 15, 10, 6, -17, -15, -10, -6):
        q = s + d
        if 0 <= q < 64 and B[q] and tk(B[q]) == 2 and cl(B[q]) == by: return True
    code = 8 if by == 0 else 9
    if by == 0:
        if (s % 8 < 7 and s >= 7 and B[s - 7] == code) or (s % 8 > 0 and s >= 9 and B[s - 9] == code): return True
    else:
        if (s % 8 < 7 and s + 7 < 64 and B[s + 7] == code) or (s % 8 > 0 and s + 9 < 64 and B[s + 9] == code): return True
    for d in (1, 8, -1, -8, 7, 9, -7, -9):
        q = s + d
        while 0 <= q < 64 and not B[q]: q += d
        if 0 <= q < 64 and B[q] and cl(B[q]) == by:
            if t == 4 and d in (1, 8, -1, -8): return True
            if t == 2 and d in (7, 9, -7, -9): return True
            if t == 5 and d in (1, 8, -1, -8, 7, 9, -7, -9): return True
    return False

def in_check(side):
    s = kings[side]
    return s >= 0 and attacked(s, side ^ 1)

def gen(side):
    L = []
    for s in range(64):
        p = B[s]
        if not p: continue
        t = tk(p); c = cl(p)
        if c != side: continue
        if t == 1:
            d = -8 if side == 0 else 8
            if 0 <= s + d < 64 and not B[s + d]:
                if (s // 8) == (6 if side == 0 else 1) and not B[s + 2 * d]:
                    L.append((s << 12) | ((s + 2 * d) << 6) | 2)
                L.append((s << 12) | ((s + d) << 6) | 0)
            for ds in ((-9, 7) if side == 0 else (7, 9)):
                q = s + ds
                if 0 <= q < 64 and abs((q % 8) - (s % 8)) == 1 and B[q] and cl(B[q]) != c:
                    L.append((s << 12) | (q << 6) | 0)
            if ep >= 0 and s // 8 in (3, 4):
                if ep == s - 7 and s % 8 < 7 and B[s + 1] == 9: L.append((s << 12) | (ep << 6) | 0)
                if ep == s - 9 and s % 8 > 0 and B[s - 1] == 9: L.append((s << 12) | (ep << 6) | 0)
        elif t == 2:
            for d in (17, 15, 10, 6, -17, -15, -10, -6):
                q = s + d
                if 0 <= q < 64 and abs((q % 8) - (s % 8)) <= 2 and (not B[q] or cl(B[q]) != c):
                    L.append((s << 12) | (q << 6) | 0)
        elif t == 3:
            for d in (7, 9, -7, -9):
                q = s + d
                while 0 <= q < 64:
                    qv = B[q]
                    if not qv: break
                    if cl(qv) != c and tk(qv) == 3: L.append((s << 12) | (q << 6) | 0)
                    elif cl(qv) == c: break
                    q += d
        elif t == 4:
            for d in (1, 8, -1, -8):
                q = s + d
                while 0 <= q < 64:
                    qv = B[q]
                    if not qv: break
                    if cl(qv) != c and tk(qv) == 4: L.append((s << 12) | (q << 6) | 0)
                    elif cl(qv) == c: break
                    q += d
        elif t == 5:
            for d in (1, 8, -1, -8, 7, 9, -7, -9):
                q = s + d
                while 0 <= q < 64:
                    qv = B[q]
                    if not qv: break
                    if cl(qv) != c and tk(qv) == 5: L.append((s << 12) | (q << 6) | 0)
                    elif cl(qv) == c: break
                    q += d
        elif t == 6:
            for d in (1, 8, -1, -8, 7, 9, -7, -9):
                q = s + d
                if 0 <= q < 64 and (not B[q] or cl(B[q]) != c): L.append((s << 12) | (q << 6) | 0)
            if c == 0:
                if cast & 1 and not B[sq(5, 7)] and not B[sq(6, 7)] and not in_check(0): L.append((sq(4, 7) << 12) | (sq(6, 7) << 6) | 0)
                if cast & 2 and not B[sq(3, 7)] and not B[sq(2, 7)] and not B[sq(1, 7)] and not in_check(0): L.append((sq(4, 7) << 12) | (sq(2, 7) << 6) | 0)
            else:
                if cast & 4 and not B[sq(5, 0)] and not B[sq(6, 0)] and not in_check(1): L.append((sq(4, 0) << 12) | (sq(6, 0) << 6) | 0)
                if cast & 8 and not B[sq(3, 0)] and not B[sq(2, 0)] and not B[sq(1, 0)] and not in_check(1): L.append((sq(4, 0) << 12) | (sq(2, 0) << 6) | 0)
    return L

def make(m):
    global B, cast, ep
    f = m >> 12; t = m >> 6 & 63; pr = m & 3
    p = B[f]; c = cl(p); t0 = tk(p)
    ep_old = ep
    B[f] = 0; B[t] = p
    if t0 == 1:
        if t - f == 16: ep = f + 8
        elif f - t == 16: ep = f - 8
        else: ep = -1
    else: ep = -1
    if t0 == 6:
        if c == 0: cast &= 12
        else: cast &= 3
    elif t0 == 4:
        if f == sq(7, 7): cast &= 254
        if f == sq(0, 7): cast &= 253
        if f == sq(7, 0): cast &= 251
        if f == sq(0, 0): cast &= 247

def unmake(m):
    global B, cast, ep
    f = m >> 12; t = m >> 6 & 63; pr = m & 3
    p = B[t]; c = cl(p); t0 = tk(p)
    B[t] = 0; B[f] = p
    ep = ep_old if False else 0
