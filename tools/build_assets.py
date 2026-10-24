# Builds Juego/assets from Legends/_produccion/personajes: cropped transparent sprites + portraits + data.js
import json, glob, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(os.path.dirname(ROOT), 'Legends', '_produccion')
OUT = os.environ.get('OUT_DIR') or os.path.join(ROOT, 'assets')
H = 240  # sprite height in px

def fg_mask(a):
    # sheets are dithered/grainy: classify on a blurred copy
    b = ndimage.gaussian_filter(a.astype(float), sigma=(2.5, 2.5, 0))
    sat = b.max(2) - b.min(2)
    lum = b.mean(2)
    # background is a smooth gradient: start from a global guess, then refine a 2D estimate
    bl = np.concatenate([lum[:6].ravel(), lum[-6:].ravel(), lum[:, :6].ravel(), lum[:, -6:].ravel()])
    bgl = np.full(lum.shape, np.median(bl))
    tol = max(14, np.percentile(np.abs(bl - np.median(bl)), 95) + 6)
    for _ in range(3):
        d = np.abs(lum - bgl)
        cand = (sat < 14) & (d < tol)
        lab, n = ndimage.label(cand)
        edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
        bg = np.isin(lab, list(edge))
        w = ndimage.gaussian_filter(bg.astype(float), 40)
        bgl = np.where(w > 1e-3, ndimage.gaussian_filter(lum * bg, 40) / np.maximum(w, 1e-3), bgl)
        tol = float(os.environ.get('BG_TOL', 7))
    # enclosed gaps (between legs/arms) that match the background closely
    tight, nt = ndimage.label((sat < 8) & (d < 5) & ~bg)
    if nt:
        ts = ndimage.sum(np.ones_like(tight), tight, range(1, nt + 1))
        bg |= np.isin(tight, [i + 1 for i, s in enumerate(ts) if s > 3000])
    fg = ndimage.binary_opening(~bg, iterations=2)
    # small enclosed holes are usually grey clothing, not real gaps: fill them back
    holes, nh = ndimage.label(ndimage.binary_fill_holes(fg) & ~fg)
    if nh:
        hs = ndimage.sum(np.ones_like(holes), holes, range(1, nh + 1))
        fg |= np.isin(holes, [i + 1 for i, s in enumerate(hs) if s < 4000])
    return fg

def poses(sheet):
    """Split a sheet into its three poses (portrait, idle, special) by blob detection, left to right."""
    a = np.asarray(sheet).astype(int)
    fg = fg_mask(a)
    # panel separator lines span the full height: drop them so poses don't merge
    cols = np.where(fg.mean(0) > .9)[0]
    for c in cols:
        fg[:, max(0, c - 3):c + 4] = False
    # merge each pose with its loose fx particles on a downscaled mask
    f = 4
    hh, ww = fg.shape[0] // f * f, fg.shape[1] // f * f
    small = fg[:hh, :ww].reshape(hh // f, f, ww // f, f).any((1, 3))
    for it in (4, 2, 1):  # less merging when poses touch each other
        lab, n = ndimage.label(ndimage.binary_dilation(small, iterations=it))
        sizes = ndimage.sum(small, lab, range(1, n + 1))
        if n >= 3 and sorted(sizes)[-3] > .15 * max(sizes):
            break
    else:
        # poses touch: cut at the emptiest columns near 1/3 and 2/3
        cov = ndimage.uniform_filter1d(fg.mean(0), 15)
        W = fg.shape[1]
        c1 = int(W * .2) + int(np.argmin(cov[int(W * .2):int(W * .45)]))
        c2 = int(W * .5) + int(np.argmin(cov[int(W * .5):int(W * .8)]))
        out = []
        for x0, x1 in ((0, c1), (c1, c2), (c2, W)):
            m = np.zeros_like(fg); m[:, x0:x1] = fg[:, x0:x1]
            im = Image.fromarray(np.dstack([a.astype(np.uint8), np.where(m, 255, 0).astype(np.uint8)]), 'RGBA')
            out.append(im.crop(im.getbbox()))
        return out
    objs = ndimage.find_objects(lab)
    top = sorted((np.argsort(sizes)[::-1][:3] + 1).tolist(), key=lambda i: objs[i - 1][1].start)
    out = []
    for i in top:
        m = np.zeros_like(fg)
        m[:hh, :ww] = np.kron(lab == i, np.ones((f, f), bool))
        m &= fg
        im = Image.fromarray(np.dstack([a.astype(np.uint8), np.where(m, 255, 0).astype(np.uint8)]), 'RGBA')
        out.append(im.crop(im.getbbox()))
    return out

def sprite(s):
    r = H / s.height
    return s.resize((max(1, round(s.width * r)), H), Image.NEAREST)

def main():
    chars = json.load(open(os.path.join(SRC, 'personajes', 'personajes.json')))
    quotes = {}
    for f in sorted(glob.glob(os.path.join(SRC, 'S*', 'episodes_*.json'))):
        for e in json.load(open(f)):
            for p in ('p1', 'p2'):
                x = e[p]
                for k in ('carousel', 'line1', 'line2'):
                    q = x.get(k)
                    if q and q not in quotes.setdefault(x['name'], []):
                        quotes[x['name']].append(q)
    # debate lines (FACT / LOGIC / QUOTE / MIC DROP with sources), written by hand in tools/debate.json
    debate = json.load(open(os.path.join(ROOT, 'tools', 'debate.json')))
    # --data-only rewrites assets/data.js without re-cutting any sprite
    data_only = '--data-only' in sys.argv
    only = set(a for a in sys.argv[1:] if not a.startswith('--'))
    data = []
    for c in chars:
        if not c.get('sheet'):
            continue
        k = c['key']
        if not data_only and (not only or k in only):
            sheet = Image.open(os.path.join(SRC, 'personajes', c['sheet'])).convert('RGB')
            ps = poses(sheet)
            for i, tag in ((1, 'i'), (2, 's')):
                sprite(ps[i]).save(os.path.join(OUT, 'sp', f'{k}_{tag}.webp'), 'WEBP', quality=82, method=6)
            p = Image.open(os.path.join(SRC, 'personajes', 'port', k + '.png')).convert('RGB')
            p.resize((120, round(120 * p.height / p.width)), Image.LANCZOS).save(os.path.join(OUT, 'sp', f'{k}_p.webp'), 'WEBP', quality=80, method=6)
        q = quotes.get(c['name'], [])
        if k == 'rocket_billionaire':  # invented parody: no real quotes, no real name
            q = ["I'll just buy the arcade.", "Censored? I prefer 'limited edition'."]
        data.append({'k': k, 'n': c['name'], 'h': c['hud'], 'g': c['series'], 'a': c.get('aura', 'gold'),
                     'm': [c.get('esp1'), c.get('esp2'), c.get('super')], 'q': q, 'd': debate[k]})
    with open(os.path.join(OUT, 'data.js'), 'w') as f:
        f.write('window.ROSTER=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
    print(len(data), 'characters')

if __name__ == "__main__":
    main()
