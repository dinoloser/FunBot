import discord
from discord.ext import commands
from discord.ui import Button, View
import random
import json
import os
from collections import defaultdict
from datetime import datetime, timezone

# ── Bot setup ──────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=";", intents=intents)

# ── Stats storage ─────────────────────────────────────
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

# ── Action GIFs (direct image URLs for Discord) ─────

ACTION_GIFS = {
    "kiss": [
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/38/bf/r71hHE9Atl1sF5iG.gif",
        "https://static.klipy.com/ii/ce286d05b8e1a47cd4f32b0e1b6dec0e/50/04/ohEWptJ8.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/fa/e9/9jQskLgUqjRrS.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/8a/5d/5sYTBY6Hwxore9ojwn.gif",
    ],
    "hug": [
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/12/67/JrFwx5E7OyvjDUn6P7O.gif",
        "https://static.klipy.com/ii/935d7ab9d8c6202580a668421940ec81/e0/6b/PaJxcbRP.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/56/05/M2hUrYKcdAr91JXjk.gif",
        "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/3b/a1/cCDLjYxd.gif",
        "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/26/df/M42jO6Xq.gif",
        "https://static.klipy.com/ii/e293a233a303a98e471f78d04e13a1b0/4c/79/Vm71YRIu.gif",
    ],
    "cuddle": [
        "https://static.klipy.com/ii/7607a26399874a14744aa5e7accfa062/b4/b4/tXYJWuWJ.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/ba/90/OOpAMLi3qc5fzg1tHA7.gif",
        "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/26/df/M42jO6Xq.gif",
        "https://static.klipy.com/ii/e293a233a303a98e471f78d04e13a1b0/4c/79/Vm71YRIu.gif",
    ],
    "pat": [
        "https://static.klipy.com/ii/c3a19a0b747a76e98651f2b9a3cca5ff/c2/73/SjYIk5nC.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/54/8f/CHtBjQ9ItN9M78.gif",
        "https://static.klipy.com/ii/9ed0121ed465c12e1f3dda331ed33f0e/df/6c/qdgkKrbYfTC1pkbxeN.gif",
    ],
    "bonk": [
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/85/9c/t6Zu7IamibnD5Pp.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/26/7f/N1t4DyZECmQRAKnU.gif",
        "https://static.klipy.com/ii/f87f46a2c5aeaeed4c68910815f73eaf/6c/76/LjmbXUjH.gif",
    ],
    "slap": [
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/73/ed/knLMcluv8Qab3JvIh.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/2a/ba/xc7sOkjNX3Wy.gif",
        "https://static.klipy.com/ii/f87f46a2c5aeaeed4c68910815f73eaf/6c/76/LjmbXUjH.gif",
    ],
    "punch": [
        "https://static.klipy.com/ii/a15b48460c436e1e92c85ffc680932cc/72/3b/rei0zkil.gif",
        "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/32/95/XtdxM0mg.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/73/ed/knLMcluv8Qab3JvIh.gif",
    ],
    "kick": [
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/e2/c7/9U7G7mfjvBqy4Mx.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/8f/02/gbsJsySiK66KGdciknH.gif",
        "https://static.klipy.com/ii/a15b48460c436e1e92c85ffc680932cc/72/3b/rei0zkil.gif",
    ],
    "lick": [
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/38/bf/r71hHE9Atl1sF5iG.gif",
        "https://static.klipy.com/ii/c3a19a0b747a76e98651f2b9a3cca5ff/c2/73/SjYIk5nC.gif",
        "https://static.klipy.com/ii/9ed0121ed465c12e1f3dda331ed33f0e/df/6c/qdgkKrbYfTC1pkbxeN.gif",
    ],
    "flirt": [
        "https://static.klipy.com/ii/ce286d05b8e1a47cd4f32b0e1b6dec0e/50/04/ohEWptJ8.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/8a/5d/5sYTBY6Hwxore9ojwn.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/fa/e9/9jQskLgUqjRrS.gif",
    ],
    "kill": [
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/8f/02/gbsJsySiK66KGdciknH.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/e2/c7/9U7G7mfjvBqy4Mx.gif",
        "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/32/95/XtdxM0mg.gif",
    ],
    "bite": [
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/73/ed/knLMcluv8Qab3JvIh.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/85/9c/t6Zu7IamibnD5Pp.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/26/7f/N1t4DyZECmQRAKnU.gif",
    ],
    "boop": [
        "https://static.klipy.com/ii/c3a19a0b747a76e98651f2b9a3cca5ff/c2/73/SjYIk5nC.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/54/8f/CHtBjQ9ItN9M78.gif",
        "https://static.klipy.com/ii/9ed0121ed465c12e1f3dda331ed33f0e/df/6c/qdgkKrbYfTC1pkbxeN.gif",
    ],
    "pinch": [
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/2a/ba/xc7sOkjNX3Wy.gif",
        "https://static.klipy.com/ii/f87f46a2c5aeaeed4c68910815f73eaf/6c/76/LjmbXUjH.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/26/7f/N1t4DyZECmQRAKnU.gif",
    ],
    "flick": [
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/2a/ba/xc7sOkjNX3Wy.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/85/9c/t6Zu7IamibnD5Pp.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/26/7f/N1t4DyZECmQRAKnU.gif",
    ],
    "tackle": [
        "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/32/95/XtdxM0mg.gif",
        "https://static.klipy.com/ii/a15b48460c436e1e92c85ffc680932cc/72/3b/rei0zkil.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/e2/c7/9U7G7mfjvBqy4Mx.gif",
    ],
    "throw": [
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/8f/02/gbsJsySiK66KGdciknH.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/e2/c7/9U7G7mfjvBqy4Mx.gif",
        "https://static.klipy.com/ii/a15b48460c436e1e92c85ffc680932cc/72/3b/rei0zkil.gif",
    ],
    "spit": [
        "https://static.klipy.com/ii/f87f46a2c5aeaeed4c68910815f73eaf/6c/76/LjmbXUjH.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/2a/ba/xc7sOkjNX3Wy.gif",
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/85/9c/t6Zu7IamibnD5Pp.gif",
    ],
    "yeet": [
        "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/8f/02/gbsJsySiK66KGdciknH.gif",
        "https://static.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/e2/c7/9U7G7mfjvBqy4Mx.gif",
        "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/32/95/XtdxM0mg.gif",
    ],
}

