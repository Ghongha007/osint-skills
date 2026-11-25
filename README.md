# osint-skills

Six skills that teach an AI coding agent to do verification work the way a careful open-source investigator would: show the evidence, give a confidence level, attribute contested facts, and say what is not established.

They are written in the open [Agent Skills](https://agentskills.io) format (a folder with a `SKILL.md` file), so they work in Claude Code and in other agents that read the same format.

| Skill | What it does | Script included |
|---|---|---|
| [verify-image](skills/verify-image/SKILL.md) | Checks whether a photo or video is what a post claims: earliest copy, source, date, place, signs of editing or AI generation | |
| [geolocate](skills/geolocate/SKILL.md) | Finds where an image was taken and reports matching features with a confidence level | |
| [chronolocate](skills/chronolocate/SKILL.md) | Works out the time of day from shadows | `sun.py`: sun position and shadow solver |
| [archive-evidence](skills/archive-evidence/SKILL.md) | Saves pages to the Wayback Machine, hashes files, keeps an evidence log | `evidence.py`: hash, archive, log |
| [attribute-claims](skills/attribute-claims/SKILL.md) | Fact-checks a draft claim by claim: OK, FIX, SOFTEN or UNVERIFIED, with suggested wording | |
| [map-a-network](skills/map-a-network/SKILL.md) | Turns a chat or social export into a Gephi network and reads it without over-claiming | uses [chat2net](https://github.com/Ghongha007/chat2net) |

## Why these exist

An AI model asked "where was this photo taken?" will often answer with a confident guess. That is the opposite of verification. These skills make the agent work in steps a reader can repeat: list the clues, match them against imagery or sources, and report what matched and what did not.

They also carry the rules we use on our own scripts: say who says a thing before saying what they say, keep allegations as allegations, give the other side's position, and do not claim a motive without evidence of one.

## Install

**Claude Code, for yourself:**

```
git clone https://github.com/Ghongha007/osint-skills.git
cp -r osint-skills/skills/* ~/.claude/skills/
```

**Claude Code, for one project:** copy the folders into `.claude/skills/` in that project.

**Other agents:** copy the folders to wherever your agent reads skills from. Each skill is self-contained.

Then ask in plain words, for example "fact-check this script before I record it" or "what time of day was this photo taken? It's at 28.6139, 77.2090 on 16 November". The agent picks the matching skill from its description.

## The two scripts work without an agent

Both need only Python 3.9 or newer, with nothing to install.

```
$ python3 skills/chronolocate/scripts/sun.py when --lat 28.6139 --lon 77.2090 \
      --date 2026-11-16 --tz +05:30 --height 1.8 --shadow-length 2.4
shadow ratio gives sun elevation 36.9 deg
10:18 to 10:35 local  (sun azimuth about 148, elevation about 36)
13:36 to 13:54 local  (sun azimuth about 207, elevation about 38)
elevation alone usually matches twice, once in the morning and once in the afternoon.

$ python3 skills/archive-evidence/scripts/evidence.py log --url https://example.org/post \
      --file post.mp4 --note "original upload" --save
```

`sun.py` uses the NOAA solar position equations without a refraction correction. `evidence.py` contacts archive.org and nothing else.

## What these skills will not do

- Locate a private person's home, or identify private individuals in footage.
- Run faces through recognition services.
- Treat an AI-detector score, a model's location guess or a network cluster as proof.
- Archive links the user has not said are public.

These limits are written into the skills. If you fork the pack, please keep them.

## Limits of the pack itself

- Skills are instructions, so results depend on the model following them and on the tools it has (web search, a browser, image input). Without web access, most of the verification steps cannot be completed and the agent should say so.
- The skills have been written from published verification practice and from our own workflow. They have not been benchmarked across models.
- `sun.py` has been checked against known noon elevations and round-trip tests (see `tests/`), not against every latitude and date.

## Tests

```
python3 -m unittest discover -s tests
```

## Related

- [india-osint](https://github.com/Ghongha007/india-osint): public records and open data for investigating stories in India
- [ai-for-osint](https://github.com/Ghongha007/ai-for-osint): AI tools for investigators, with where each runs and its known limits
- [chat2net](https://github.com/Ghongha007/chat2net): turn a chat or social-media export into a Gephi network
- [verify-mcp](https://github.com/Ghongha007/verify-mcp): an MCP server with keyless, read-only verification lookups
- [osint-visuals](https://github.com/Ghongha007/osint-visuals): agent skills for evidence graphics: ship and flight tracks, shadow diagrams, 3D scenes, satellite before/after and scroll stories

## Licence

MIT. Made by [OSINT JOURNO](https://github.com/OSINT-JOURNO).
