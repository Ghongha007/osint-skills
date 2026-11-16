import importlib.util, os, sys, tempfile, unittest, hashlib, csv
from datetime import datetime, timezone, timedelta
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
sun = load("sun", "skills/chronolocate/scripts/sun.py")
ev = load("evidence", "skills/archive-evidence/scripts/evidence.py")
IST = timezone(timedelta(hours=5, minutes=30))

class Sun(unittest.TestCase):
    def test_noon_elevations(self):
        # at local solar noon, elevation = 90 - |latitude - solar declination|
        az, el = sun.sun_position(28.6139, 77.2090, datetime(2026, 6, 21, 12, 23, tzinfo=IST))
        self.assertAlmostEqual(el, 90 - (28.6139 - 23.44), delta=0.3)
        self.assertAlmostEqual(az, 180, delta=3)
        az, el = sun.sun_position(51.5, -0.12, datetime(2026, 12, 21, 12, 0, tzinfo=timezone.utc))
        self.assertAlmostEqual(el, 90 - (51.5 + 23.44), delta=0.3)
        _, el = sun.sun_position(0, 0, datetime(2026, 3, 20, 12, 7, tzinfo=timezone.utc))
        self.assertGreater(el, 89)
    def test_morning_east_evening_west(self):
        az, el = sun.sun_position(28.6, 77.2, datetime(2026, 11, 16, 8, 0, tzinfo=IST))
        self.assertTrue(90 < az < 180 and el > 0)
        az, el = sun.sun_position(28.6, 77.2, datetime(2026, 11, 16, 16, 0, tzinfo=IST))
        self.assertTrue(180 < az < 270 and el > 0)
        _, el = sun.sun_position(28.6, 77.2, datetime(2026, 11, 16, 23, 0, tzinfo=IST))
        self.assertLess(el, 0)
    def test_southern_hemisphere_noon_is_north(self):
        az, el = sun.sun_position(-33.87, 151.21, datetime(2026, 6, 21, 2, 0, tzinfo=timezone.utc))
        self.assertTrue(az < 20 or az > 340)
    def test_round_trip(self):
        t = datetime(2026, 11, 16, 10, 30, tzinfo=IST)
        az, el = sun.sun_position(28.6139, 77.2090, t)
        wins = sun.find_times(28.6139, 77.2090, t, IST, sun_azimuth=az, elevation=el, tolerance=0.5)
        self.assertEqual(len(wins), 1)
        self.assertTrue(wins[0][0] <= t <= wins[0][1])
        self.assertEqual(len(sun.find_times(28.6139, 77.2090, t, IST, elevation=el, tolerance=0.5)), 2)
    def test_naive_time_rejected(self):
        with self.assertRaises(ValueError):
            sun.sun_position(0, 0, datetime(2026, 1, 1))

class Evidence(unittest.TestCase):
    def test_hash_and_offline_log(self):
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "a.bin"); open(f, "wb").write(b"abc")
            self.assertEqual(ev.sha256(f), hashlib.sha256(b"abc").hexdigest())
            log = os.path.join(d, "log.csv")
            for _ in range(2):
                self.assertEqual(ev.main(["log", "--file", f, "--note", "n", "--log", log, "--offline"]), 0)
            rows = list(csv.DictReader(open(log, encoding="utf-8")))
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["sha256"], hashlib.sha256(b"abc").hexdigest())
            self.assertEqual(ev.main(["hash", os.path.join(d, "missing")]), 2)

if __name__ == "__main__":
    unittest.main()