MARRY_GIFS = [
    "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/12/67/JrFwx5E7OyvjDUn6P7O.gif",
    "https://static.klipy.com/ii/935d7ab9d8c6202580a668421940ec81/e0/6b/PaJxcbRP.gif",
    "https://static.klipy.com/ii/d7aec6f6f171607374b2065c836f92f4/3b/a1/cCDLjYxd.gif",
]

PROPOSAL_GIFS = [
    "https://static.klipy.com/ii/ce286d05b8e1a47cd4f32b0e1b6dec0e/50/04/ohEWptJ8.gif",
    "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/38/bf/r71hHE9Atl1sF5iG.gif",
    "https://static.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/8a/5d/5sYTBY6Hwxore9ojwn.gif",
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

# ── Messages ──────────────────────────────────────────

ACTION_MESSAGES = {
    "kiss": [
        "{author} gives {target} a sweet kiss! 💋",
        "{author} plants a kiss on {target}'s cheek! 😘",
        "{author} kisses {target} passionately! 🔥",
        "{author} sneakily steals a kiss from {target}! 🥰",
    ],
    "kick": [
        "{author} kicks {target} across the room! 🦶‍♂️💨",
        "{author} delivers a powerful kick to {target}! 🥋",
        "{author} roundhouse kicks {target}! 💥",
        "{author} dropkicks {target} into next week! 🦵",
    ],
    "punch": [
        "{author} punches {target} square in the face! 💪",
        "{author} throws a haymaker at {target}! 💪",
        "{author} lands a solid punch on {target}! 💥",
        "{author} gives {target} a one-two combo! 🥊",
    ],
    "slap": [
        "{author} slaps {target} across the face! 🖐️",
        "{author} gives {target} a hard slap! 😱",
        "{author} slaps {target} — what did they do?! 😲",
        "{author} dramatically slaps {target}! 🎭",
    ],
    "cuddle": [
        "{author} cuddles {target} warmly! 🥰",
        "{author} snuggles up to {target}! 🧸",
        "{author} wraps {target} in a cozy cuddle! 💕",
        "{author} spoons {target} gently! 🥄",
    ],
    "lick": [
        "{author} licks {target}! 👅",
        "{author} gives {target} a big lick! 😝",
        "{author} sneakily licks {target}! 🤪",
        "{author} licks {target} like a lollipop! 🍭",
    ],
    "hug": [
        "{author} gives {target} a warm hug! 🤗",
        "{author} wraps {target} in a big hug! 🫂",
        "{author} hugs {target} tightly! 💞",
        "{author} bear-hugs {target} out of nowhere! 🐻",
    ],
    "pat": [
        "{author} pats {target} on the head! 🐱",
        "{author} gently pats {target}! ✨",
        "{author} gives {target} a reassuring pat! 🥹",
        "{author} pats {target} like a good puppy! 🐶",
    ],
    "bonk": [
        "{author} bonks {target} on the head! 🔨",
        "{author} gives {target} a mighty bonk! 🛎️",
        "{author} bonks {target} — straight to horny jail! 🚨",
        "{author} bonks {target} into next week! 💫",
    ],
    "flirt": [
        "{author} flirts with {target}! 😏",
        "{author} winks at {target} seductively! 💋",
        "{author} slides into {target}'s DMs IRL! 🔥",
        "{author} gives {target} a smooth pickup line! 🌹",
    ],
    "kill": [
        "{author} kills {target}! 💀",
        "{author} eliminates {target}! ⚔️",
        "{author} murders {target} brutally! 🔪",
        "{author} sends {target} to the shadow realm! 🌑",
    ],
    "bite": [
        "{author} bites {target}! 🦷",
        "{author} chomps down on {target}! 🐊",
        "{author} gives {target} a little nibble! 😬",
        "{author} CHOMP — {target} got bit! 🦈",
    ],
    "boop": [
        "{author} boops {target}'s nose! 👆",
        "{author} gently boops {target}! 🥹",
        "{author} sneaks a boop on {target}! ✨",
        "{author} boops {target} right on the snoot! 👃",
    ],
    "pinch": [
        "{author} pinches {target}'s cheek! 🤏",
        "{author} gives {target} a little pinch! 😈",
        "{author} pinches {target} — ouch! 🫣",
        "{author} pinches {target}'s nose! 👃",
    ],
    "flick": [
        "{author} flicks {target}'s forehead! 👋",
        "{author} gives {target} a quick flick! 🤪",
        "{author} flicks {target} — right on the nose! 😛",
        "{author} flick-flick-flicks {target}! 👌",
    ],
    "tackle": [
        "{author} tackles {target} to the ground! 🏈",
        "{author} leaps and tackles {target}! 💨",
        "{author} full-on tackles {target}! 💥",
        "{author} comes flying in and tackles {target}! ✈️",
    ],
    "throw": [
        "{author} throws {target} across the room! 🌀",
        "{author} yeets {target} into the distance! 🚀",
        "{author} hurls {target} like a frisbee! 🥏",
        "{author} tosses {target} like a ragdoll! 🧸",
    ],
    "spit": [
        "{author} spits on {target}! 💦",
        "{author} hocks a loogie at {target}! 🤮",
        "{author} spits in {target}'s general direction! 🧂",
        "{author} dramatically spits to the side! 🎬",
    ],
    "yeet": [
        "{author} YEETS {target} into the void! 🌌",
        "{author} sends {target} flying across the server! 🚀",
        "{author} violently yeets {target} into orbit! 🛸",
        "{author} YEET — and {target} is gone! 💨",
    ],
}

COLOR_MAP = {
    "kiss": "#FF69B4", "cuddle": "#FF69B4", "hug": "#FF69B4", "flirt": "#FF69B4",
    "pat": "#FFD700", "boop": "#FFD700",
    "bonk": "#FFA500",
    "kill": "#000000",
    "bite": "#8B0000", "pinch": "#8B0000", "flick": "#8B0000",
    "tackle": "#4B0082", "throw": "#4B0082", "yeet": "#4B0082", "spit": "#4B0082",
}

def action_embed(author: discord.Member, target: discord.Member, action: str, count: int = None):
    msg_template = random.choice(ACTION_MESSAGES[action])
    message = msg_template.format(author=author.mention, target=target.mention)
    gif_url = random.choice(ACTION_GIFS[action])
    color = discord.Color.from_str(COLOR_MAP.get(action, "#FF0000"))
    embed = discord.Embed(description=message, color=color)
    embed.set_image(url=gif_url)
    if count is not None and count > 0:
        embed.set_footer(text=f"#{count} — you've used ;{action} on them {count} times")
    return embed


# ── Marry View (Accept/Decline buttons) ───────────────(
class MarryView(View):
    def __init__(self, proposer: discord.Member, target: discord.Member):
        super().__init__(timeout=60.0)
        self.proposer = proposer
        self.target = target
        self.answered = False

    async def disable_buttons(self, interaction: discord.Interaction):
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

    @discord.ui.button(label="💍 Accept", style=discord.ButtonStyle.success, emoji="✅")
    async def accept_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.target.id:
            await interaction.response.send_message(f"Only {self.target.mention} can accept this proposal!", ephemeral=True)
            return
        self.answered = True

        # Record marriage
        author_key = str(self.proposer.id)
        target_key = str(self.target.id)
        marriage_key = f"{author_key}_{target_key}"
        marriages[marriage_key] = {
            "author_id": self.proposer.id,
            "target_id": self.target.id,
            "date": datetime.now(timezone.utc).isoformat()
        }
        save_json(MARRIAGE_FILE, marriages)

        gif_url = random.choice(ACCEPT_GIFS)
        embed = discord.Embed(
            description=f"💍 **{self.proposer.mention} & {self.target.mention} are now married!** 🎉\nThey said yes! 💕",
            color=discord.Color.from_str("#FF69B4")
        )
        embed.set_image(url=gif_url)
        wedding_date = datetime.fromisoformat(marriages[marriage_key]["date"])
        date_str = wedding_date.strftime("%B %d, %Y")
        embed.set_footer(text=f"Married on {date_str}")

        await self.disable_buttons(interaction)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="💔 Decline", style=discord.ButtonStyle.danger, emoji="❌")
    async def decline_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.target.id:
            await interaction.response.send_message(f"Only {self.target.mention} can decline this proposal!", ephemeral=True)
            return
        self.answered = True

        gif_url = random.choice(DECLINE_GIFS)
        embed = discord.Embed(
            description=f"💔 {self.proposer.mention} proposed to {self.target.mention}... but they said no... 😢",
            color=discord.Color.dark_gray()
        )
        embed.set_image(url=gif_url)

        await self.disable_buttons(interaction)
        await interaction.response.edit_message(embed=embed, view=self)

    async def on_timeout(self):
        self.answered = True
        for child in self.children:
            child.disabled = True


