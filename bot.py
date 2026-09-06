import discord
from discord.ext import commands
from discord.ui import Button, View
import random
import json
import os
from collections import defaultdict
from datetime import datetime, timezone

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=";", intents=intents)

STATS_FILE = "stats.json"
MARRIAGE_FILE = "marriages.json"

def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

stats = load_json(STATS_FILE, {})
marriages = load_json(MARRIAGE_FILE, {})

def record_use(author_id: int, target_id: int, command: str):
    author_key = str(author_id)
    target_key = str(target_id)
    if author_key not in stats:
        stats[author_key] = {}
    if target_key not in stats[author_key]:
        stats[author_key][target_key] = {}
    if command not in stats[author_key][target_key]:
        stats[author_key][target_key][command] = 0
    stats[author_key][target_key][command] += 1
    save_json(STATS_FILE, stats)

def get_count(author_id: int, target_id: int, command: str) -> int:
    author_key = str(author_id)
    target_key = str(target_id)
    if author_key in stats and target_key in stats[author_key] and command in stats[author_key][target_key]:
        return stats[author_key][target_key][command]
    return 0

ACTION_GIFS = {
    "kiss": [
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/38/bf/r71hHE9Atl1sF5iG.gif",
        "https://static.klipy.com/ii/935d7ab9d8c6202580a668421940ec81/8f/fc/ywiwFu96.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/fa/e9/9jQskLgUqjRrS.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/8a/5d/5sYTBY6Hwxore9ojwn.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/78/93/cwIYiBCG11bKqBIIo.gif",
    ],
    "hug": [
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/12/67/JrFwx5E7OyvjDUn6P7O.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/56/05/M2hUrYKcdAr91JXjk.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/7a/10/8NAEeoyglvATjC.gif",
        "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/3b/a1/cCDLjYxd.gif",
        "https://static.klipy.com/ii/e293a233a303a98e471f78d04e13a1b0/4c/79/Vm71YRIu.gif",
        "https://static.klipy.com/ii/935d7ab9d8c6202580a668421940ec81/e0/6b/PaJxcbRP.gif",
    ],
    "cuddle": [
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/ba/90/OOpAMLi3qc5fzg1tHA7.gif",
        "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/26/df/M42jO6Xq.gif",
        "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/4b/a1/YlNAVgAF.gif",
        "https://static.klipy.com/ii/7607a26399874a14744aa5e7accfa062/b4/b4/tXYJWuWJ.gif",
    ],
    "pat": [
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/54/8f/CHtBjQ9ItN9M78.gif",
        "https://static.klipy.com/ii/f87f46a2c5aeaeed4c68910815f73eaf/6b/92/Lj3jkuSu.gif",
        "https://static.klipy.com/ii/c3a19a0b747a76e98651f2b9a3cca5ff/c2/73/SjYIk5nC.gif",
        "https://static.klipy.com/ii/9ed0121ed465c12e1f3dda331ed33f0e/df/6c/qdgkKrbYfTC1pkbxeN.gif",
    ],
    "bonk": [
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/85/9c/t6Zu7IamibnD5Pp.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/26/7f/N1t4DyZECmQRAKnU.gif",
        "https://static.klipy.com/ii/e7539ef2aad336edaa067c28ee130b3c/e7/08/KZVUMnGujTWx.gif",
        "https://static.klipy.com/ii/8ce8357c78ea940b9c2015daf05ce1a5/d9/ed/C57d3Wv9.gif",
    ],
    "slap": [
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/73/ed/knLMcluv8Qab3JvIh.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/2a/ba/xc7sOkjNX3Wy.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/a0/53/muD8fKZMD4A9riaAC.gif",
        "https://static.klipy.com/ii/35ccce3d852f7995dd2da910f2abd795/04/61/ccvD5zDR.gif",
        "https://static.klipy.com/ii/35ccce3d852f7995dd2da910f2abd795/3e/51/gVeMoFwY.gif",
    ],
    "punch": [
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/25/1c/fM4mHnKeLwxer.gif",
        "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/32/95/XtdxM0mg.gif",
        "https://static.klipy.com/ii/a15b48460c436e1e92c85ffc680932cc/72/3b/rei0zkil.gif",
        "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/59/ba/JYFqHKlN.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/bc/e6/UvkVVpuUbUklQ.gif",
    ],
    "kick": [
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/8f/02/gbsJsySiK66KGdciknH.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/e2/c7/9U7G7mfjvBqy4Mx.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/35/da/dTFSgmSfQV6kqQ1PuHo.gif",
        "https://static.klipy.com/ii/c44064a00e4b7451969381d90dea1769/ff/cc/6a2lTX7k.gif",
    ],
    "lick": [
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/be/f0/Gf68ABL3XsCIsm1.gif",
        "https://static.klipy.com/ii/35ccce3d852f7995dd2da910f2abd795/04/7f/2mCZdDxE.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/e0/33/dr72jN0J7LCaO1vGudTk.gif",
    ],
    "flirt": [
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/3c/b0/jPT1KubKEz6lv3.gif",
        "https://static.klipy.com/ii/ce286d05b8e1a47cd4f32b0e1b6dec0e/50/04/ohEWptJ8.gif",
        "https://static.klipy.com/ii/35ccce3d852f7995dd2da910f2abd795/35/72/tCif1r4f.gif",
        "https://static.klipy.com/ii/e293a233a303a98e471f78d04e13a1b0/ab/8b/Cz9eOlCC.gif",
    ],
    "kill": [
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/ce/8a/TPIwIHbkwmClV.gif",
        "https://static.klipy.com/ii/8ce8357c78ea940b9c2015daf05ce1a5/07/1f/aPvaSIuP.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/aa/06/nwHcRITLB3s5WShoL.gif",
    ],
    "bite": [
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/73/ed/knLMcluv8Qab3JvIh.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/85/9c/t6Zu7IamibnD5Pp.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/26/7f/N1t4DyZECmQRAKnU.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/e0/33/dr72jN0J7LCaO1vGudTk.gif",
    ],
    "boop": [
        "https://static.klipy.com/ii/925f17378dd1893b674a723c07535afe/03/57/KjrvGk0w.gif",
        "https://static.klipy.com/ii/c3a19a0b747a76e98651f2b9a3cca5ff/c2/73/SjYIk5nC.gif",
        "https://static.klipy.com/ii/9ed0121ed465c12e1f3dda331ed33f0e/df/6c/qdgkKrbYfTC1pkbxeN.gif",
    ],
    "pinch": [
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/2a/ba/xc7sOkjNX3Wy.gif",
        "https://static.klipy.com/ii/f87f46a2c5aeaeed4c68910815f73eaf/6c/76/LjmbXUjH.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/5c/10/OgjMNZPwMu3Bt.gif",
        "https://static.klipy.com/ii/35ccce3d852f7995dd2da910f2abd795/04/61/ccvD5zDR.gif",
    ],
    "flick": [
        "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/cf/34/bEcRsy61.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/a0/53/muD8fKZMD4A9riaAC.gif",
        "https://static.klipy.com/ii/e7539ef2aad336edaa067c28ee130b3c/e7/08/KZVUMnGujTWx.gif",
    ],
    "tackle": [
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/57/e9/eGARSXmC74lLiVFJ1A4J.gif",
        "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/b1/b9/6bpHnxdC.gif",
        "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/7e/a4/FMioev1W.gif",
        "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/32/95/XtdxM0mg.gif",
    ],
    "throw": [
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/5c/1e/faZXrUvDytf1CFjv33.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/8f/02/gbsJsySiK66KGdciknH.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/e2/c7/9U7G7mfjvBqy4Mx.gif",
        "https://static.klipy.com/ii/c44064a00e4b7451969381d90dea1769/ff/cc/6a2lTX7k.gif",
    ],
    "spit": [
        "https://static.klipy.com/ii/935d7ab9d8c6202580a668421940ec81/87/96/omv3U0WF.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/70/b5/0ndyTzeNTZOt.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/fb/26/rkbcLWTxgsBlV.gif",
    ],
    "yeet": [
        "https://static.klipy.com/ii/925f17378dd1893b674a723c07535afe/93/c7/KQ5oV3U6.gif",
        "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/eb/c1/4rYYwdHQ.gif",
        "https://static.klipy.com/ii/35ccce3d852f7995dd2da910f2abd795/04/7f/2mCZdDxE.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/5c/10/OgjMNZPwMu3Bt.gif",
    ],
}

