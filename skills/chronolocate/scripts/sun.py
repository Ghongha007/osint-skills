#!/usr/bin/env python3
"""Sun position and shadow maths for chronolocation. Standard library only.

Uses the NOAA solar position equations (no correction for atmospheric refraction,
so elevations within a few degrees of the horizon are less reliable).

  sun.py position --lat 28.6139 --lon 77.2090 --time 2026-06-21T12:00+05:30
  sun.py when --lat 28.6139 --lon 77.2090 --date 2026-06-21 --tz +05:30 --shadow-azimuth 70
  sun.py when --lat 28.6139 --lon 77.2090 --date 2026-06-21 --tz +05:30 --height 1.8 --shadow-length 2.4
"""
import argparse
import math
import sys
from datetime import datetime, timedelta, timezone

R, D = math.radians, math.degrees


def sun_position(lat, lon, when):
    """Return (azimuth, elevation) in degrees. Azimuth is clockwise from true north. `when` must be timezone-aware."""
    if when.tzinfo is None:
        raise ValueError("time needs a timezone, e.g. 2026-06-21T12:00+05:30 or ...Z")
    u = when.astimezone(timezone.utc)
    jd = u.toordinal() + 1721424.5 + (u.hour + u.minute / 60 + u.second / 3600) / 24
    t = (jd - 2451545.0) / 36525.0
    l0 = (280.46646 + t * (36000.76983 + t * 0.0003032)) % 360
    m = 357.52911 + t * (35999.05029 - 0.0001537 * t)
    e = 0.016708634 - t * (0.000042037 + 0.0000001267 * t)
    c = (math.sin(R(m)) * (1.914602 - t * (0.004817 + 0.000014 * t))
         + math.sin(R(2 * m)) * (0.019993 - 0.000101 * t) + math.sin(R(3 * m)) * 0.000289)
    omega = 125.04 - 1934.136 * t
    lam = l0 + c - 0.00569 - 0.00478 * math.sin(R(omega))
    eps = 23 + (26 + (21.448 - t * (46.815 + t * (0.00059 - t * 0.001813))) / 60) / 60 + 0.00256 * math.cos(R(omega))
    decl = math.asin(math.sin(R(eps)) * math.sin(R(lam)))
    y = math.tan(R(eps / 2)) ** 2
    eot = 4 * D(y * math.sin(2 * R(l0)) - 2 * e * math.sin(R(m)) + 4 * e * y * math.sin(R(m)) * math.cos(2 * R(l0))
                - 0.5 * y * y * math.sin(4 * R(l0)) - 1.25 * e * e * math.sin(2 * R(m)))
    minutes = u.hour * 60 + u.minute + u.second / 60
    tst = (minutes + eot + 4 * lon) % 1440
    ha = tst / 4 - 180
    cz = math.sin(R(lat)) * math.sin(decl) + math.cos(R(lat)) * math.cos(decl) * math.cos(R(ha))
    zen = math.acos(max(-1.0, min(1.0, cz)))
    den = math.cos(R(lat)) * math.sin(zen)
    if abs(den) < 1e-9:
        az = 180.0 if lat > D(decl) else 0.0
    else:
        a = D(math.acos(max(-1.0, min(1.0, (math.sin(R(lat)) * math.cos(zen) - math.sin(decl)) / den))))
        az = (a + 180) % 360 if ha > 0 else (540 - a) % 360
    return az, 90 - D(zen)


def angle_diff(a, b):
    return abs((a - b + 180) % 360 - 180)


def find_times(lat, lon, day, tz, sun_azimuth=None, elevation=None, tolerance=1.0):
    """Scan one local day minute by minute. Returns [(start, end, az, el)] windows where the sun matches."""
    start = datetime(day.year, day.month, day.day, tzinfo=tz)
    hits = []
    for i in range(1440):
        w = start + timedelta(minutes=i)
        az, el = sun_position(lat, lon, w)
        if el <= 0:
            continue
        ok = True
        if sun_azimuth is not None:
            ok = ok and angle_diff(az, sun_azimuth) <= tolerance
        if elevation is not None:
            ok = ok and abs(el - elevation) <= tolerance
        if ok:
            hits.append((w, az, el))
    windows = []
    for w, az, el in hits:
        if windows and (w - windows[-1][1]) <= timedelta(minutes=1):
            windows[-1][1] = w
        else:
            windows.append([w, w, az, el])
    return [tuple(x) for x in windows]


def parse_tz(s):
    if s in ("Z", "UTC", "utc"):
        return timezone.utc
    sign = -1 if s.startswith("-") else 1
    hh, _, mm = s.lstrip("+-").partition(":")
    return timezone(sign * timedelta(hours=int(hh), minutes=int(mm or 0)))


def main(argv=None):
    p = argparse.ArgumentParser(description="Sun position and shadow maths for chronolocation.")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("position", help="where the sun is at a given place and time")
    b = sub.add_parser("when", help="at what time of day the sun matches a measured shadow")
    for q in (a, b):
        q.add_argument("--lat", type=float, required=True)
        q.add_argument("--lon", type=float, required=True, help="east is positive")
    a.add_argument("--time", required=True, help="ISO time with offset, e.g. 2026-06-21T12:00+05:30")
    b.add_argument("--date", required=True, help="YYYY-MM-DD (local date)")
    b.add_argument("--tz", default="Z", help="local offset from UTC, e.g. +05:30 (default UTC)")
    b.add_argument("--shadow-azimuth", type=float, help="compass direction the shadow points, degrees from north")
    b.add_argument("--height", type=float, help="height of the object casting the shadow")
    b.add_argument("--shadow-length", type=float, help="length of its shadow on flat ground, same unit")
    b.add_argument("--tolerance", type=float, default=1.0, help="degrees of error to allow (default 1)")
    g = p.parse_args(argv)
    if not (-90 <= g.lat <= 90 and -180 <= g.lon <= 180):
        p.error("latitude must be -90..90 and longitude -180..180")
    if g.cmd == "position":
        w = datetime.fromisoformat(g.time.replace("Z", "+00:00"))
        az, el = sun_position(g.lat, g.lon, w)
        print(f"sun azimuth   {az:6.1f} deg from north")
        print(f"sun elevation {el:6.1f} deg" + ("  (below the horizon)" if el <= 0 else ""))
        if el > 0:
            print(f"shadow points {(az + 180) % 360:6.1f} deg from north, length = {1 / math.tan(R(el)):.2f} x object height")
        return 0
    sun_az = (g.shadow_azimuth + 180) % 360 if g.shadow_azimuth is not None else None
    el = None
    if (g.height is None) != (g.shadow_length is None):
        p.error("--height and --shadow-length go together")
    if g.height is not None:
        if g.height <= 0 or g.shadow_length <= 0:
            p.error("--height and --shadow-length must be positive")
        el = D(math.atan2(g.height, g.shadow_length))
        print(f"shadow ratio gives sun elevation {el:.1f} deg")
    if sun_az is None and el is None:
        p.error("give --shadow-azimuth, or --height with --shadow-length, or both")
    y, mo, d = (int(x) for x in g.date.split("-"))
    wins = find_times(g.lat, g.lon, datetime(y, mo, d), parse_tz(g.tz), sun_az, el, g.tolerance)
    if not wins:
        print("no time on this date matches. Check the date, the location, the compass direction, or raise --tolerance.")
        return 1
    for s, e, az, elv in wins:
        print(f"{s:%H:%M} to {e:%H:%M} local  (sun azimuth about {az:.0f}, elevation about {elv:.0f})")
    if sun_az is None:
        print("elevation alone usually matches twice, once in the morning and once in the afternoon.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