def make_action_command(name: str):
    @bot.command(name=name)
    async def cmd(ctx, member: discord.Member = None):
        if member is None or member == ctx.author:
            await ctx.send(f"You need to mention someone to {name}!")
            return
        record_use(ctx.author.id, member.id, name)
        count = get_count(ctx.author.id, member.id, name)
        embed = action_embed(ctx.author, member, name, count)
        await ctx.send(embed=embed)
    return cmd

for action in ACTION_GIFS:
    make_action_command(action)


# ── Special marry command ───────────────────────────────

@bot.command(name="marry")
async def cmd_marry(ctx, member: discord.Member = None):
    if member is None or member == ctx.author:
        await ctx.send("You need to mention someone to marry!")
        return

    # Check if already married to this person
    marriage_key = f"{str(ctx.author.id)}_{str(member.id)}"
    if marriage_key in marriages:
        wedding_date = datetime.fromisoformat(marriages[marriage_key]["date"])
        days_married = (datetime.now(timezone.utc) - wedding_date).days
        date_str = wedding_date.strftime("%B %d, %Y")
        embed = discord.Embed(
            description=f"💍 You're already married to {member.mention}!\nSince {date_str} — **{days_married}** days together! 💕",
            color=discord.Color.from_str("#FF69B4")
        )
        embed.set_image(url=random.choice(MARRY_GIFS))
        await ctx.send(embed=embed)
        return

    # Send proposal
    record_use(ctx.author.id, member.id, "marry")
    count = get_count(ctx.author.id, member.id, "marry")

    gif_url = random.choice(PROPOSAL_GIFS)
    embed = discord.Embed(
        description=f"💍 {ctx.author.mention} is down on one knee...\n**{member.mention}, will you marry them?** 💕",
        color=discord.Color.from_str("#FF69B4")
    )
    embed.set_image(url=gif_url)
    embed.set_footer(text=f"#{count} — you've proposed to them {count} times")

    view = MarryView(ctx.author, member)
    await ctx.send(embed=embed, view=view)