MARRY_GIFS = [
    "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/12/67/JrFwx5E7OyvjDUn6P7O.gif",
    "https://static.klipy.com/ii/935d7ab9d8c6202580a668421940ec81/e0/6b/PaJxcbRP.gif",
    "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/3b/a1/cCDLjYxd.gif",
]

PROPOSAL_GIFS = [
    "https://static.klipy.com/ii/ce286d05b8e1a47cd4f32b0e1b6dec0e/50/04/ohEWptJ8.gif",
    "https://static.klipy.com/ii/935d7ab9d8c6202580a668421940ec81/8f/fc/ywiwFu96.gif",
    "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/3c/b0/jPT1KubKEz6lv3.gif",
]

ACCEPT_GIFS = [
    "https://static.klipy.com/ii/7607a26399874a14744aa5e7accfa062/b4/b4/tXYJWuWJ.gif",
    "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/ba/90/OOpAMLi3qc5fzg1tHA7.gif",
    "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/26/df/M42jO6Xq.gif",
]

DECLINE_GIFS = [
    "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/85/9c/t6Zu7IamibnD5Pp.gif",
    "https://static.klipy.com/ii/f87f46a2c5aeaeed4c68910815f73eaf/6c/76/LjmbXUjH.gif",
    "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/26/7f/N1t4DyZECmQRAKnU.gif",
]
