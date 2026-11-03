#!/usr/bin/env python3
"""Téléchargeur poli pour coa-development.org (lecture seule).

- Refuse toute route interdite (robots.txt + armurerie + compte).
- Max ~2 requêtes/s (pause 0.55 s entre deux requêtes réseau).
- Cache disque dans /home/claude/coa-fr/work/site-coa/cache/ : relançable sans re-télécharger.
- Aucun cookie, aucune connexion, uniquement GET.

Usage en module : from fetch import get ; get('/api/xxx') -> (status, bytes, content_type)
Usage CLI : python3 fetch.py /chemin [/chemin2 ...]  (affiche statut + taille + fichier cache)
"""
import hashlib
import os
import sys
import time
import json
import urllib.parse

import requests

BASE = "https://coa-development.org"
CACHE = "/home/claude/coa-fr/work/site-coa/cache"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
FORBIDDEN_PREFIXES = ("/account", "/api/account", "/bug-media", "/downloads", "/armory", "/api/armory",
                      "/api/auth", "/login", "/logout", "/register")
MIN_INTERVAL = float(__import__("os").environ.get("COA_INTERVAL", "0.56"))
_last = [0.0]
import threading
_lock = threading.Lock()
_session = requests.Session()
_session.headers.update({"User-Agent": UA, "Accept": "*/*"})
LOG = "/home/claude/coa-fr/collecte/site-coa/journal.txt"


def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + " | " + msg + "\n")


def _check(path):
    p = urllib.parse.urlparse(path).path.lower()
    for fp in FORBIDDEN_PREFIXES:
        if p == fp or p.startswith(fp + "/") or p.startswith(fp + "?") or (fp.endswith("/") and p.startswith(fp)):
            raise PermissionError("Route interdite : " + path)
    # armory variants
    if "armory" in p or "/account" in p:
        raise PermissionError("Route interdite : " + path)


def cache_path(path):
    h = hashlib.sha1(path.encode()).hexdigest()[:16]
    safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in path.strip("/"))[:80] or "root"
    return os.path.join(CACHE, safe + "__" + h)


def get(path, force=False, allow_armory_home=False, store=True):
    if path.startswith("http"):
        u = urllib.parse.urlparse(path)
        if u.netloc != "coa-development.org":
            raise ValueError("Hors site : " + path)
        path = u.path + (("?" + u.query) if u.query else "")
    if not (allow_armory_home and path in ("/armory",)):
        _check(path)
    os.makedirs(CACHE, exist_ok=True)
    cp = cache_path(path)
    if store and not force and os.path.exists(cp + ".body"):
        meta = json.load(open(cp + ".meta", encoding="utf-8"))
        return meta["status"], open(cp + ".body", "rb").read(), meta.get("ctype", "")
    # throttle partagé entre fils : au plus une requête qui démarre toutes les MIN_INTERVAL secondes
    with _lock:
        wait = MIN_INTERVAL - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
    for attempt in range(3):
        try:
            r = _session.get(BASE + path, timeout=60, allow_redirects=False)
            break
        except requests.RequestException as e:
            if attempt == 2:
                log(f"ERREUR réseau {path}: {e}")
                raise
            time.sleep(2 + attempt * 3)
    if r.status_code in (301, 302, 303, 307, 308):
        loc = r.headers.get("Location", "")
        log(f"Redirection {path} -> {loc} (non suivie)")
    if r.status_code == 429:
        log(f"429 sur {path}, pause 30 s")
        time.sleep(30)
        return get(path, force=True, allow_armory_home=allow_armory_home, store=store)
    if not store:
        return r.status_code, r.content, r.headers.get("Content-Type", "")
    with open(cp + ".body", "wb") as f:
        f.write(r.content)
    with open(cp + ".meta", "w", encoding="utf-8") as f:
        json.dump({"path": path, "status": r.status_code, "ctype": r.headers.get("Content-Type", ""),
                   "len": len(r.content), "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "location": r.headers.get("Location", "")}, f)
    return r.status_code, r.content, r.headers.get("Content-Type", "")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        try:
            st, body, ct = get(p)
            print(st, len(body), ct, cache_path(p) + ".body")
        except PermissionError as e:
            print("REFUS", e)
