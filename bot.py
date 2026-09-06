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
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/38/bf/r71hHE9At1lsF5iG.gif",
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

ACTION_MESSAGES = {
    "kiss": [
        "{author} gives {target} a sweet kiss! 💋",
        "{author} plants a kiss on {target}'s cheek! 😘",
        "{author} kisses {target} passionately! 🔥",
        "{author} sneakily steals a kiss from {target}! 🥰",
    ],
    "kick": [
        "{author} kicks {target} across the room! 🦶💨",
        "{author} delivers a powerful kick to {target}! 🥋",
        "{author} roundhouse kicks {target}! 💥",
        "{author} dropkicks {target} into next week! 🦵",
    ],
    "punch": [
        "{author} punches {target} square in the face! 💪",
        "{author} throws a haymaker at {target}! 💪",
        "{author} lands a solid punch on {target}! 💥",
        "{author} gives {target} a one-two combo! 👊",
    ],
    "slap": [
        "{author} slaps {target} across the face! 🖐️",
        "{author} gives {target} a hard slap! 🖐️💥",
        "{author} slaps {target} silly! 🖐️😵",
        "{author} delivers a stinging slap to {target}! 🖐️🔥",
    ],
    "hug": [
        "{author} gives {target} a warm hug! 🤗",
        "{author} wraps {target} in a tight embrace! 🫂",
        "{author} hugs {target} lovingly! 💕",
        "{author} pulls {target} into a big hug! 🫂",
    ],
    "pat": [
        "{author} pats {target} on the head! 🥺",
        "{author} gently pats {target}! ✨",
        "{author} gives {target} a comforting pat! 💖",
        "{author} pats {target}'s head softly! 🥹",
    ],
    "bonk": [
        "{author} bonks {target} on the head! 🔨",
        "{author} gives {target} a good bonk! 🔨💥",
        "{author} bonks {target} into next week! 🔨",
        "{author} delivers a mighty bonk to {target}! 🔨⚡",
    ],
    "cuddle": [
        "{author} cuddles up to {target}! 🥰",
        "{author} snuggles with {target}! 💕",
        "{author} gives {target} a cozy cuddle! 🫂",
        "{author} curls up with {target}! 🌙",
    ],
    "lick": [
        "{author} licks {target}! 👅",
        "{author} gives {target} a big lick! 👅💦",
        "{author} licks {target}'s face! 👅😋",
        "{author} slobbers all over {target}! 👅🤪",
    ],
    "flirt": [
        "{author} flirts with {target}! 😏",
        "{author} winks at {target}! 😉",
        "{author} smoothly flirts with {target}! 💋",
        "{author} shoots their shot at {target}! 🔥",
    ],
    "kill": [
        "{author} kills {target}! 💀",
        "{author} utterly destroys {target}! ☠️",
        "{author} eliminates {target}! 💀🔪",
        "{author} sends {target} to the shadow realm! 🌑",
    ],
    "bite": [
        "{author} bites {target}! 🦷",
        "{author} chomps down on {target}! 🐕",
        "{author} nibbles on {target}! 🥺",
        "{author} gives {target} a love bite! 😈",
    ],
    "boop": [
        "{author} boops {target}'s nose! 👆",
        "{author} gently boops {target}! 👆🥺",
        "{author} sneakily boops {target}! 👆😏",
        "{author} gives {target} a little boop! 👆✨",
    ],
    "pinch": [
        "{author} pinches {target}'s cheek! 🤏",
        "{author} gives {target} a playful pinch! 🤏😈",
        "{author} pinches {target} really hard! 🤏😤",
        "{author} squeezes {target}'s cheeks! 🤏🥹",
    ],
    "flick": [
        "{author} flicks {target}'s forehead! 👆💢",
        "{author} gives {target} a quick flick! 👆",
        "{author} flickes {target} right on the nose! 👆😤",
        "{author} delivers a precise flick to {target}! 👆🎯",
    ],
    "tackle": [
        "{author} tackles {target} to the ground! 🏈",
        "{author} jumps on {target} with a tackle! 💥",
        "{author} tackles {target} out of nowhere! 💨",
        "{author} rugby tackles {target}! 🏉",
    ],
    "throw": [
        "{author} throws {target} across the room! 💫",
        "{author} hurls {target} into the distance! 🚀",
        "{author} tosses {target} like a ragdoll! 🪀",
        "{author} yeets {target} away! 💨",
    ],
    "spit": [
        "{author} spits on {target}! 🤮",
        "{author} spits water all over {target}! 💦",
        "{author} does a spit take all over {target}! 😤💦",
        "{author} spits in {target}'s general direction! 🧐",
    ],
    "yeet": [
        "{author} YEETS {target} into the void! 🚀",
        "{author} sends {target} flying! 💨",
        "{author} yeets {target} into orbit! 🌍🚀",
        "{author} absolutely YEETS {target}! 🔥",
    ],
}

