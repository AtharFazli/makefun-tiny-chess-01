# tiny-chess-01 agent: chess engine + env agent loop
import json, os, sys, urllib.request as U, urllib.error as E

# ---------- chess engine ----------
B = [0] * 64
cast = 0
ep = -1
ep_cap = -1
cast_save = 0
kings = [-1, -1]

def sq(f, r): return r * 8 + f
def tk(p): return p >> 3
def cl(p): return p & 1

def empty():
    global B, cast, ep, ep_cap, cast_save, kings
    B = [0] * 64; cast = 0; ep = -1; ep_cap = -1; cast_save = 0; kings = [-1, -1]

def start():
    empty()
    back = (32, 16, 24, 40, 48, 24, 16, 32)
    for i in range(8):
        B[sq(i, 7)] = back[i]; B[sq(i, 0)] = back[i] | 1
    for f in range(8):
        B[sq(f, 6)] = 8; B[sq(f, 1)] = 9
    cast = 15; kings[:] = [sq(4, 7), sq(4, 0)]

def setup(fen):
    global B, cast, ep, ep_cap, cast_save, kings
    empty()
    p = fen.split(); rows = p[0].split('/')
    for r in range(8):
        f = 0
        for ch in rows[r]:
            if ch.isdigit():
                f += int(ch); continue
            c = ch.lower(); t = 'pnbrqk'.find(c) + 1
            col = 0 if ch.isupper() else 1
            B[sq(f, r)] = (t << 3) | col; f += 1
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
    for d in (17, 15, 10, 6, -17, -15, -10, -6):
        q = s + d
        if 0 <= q < 64 and B[q] and tk(B[q]) == 2 and cl(B[q]) == by: return True
    code = 8 if by == 0 else 9
    if by == 0:
        if (s % 8 < 7 and s >= 7 and B[s - 7] == code) or (s % 8 > 0 and s >= 9 and B[s - 9] == code): return True
    else:
        if (s % 8 < 7 and s + 7 < 64 and B[s + 7] == code) or (s % 8 > 0 and s + 9 < 64 and B[s + 9] == code): return True
    for d in (1, 8, -1, -8):
        q = s + d
        while 0 <= q < 64 and not B[q]: q += d
        if 0 <= q < 64 and B[q] and cl(B[q]) == by and tk(B[q]) in (4, 5): return True
    for d in (7, 9, -7, -9):
        q = s + d
        while 0 <= q < 64 and not B[q]: q += d
        if 0 <= q < 64 and B[q] and cl(B[q]) == by and tk(B[q]) in (3, 5): return True
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
    global B, cast, ep, ep_cap, cast_save, ep_old
    f = m >> 12; t = m >> 6 & 63; pr = m & 3
    p = B[f]; c = cl(p); t0 = tk(p)
    ep_old = ep; ep_cap = -1
    B[f] = 0; B[t] = p
    if t0 == 1:
        if t - f == 16: ep = f + 8
        elif f - t == 16: ep = f - 8
        else:
            ep = -1
            if ep_old >= 0 and t == ep_old: ep_cap = (t + 8) if c == 0 else (t - 8)
    else: ep = -1
    if t0 == 6:
        if c == 0: cast &= 12
        else: cast &= 3
    elif t0 == 4:
        if f == sq(7, 7): cast &= 254
        if f == sq(0, 7): cast &= 253
        if f == sq(7, 0): cast &= 251
        if f == sq(0, 0): cast &= 247
    cast_save = cast

def unmake(m):
    global B, cast, ep, ep_cap, ep_old
    f = m >> 12; t = m >> 6 & 63; pr = m & 3
    p = B[t]; c = cl(p); t0 = tk(p)
    B[t] = 0; B[f] = p
    if ep_cap >= 0: B[ep_cap] = 0
    if t0 == 6:
        if c == 0: cast |= 12
        else: cast |= 3
    elif t0 == 4:
        if f == sq(7, 7): cast |= 1
        if f == sq(0, 7): cast |= 2
        if f == sq(7, 0): cast |= 4
        if f == sq(0, 0): cast |= 8
    ep = ep_old

