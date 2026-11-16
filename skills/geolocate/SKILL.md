---
name: geolocate
description: Find where a photo or video was taken using visible clues and satellite or street-level imagery, and report the result with evidence and a confidence level. Use when the user asks where an image was taken, wants to check a claimed location, or mentions geolocation.
---

# Geolocate

Work from what is visible to a location that can be checked by someone else. A model's first impression of where a photo "looks like" is a lead to test, never the answer.

## First: should this image be located?

Proceed for news events, public places, conflict and disaster footage, and claims made by public figures or organisations.

Stop and ask the user for context if the image appears to show a private individual's home, a private person who has not put their location in public, a child, or someone who may be hiding from another person. Do not locate these on request alone. Finding a private person's home is not verification work.

## Method

1. **Describe before you conclude.** List every clue without interpreting it:
   - text: signs, shop names, number plates (format only), posters, language and script
   - built environment: road markings, kerbs, poles, power lines, architecture, roof types, bollards
   - landscape: skyline, ridge lines, rivers, coast, vegetation, soil colour
   - other: which side traffic drives on, sun direction, weather, vehicles, uniforms, brands
2. **Narrow in steps**: country, then region, then town, then street. Write down what moved you each step.
3. **Search the specific clues**: a shop name with a city, a phone-number area code on a sign, a distinctive building in a reverse image search.
4. **Match on imagery.** Find the spot in satellite view and, where available, street-level imagery. Look for at least three independent features that line up (for example a roof shape, a junction layout and a tower), and check there is nothing that contradicts.
5. **Work out the camera position and direction**, not only the general area.
6. **Check the date of the reference imagery.** Buildings appear and disappear. A mismatch may be age, not error.

## How to report

- Coordinates of the camera position, plus the direction it faces.
- The matching features, each stated as "in the image" and "in the reference imagery" so a reader can repeat the check.
- A confidence level with the reason:
  - **confirmed**: three or more independent features match and nothing contradicts
  - **probable**: the area matches but the exact position is not pinned
  - **possible**: consistent with the clues, with other candidates still open
- What you could not match, and what would settle it.

## Limits

- Never present a guess as a finding. If you cannot match features on imagery, say the location is not confirmed.
- AI geolocation tools and model guesses are often confidently wrong, especially for rural scenes and plain interiors. Use them to generate candidates only.
- A location match shows where an image was taken. It does not show when, or what the image depicts. Pair it with reverse image search for earlier copies, and with chronolocation.