ACTION_COLORS = {
    "kiss": 0xFF69B4,
    "hug": 0x87CEEB,
    "cuddle": 0xDEB887,
    "pat": 0xFFD700,
    "bonk": 0xFF4500,
    "slap": 0xDC143C,
    "punch": 0x8B0000,
    "kick": 0x8B4513,
    "lick": 0x9370DB,
    "flirt": 0xFF1493,
    "kill": 0x2F2F2F,
    "bite": 0xCD853F,
    "boop": 0x98FB98,
    "pinch": 0xFFA07A,
    "flick": 0x4682B4,
    "tackle": 0x556B2F,
    "throw": 0xDAA520,
    "spit": 0x808080,
    "yeet": 0xFF8C00,
}

for action in list(ACTION_GIFS.keys()):
    cmd_name = action
    gif_list = ACTION_GIFS[action]
    msg_list = ACTION_MESSAGES[action]
    color = ACTION_COLORS[action]

    @bot.command(name=cmd_name)
    async def action_cmd(ctx, member: discord.Member = None):
        act = ctx.command.name
        gifs = ACTION_GIFS[act]
        msgs = ACTION_MESSAGES[act]
        c = ACTION_COLORS[act]
        target = member if member else ctx.author
        msg = random.choice(msgs).format(author=ctx.author.mention, target=target.mention)
        gif_url = random.choice(gifs)
        count = get_count(ctx.author.id, target.id, act)
        record_use(ctx.author.id, target.id, act)
        embed = discord.Embed(description=msg, color=c)
        embed.set_image(url=gif_url)
        embed.set_footer(text=f"{target.display_name} has been {act}ed {count + 1} times")
        await ctx.send(embed=embed)

@bot.command(name="marry")
async def marry(ctx, member: discord.Member):
    author_id = str(ctx.author.id)
    target_id = str(member.id)

    if author_id == target_id:
        await ctx.send("You can't marry yourself, silly! 🙃")
        return

    if target_id in marriages and marriages[target_id]["spouse"] == author_id:
        await ctx.send("You're already married! 💍")
        return

    if author_id in marriages:
        await ctx.send("You're already married! Divorce first with `;divorce` 💔")
        return

    if target_id in marriages:
        await ctx.send(f"{member.mention} is already married to someone else! 💔")
        return

    gif_url = random.choice(PROPOSAL_GIFS)
    embed = discord.Embed(
        title="💍 Marriage Proposal!",
        description=f"{ctx.author.mention} is proposing to {member.mention}! Will you accept? 💕",
        color=0xFF69B4
    )
    embed.set_image(url=gif_url)

    accept = Button(label="💍 Accept", style=discord.ButtonStyle.green)
    decline = Button(label="💔 Decline", style=discord.ButtonStyle.red)

    async def accept_cb(interaction):
        if interaction.user.id != member.id:
            await interaction.response.send_message("Only the one being proposed to can accept!", ephemeral=True)
            return
        marriages[target_id] = {"spouse": author_id, "date": datetime.now(timezone.utc).isoformat()}
        save_json(MARRIAGE_FILE, marriages)
        gif = random.choice(ACCEPT_GIFS)
        emb = discord.Embed(
            title="🎉 Married!",
            description=f"{ctx.author.mention} and {member.mention} are now married! 💍💕",
            color=0xFF69B4
        )
        emb.set_image(url=gif)
        await interaction.response.edit_message(embed=emb, view=None)

    async def decline_cb(interaction):
        if interaction.user.id != member.id:
            await interaction.response.send_message("Only the one being proposed to can decline!", ephemeral=True)
            return
        gif = random.choice(DECLINE_GIFS)
        emb = discord.Embed(
            title="💔 Rejected!",
            description=f"{member.mention} declined the proposal... 😢",
            color=0x808080
        )
        emb.set_image(url=gif)
        await interaction.response.edit_message(embed=emb, view=None)

    accept.callback = accept_cb
    decline.callback = decline_cb
    view = View()
    view.add_item(accept)
    view.add_item(decline)
    await ctx.send(embed=embed, view=view)

@bot.command(name="divorce")
async def divorce(ctx):
    author_id = str(ctx.author.id)
    if author_id not in marriages:
        await ctx.send("You're not even married! 💀")
        return
    del marriages[author_id]
    save_json(MARRIAGE_FILE, marriages)
    await ctx.send(f"{ctx.author.mention} got divorced... 💔 It's over.")

@bot.command(name="stats")
async def stats_cmd(ctx, member: discord.Member = None):
    target = member if member else ctx.author
    target_key = str(target.id)
    lines = []
    total = 0
    for author_key, targets in stats.items():
        if target_key in targets:
            for cmd, count in targets[target_key].items():
                lines.append(f"• **{cmd}** — {count} times")
                total += count
    if not lines:
        await ctx.send(f"{target.mention} hasn't been actioned yet... 🤔")
        return
    embed = discord.Embed(
        title=f"📊 Stats for {target.display_name}",
        description="\n".join(lines) + f"\n\n**Total: {total}**",
        color=0x00BFFF
    )
    await ctx.send(embed=embed)

TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ DISCORD_TOKEN not set in environment")
