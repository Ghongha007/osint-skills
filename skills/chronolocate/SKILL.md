---
name: chronolocate
description: Work out when a photo or video was taken from shadows and the sun's position. Use when the user asks what time or date an image was captured, wants to check a claimed time against shadows, or mentions chronolocation, shadow analysis or SunCalc.
---

# Chronolocate

Estimate the time of day (and sometimes narrow the date) of an image whose location is already known, using the direction and length of shadows.

## Before you start

You need three things. If one is missing, say which and stop guessing.

1. **Location** as latitude and longitude. If the place is unknown, geolocate first.
2. **A shadow you can measure**: cast by something vertical (pole, building edge, standing person) onto roughly flat ground.
3. **Either the date or the time.** With the date you can solve for the time. With neither, you can only give a range of combinations.

## Method

1. **Find north in the image.** Match the image to satellite imagery and draw the shadow on the map. Read its compass direction: 0 is north, 90 east, 180 south, 270 west. Give your reading as a range (for example 60 to 70), not one number.
2. **Measure the ratio if you can.** If the object's height and its shadow length can both be estimated (a person is roughly 1.6 to 1.8 m; count paving stones or lane widths for the shadow), note both.
3. **Run the script** in this skill's `scripts/` folder:

   ```
   python3 scripts/sun.py when --lat LAT --lon LON --date YYYY-MM-DD --tz +05:30 --shadow-azimuth 65 --tolerance 5
   python3 scripts/sun.py when --lat LAT --lon LON --date YYYY-MM-DD --tz +05:30 --height 1.7 --shadow-length 2.4
   python3 scripts/sun.py position --lat LAT --lon LON --time 2026-06-21T12:00+05:30
   ```

   `--shadow-azimuth` is the direction the shadow points. The script converts it to the sun's direction. Set `--tolerance` to half the width of your measured range.
4. **Check a claimed time** with `position`: if the claim says 5 pm and the script puts the sun in the west-south-west at 20 degrees, shadows must point east-north-east and be about 2.7 times the object's height. Compare with the image.
5. **Cross-check** with anything else visible: clocks, shop shutters, traffic, prayer or school times, weather records for that day, other footage of the same event.

## How to report

- Give a **window**, never a single minute: "between about 10:15 and 10:40 local time".
- State what you measured, the range you used, and the assumed date.
- Shadow length alone matches twice a day (morning and afternoon). Say which one you chose and why (which side the shadow falls on).
- Say what would change the answer: sloping ground, a leaning object, lens distortion near the frame edge, an uncertain date.

## Limits

- The script ignores atmospheric refraction. Treat results as unreliable when the sun is within about 3 degrees of the horizon.
- Near the equator around midday, shadows are too short to measure well.
- Shadows fix the time on a given date, or a pair of dates for a given time (the sun repeats its path on either side of each solstice). They rarely fix a date on their own.
- A matching shadow is consistent with a claim. It does not prove the claim.
