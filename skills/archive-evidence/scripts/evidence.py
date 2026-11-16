#!/usr/bin/env python3
"""Evidence log helper. Standard library only.

  evidence.py hash FILE [FILE...]            SHA-256 of local files
  evidence.py check URL                      latest Wayback Machine snapshot of a URL, if any
  evidence.py save URL                       ask the Wayback Machine to capture a URL now
  evidence.py log --url URL [--file FILE] [--note TEXT] [--log evidence_log.csv] [--save]

`log` appends one row: UTC time, URL, Wayback snapshot, local file, SHA-256, note.
"""
import argparse
import csv
import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

UA = {"User-Agent": "evidence-log/0.1"}
FIELDS = ["logged_utc", "url", "wayback_snapshot", "snapshot_time", "file", "sha256", "bytes", "note"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def wayback_latest(url, timeout=30):
    """Return (snapshot_url, timestamp) of the closest snapshot, or ('', '')."""
    q = "https://archive.org/wayback/available?url=" + urllib.parse.quote(url, safe="")
    with urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=timeout) as r:
        snap = json.load(r).get("archived_snapshots", {}).get("closest") or {}
    return (snap.get("url", ""), snap.get("timestamp", "")) if snap.get("available") else ("", "")


def wayback_save(url, timeout=120):
    """Ask Save Page Now to capture the URL. Returns the snapshot URL it redirects to."""
    req = urllib.request.Request("https://web.archive.org/save/" + url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.geturl()


def append_log(path, row):
    new = not os.path.exists(path) or os.path.getsize(path) == 0
    with open(path, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)


def main(argv=None):
    p = argparse.ArgumentParser(description="Hash files, check or request Wayback snapshots, keep an evidence log.")
    sub = p.add_subparsers(dest="cmd", required=True)
    h = sub.add_parser("hash"); h.add_argument("files", nargs="+")
    c = sub.add_parser("check"); c.add_argument("url")
    s = sub.add_parser("save"); s.add_argument("url")
    l = sub.add_parser("log")
    l.add_argument("--url", default="")
    l.add_argument("--file")
    l.add_argument("--note", default="")
    l.add_argument("--log", default="evidence_log.csv")
    l.add_argument("--save", action="store_true", help="request a fresh Wayback capture first")
    l.add_argument("--offline", action="store_true", help="do not contact the Wayback Machine")
    a = p.parse_args(argv)
    try:
        if a.cmd == "hash":
            for f in a.files:
                print(f"{sha256(f)}  {f}")
        elif a.cmd == "check":
            snap, ts = wayback_latest(a.url)
            print(f"{snap}  (captured {ts} UTC)" if snap else "no snapshot found")
            return 0 if snap else 1
        elif a.cmd == "save":
            print(wayback_save(a.url))
        else:
            if not a.url and not a.file:
                p.error("give --url, --file, or both")
            row = dict.fromkeys(FIELDS, "")
            row.update(logged_utc=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), url=a.url, note=a.note)
            if a.file:
                row.update(file=a.file, sha256=sha256(a.file), bytes=os.path.getsize(a.file))
            if a.url and not a.offline:
                try:
                    if a.save:
                        wayback_save(a.url)
                    row["wayback_snapshot"], row["snapshot_time"] = wayback_latest(a.url)
                except OSError as e:
                    print(f"warning: Wayback Machine not reached ({e}); row logged without a snapshot", file=sys.stderr)
            append_log(a.log, row)
            print(f"logged to {a.log}")
            for k in FIELDS:
                if row[k] != "":
                    print(f"  {k}: {row[k]}")
    except FileNotFoundError as e:
        print(f"no such file: {e.filename}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"network or file error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
