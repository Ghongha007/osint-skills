---
name: map-a-network
description: Turn a chat or social-media export into a network and read it responsibly. Converts Telegram exports, X archives, YouTube comments or a CSV of posts into Gephi files with chat2net, then guides layout, community detection and interpretation. Use when the user wants to see who interacts with whom, find clusters or central accounts, or mentions Gephi, network analysis or coordinated behaviour.
---

# Map a network

## 1. Check the data first

Ask where the export came from. Proceed with the user's own archive, public channels and groups, public posts, or data shared with consent. If it is a private group the user is not part of, or scraped private data, stop and say why.

## 2. Build the network

Use `chat2net` (https://github.com/Ghongha007/chat2net; clone it and run `pip install .` in its folder). It reads the file and writes `edges.csv` and `nodes.csv`.

```
chat2net result.json                                   # Telegram Desktop JSON export
chat2net posts.csv --author-col user --text-col text   # any table of posts
chat2net video.info.json                               # yt-dlp --write-comments
chat2net a.json b.json --min-weight 2 --gexf           # combine files, drop one-off contacts
chat2net result.json --anonymise                       # names replaced by salted hashes
```

If `chat2net` is not available, build the same two tables by hand: an edges table with columns `Source`, `Target`, `Type` (the word `Directed`) and `Weight`, where each row points from the account that acted to the account it replied to, mentioned, forwarded or reposted.

Read the printed summary to the user: how many accounts and connections, and who received the most.

## 3. Lay it out in Gephi

1. *File > Import spreadsheet...*, choose `edges.csv`, confirm **Edges table**.
2. *Layout*: **ForceAtlas 2**, *Run*, then *Stop* when it settles. Connected accounts pull together; everything else pushes apart.
3. *Statistics*: run **Modularity**. *Appearance*: colour nodes by *Modularity Class*.
4. *Appearance*: size nodes by **Degree** (how many connections), or run *Network Diameter* and size by **Betweenness Centrality** to find accounts that bridge groups.

## 4. Read it carefully

- **A cluster is a lead, not proof.** Accounts cluster because they interact. That may be coordination. It may be colleagues, rivals arguing, or fans of one team. Open the posts behind the strongest connections before saying what a cluster is.
- **Big does not mean influential.** A large node may be an account that many people are attacking, or a bot that mentions everyone.
- **Coordination needs more than a shape.** Look for identical text, synchronised timing, account creation dates in a batch, and shared links. Report those specifically.
- **The layout is not a map.** Distance on the page is approximate, and running the layout again gives a different picture. Community counts change with the Modularity resolution setting; say which setting you used.
- **Missing data bends the picture.** Deleted posts, private accounts and the export's date range all shape what you see. State the date range and source.

## 5. Report

What the data is and its date range, the size of the network, the communities found and what the posts inside each have in common (checked by reading them), the bridging accounts, and what the network cannot show. Do not name private individuals as members of a cluster in anything meant for publication; describe the cluster.
