---
name: verify-image
description: Check whether a photo or video is what a post claims it is. Covers finding the earliest copy, checking for old or out-of-context footage, signs of editing or AI generation, and reporting what is and is not established. Use when the user asks if an image or video is real, fake, old, AI-generated or miscaptioned.
---

# Verify an image or video

Most false visuals are real footage with a false caption: an old flood, another country, a film set. Check context before pixels.

## The five questions

Answer each, or say that you could not.

1. **Provenance: is this the original?** Find the earliest copy. Search with more than one reverse image engine, because each indexes different regions and platforms. For video, extract several frames and search each. An earlier copy with a different caption usually settles the matter.
2. **Source: who captured it?** The uploader is often not the person who filmed it. Look for the first uploader, a watermark, a longer or higher-quality version, and whether that account plausibly was there.
3. **Date: when was it captured?** Upload time is the latest possible capture time, not the capture time. Check weather records, shadows (see chronolocation), events visible in the frame, and file metadata if you have the original file. Most platforms strip metadata, so its absence means nothing.
4. **Location: where was it captured?** Match visible features to imagery (see geolocation).
5. **Motivation and consistency: does the content fit the claim?** Language on signs, uniforms, vehicles, season, and whether independent footage of the same event exists.

## Editing and AI generation

- Look for what the scene gets wrong: text and signage that does not read, inconsistent shadows and reflections, repeated textures, hands and teeth, objects that merge, physics that does not hold across video frames.
- Check for provenance data: Content Credentials (C2PA) in the file, and visible or invisible watermarks from the generator.
- **Treat automatic detectors as weak evidence.** They give false positives on compressed, resized or screenshotted real images and miss output from newer generators. Never report a detector score as a finding by itself. Report it as one input with the tool's name.
- "No sign of manipulation found" is not "authentic". Say which.

## How to report

Use one of these, with the evidence for it:

- **Verified**: original found; source, date and place established.
- **Miscaptioned**: real footage, but from another time, place or event. Give the earliest copy and its real context.
- **Altered or synthetic**: state the specific evidence.
- **Unverified**: say which of the five questions remain open.

Give links to the earliest copy and the reference material so a reader can repeat the check. Archive both the claim and the original before publishing (see the archive-evidence skill).

## Care

- Do not identify private individuals in footage, and do not run faces through recognition services. Verifying what happened does not require naming bystanders.
- Graphic footage: warn the user before describing it in detail.
- If the image shows a possible victim or a child, limit the analysis to whether the claim about the event is true.