# ── Stats command ───────────────────────────────────────

@bot.command(name="stats")
async def cmd_stats(ctx, member: discord.Member = None):
    author_key = str(ctx.author.id)

    if member is None:
        if author_key not in stats or not stats[author_key]:
            await ctx.send("You haven't used any commands yet! Go ;kiss @someone!")
            return

        total = 0
        target_totals = defaultdict(int)
        command_totals = defaultdict(int)

        for t_key, commands_dict in stats[author_key].items():
            for cmd_name, count in commands_dict.items():
                total += count
                target_totals[t_key] += count
                command_totals[cmd_name] += count

        top_target_id = max(target_totals, key=target_totals.get)
        top_target = ctx.guild.get_member(int(top_target_id))
        top_target_name = top_target.display_name if top_target else f"User {top_target_id}"

        top_cmd = max(command_totals, key=command_totals.get)

        embed = discord.Embed(
            title=f"📊 {ctx.author.display_name}'s Command Stats",
            description=f"**Total commands used:** {total}",
            color=discord.Color.blue()
        )
        embed.add_field(name="🎯 Most targeted", value=top_target_name, inline=True)
        embed.add_field(name="⚡ Favorite command", value=f";{top_cmd}", inline=True)

        sorted_targets = sorted(target_totals.items(), key=lambda x: -x[1])[:5]
        targets_text = ""
        for t_key, count in sorted_targets:
            t_member = ctx.guild.get_member(int(t_key))
            t_name = t_member.display_name if t_member else f"User {t_key}"
            targets_text += f"• {t_name}: **{count}** times\n"
        if targets_text:
            embed.add_field(name="Top targets", value=targets_text, inline=False)

        await ctx.send(embed=embed)

    else:
        target_key = str(member.id)
        if author_key not in stats or target_key not in stats[author_key]:
            await ctx.send(f"You haven't used any commands on {member.display_name} yet!")
            return

        user_stats = stats[author_key][target_key]
        total = sum(user_stats.values())
        sorted_cmds = sorted(user_stats.items(), key=lambda x: -x[1])

        embed = discord.Embed(
            title=f"📊 {ctx.author.display_name} x {member.display_name}",
            description=f"**Total:** {total} commands used on {member.mention}",
            color=discord.Color.blue()
        )

        cmd_list = ""
        for cmd_name, count in sorted_cmds:
            cmd_list += f"`;{cmd_name}`: **{count}** times\n"
        embed.add_field(name="Command breakdown", value=cmd_list, inline=False)

        # Check if they're married
        marriage_key = f"{author_key}_{target_key}"
        if marriage_key in marriages:
            wedding_date = datetime.fromisoformat(marriages[marriage_key]["date"])
            days_married = (datetime.now(timezone.utc) - wedding_date).days
            date_str = wedding_date.strftime("%B %d, %Y")
            embed.add_field(
                name="💍 Marriage",
                value=f"Married on {date_str} — **{days_married}** day{'s' if days_married != 1 else ''}!",
                inline=False
            )

        await ctx.send(embed=embed)


# ── Divorce command ─────────────────────────────────────

@bot.command(name="divorce")
async def cmd_divorce(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("Mention who you want to divorce!")
        return
    marriage_key = f"{str(ctx.author.id)}_{str(member.id)}"
    if marriage_key not in marriages:
        await ctx.send(f"You're not even married to {member.mention}!")
        return
    del marriages[marriage_key]
    save_json(MARRIAGE_FILE, marriages)
    embed = discord.Embed(
        description=f"💔 {ctx.author.mention} divorced {member.mention}... it's over.",
        color=discord.Color.dark_gray()
    )
    embed.set_image(url=random.choice(DECLINE_GIFS))
    await ctx.send(embed=embed)


# ── On ready ────────────────────────────────────────────

@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online and ready!")
    print(f"   Bot ID: {bot.user.id}")
    print(f"   Servers: {len(bot.guilds)}")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=";kiss | ;stats | ;bonk"
    ))


# ── Run ─────────────────────────────────────────────────

if __name__ == "__main__":
    import os
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        token = "YOUR_BOT_TOKEN_HERE"
    bot.run(token)
