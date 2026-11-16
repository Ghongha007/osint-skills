---
name: archive-evidence
description: Preserve online evidence before it disappears. Saves pages to the Wayback Machine, hashes downloaded files and keeps a timestamped evidence log. Use when the user finds a post, page, image or video they may need to cite later, or asks to archive, preserve or log evidence.
---

# Archive evidence

Posts get deleted and pages get edited. Preserve first, analyse second.

## Order of work

1. **Archive the page** as soon as it matters, before doing anything else with it.
2. **Save a local copy** of the media (the original file where possible, not a screenshot of it).
3. **Hash the local copy** so you can later show it has not changed.
4. **Log it**: what, where from, when you saw it, archive link, hash, and why it matters.

## The script

`scripts/evidence.py` needs only Python. It contacts archive.org and nothing else.

```
python3 scripts/evidence.py check URL          # is there already a snapshot?
python3 scripts/evidence.py save URL           # ask the Wayback Machine to capture it now
python3 scripts/evidence.py hash FILE...       # SHA-256
python3 scripts/evidence.py log --url URL --file FILE --note "why this matters" --save
```

`log` appends one row to `evidence_log.csv` (change with `--log`): UTC time, URL, snapshot link, snapshot time, file, SHA-256, size, note. Use `--offline` to log a file without contacting archive.org.

## Rules

- **Ask before archiving anything the user has not said is public.** Sending a URL to the Wayback Machine publishes it to a public archive. Never submit private links, unlisted documents, links containing tokens or session ids, or pages behind a login.
- **Check the snapshot, do not assume it.** After `save`, open the snapshot link. Many platforms (Instagram, X, Facebook, most video players) archive as a login wall or an empty shell. If the snapshot does not show the content, say so and fall back to a local copy plus a screenshot that includes the address bar and system clock.
- **Use a second archive** for anything important (for example archive.today), because one service can fail or remove a capture.
- **Never edit the original file.** Work on a copy. Hash the original first.
- **Record the time in UTC** and note the local timezone of the event separately.
- A hash proves the file has not changed since you hashed it. It does not prove the file was authentic when you got it.
- Do not store more personal data than the story needs, and keep the log somewhere access-controlled if it names private individuals.

## What to tell the user

After each item: the snapshot link (and whether you confirmed it shows the content), the file hash, and the row you logged. If archiving failed, say that plainly and give the fallback you used.