def uc(m):
    f1 = m >> 12; r1 = f1 >> 3
    f2 = m >> 6 & 63; r2 = f2 >> 3
    return 'abcdefgh'[f1 & 7] + str(8 - r1) + 'abcdefgh'[f2 & 7] + str(8 - r2) + 'pnbrq'[m & 3]

def parse_uci(uci):
    f1 = 'abcdefgh'.find(uci[0]); r1 = 8 - int(uci[1])
    f2 = 'abcdefgh'.find(uci[2]); r2 = 8 - int(uci[3])
    promo = 'nbrq'.find(uci[4]) if len(uci) > 4 else 0
    return (sq(f1, r1) << 12) | (sq(f2, r2) << 6) | promo

# ---------- evaluation & search ----------
MAT = [0, 100, 320, 330, 500, 900, 0]
PA = [0, 0, 20, 30, 35, 40, 30, 0]
PF = [0, 10, 15, 20, 20, 15, 10, 0]

def evaluate():
    score = 0
    for s in range(64):
        p = B[s]
        if not p: continue
        t = tk(p); c = cl(p)
        if t == 6: continue
        val = MAT[t]
        r = s >> 3; f = s & 7
        if t == 1:
            val += PA[r] + PF[f]
        elif t == 2:
            val += 6 * (7 - abs(r - 3) - abs(f - 3))
        elif t == 3:
            val += 5 * (7 - abs(r - 3) - abs(f - 3))
        elif t == 4:
            val += 8 if r == 6 else (4 if f in (3, 4) and r == 0 else 0)
        elif t == 5:
            val += 3 * (7 - abs(r - 3) - abs(f - 3))
        score += val if c == 0 else -val
    wk = kings[0]; bk = kings[1]
    kw = 80 - 12 * (7 - wk >> 3); kb = 80 - 12 * (7 - bk >> 3)
    score += kw - kb
    return score

def search(side, depth, alpha, beta):
    if in_check(side):
        return 100000 if side == 0 else -100000
    if depth <= 0:
        return evaluate()
    best = -100001
    for m in gen(side):
        make(m)
        score = -search(side ^ 1, depth - 1, -beta, -alpha)
        unmake(m)
        if score > best: best = score
        if score > alpha: alpha = score
        if alpha >= beta: break
    return best

def choose(fen, legal):
    setup(fen)
    best = None; best_score = -100001
    for u in legal:
        m = parse_uci(u)
        make(m)
        s = -100001
        if not in_check(0):
            s = -search(1, 2, -100001, 100001)
        unmake(m)
        if s > best_score:
            best_score = s; best = u
    return best or legal[0]

# ---------- agent loop (env) ----------
def post(path, body):
    req = urllib.request.Request(ENV_URL + path, data=json.dumps(body).encode(), headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(req) as res:
            return json.load(res)
    except urllib.error.HTTPError as e:
        sys.exit("HTTP %d: %s" % (e.code, e.read().decode(errors="replace")))

def main():
    global ENV_URL
    ENV_URL = os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL not set")
    while True:
        g = post("/game", {})
        if g.get("status") == "done": break
        while g.get("status") == "your_move":
            legal = g.get("legal_moves", [])
            if not legal:
                sys.exit("no legal moves")
            g = post("/move", {"game": g.get("game"), "move": choose(g.get("fen", ""), legal)})
        print("game %s: %s by %s" % (g.get("game"), g.get("outcome"), g.get("reason")), file=sys.stderr)
    print("done: wins=%s draws=%s losses=%s" % (g.get("wins"), g.get("draws"), g.get("losses")), file=sys.stderr)

if __name__ == "__main__":
    main()

