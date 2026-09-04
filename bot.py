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

# ── Action GIFs & Messages (direct .gif URLs for Discord) ─────

ACTION_GIFS = {
    "kiss": [
        "https://tenor.com/18292283.gif",
        "https://tenor.com/13968388.gif",
        "https://tenor.com/14566668.gif",
        "https://tenor.com/17984512.gif",
        "https://tenor.com/17367580.gif",
    ],
    "kick": [
        "https://tenor.com/17984490.gif",
        "https://tenor.com/17367568.gif",
        "https://tenor.com/14566285.gif",
        "https://tenor.com/17984514.gif",
        "https://tenor.com/17367582.gif",
    ],
    "punch": [
        "https://tenor.com/17984493.gif",
        "https://tenor.com/14000175.gif",
        "https://tenor.com/17367569.gif",
        "https://tenor.com/17984515.gif",
        "https://tenor.com/17367583.gif",
    ],
    "slap": [
        "https://tenor.com/17984500.gif",
        "https://tenor.com/17367563.gif",
        "https://tenor.com/14000176.gif",
        "https://tenor.com/17984516.gif",
        "https://tenor.com/17367584.gif",
    ],
    "cuddle": [
        "https://tenor.com/17984496.gif",
        "https://tenor.com/13968472.gif",
        "https://tenor.com/14000177.gif",
        "https://tenor.com/17984517.gif",
        "https://tenor.com/17367585.gif",
    ],
    "lick": [
        "https://tenor.com/17984503.gif",
        "https://tenor.com/17367566.gif",
        "https://tenor.com/14000179.gif",
        "https://tenor.com/17984518.gif",
        "https://tenor.com/17367586.gif",
    ],
    "hug": [
        "https://tenor.com/17984495.gif",
        "https://tenor.com/17367567.gif",
        "https://tenor.com/14000178.gif",
        "https://tenor.com/17984519.gif",
        "https://tenor.com/17367587.gif",
    ],
    "pat": [
        "https://tenor.com/17984499.gif",
        "https://tenor.com/17367564.gif",
        "https://tenor.com/14000180.gif",
        "https://tenor.com/17984520.gif",
        "https://tenor.com/17367588.gif",
    ],
    "bonk": [
        "https://tenor.com/17984491.gif",
        "https://tenor.com/17367570.gif",
        "https://tenor.com/14000181.gif",
        "https://tenor.com/17984521.gif",
        "https://tenor.com/17367589.gif",
    ],
    "flirt": [
        "https://tenor.com/17984501.gif",
        "https://tenor.com/17367565.gif",
        "https://tenor.com/14000182.gif",
        "https://tenor.com/17984522.gif",
        "https://tenor.com/17367590.gif",
    ],
    "kill": [
        "https://tenor.com/17984492.gif",
        "https://tenor.com/17367571.gif",
        "https://tenor.com/14000183.gif",
        "https://tenor.com/17984523.gif",
        "https://tenor.com/17367591.gif",
    ],
    "bite": [
        "https://tenor.com/17367572.gif",
        "https://tenor.com/17984504.gif",
        "https://tenor.com/14000184.gif",
        "https://tenor.com/17984524.gif",
        "https://tenor.com/17367592.gif",
    ],
    "boop": [
        "https://tenor.com/17367573.gif",
        "https://tenor.com/17984505.gif",
        "https://tenor.com/14000185.gif",
        "https://tenor.com/17984525.gif",
        "https://tenor.com/17367593.gif",
    ],
    "pinch": [
        "https://tenor.com/17367574.gif",
        "https://tenor.com/17984506.gif",
        "https://tenor.com/14000186.gif",
        "https://tenor.com/17984526.gif",
        "https://tenor.com/17367594.gif",
    ],
    "flick": [
        "https://tenor.com/17367575.gif",
        "https://tenor.com/17984507.gif",
        "https://tenor.com/14000187.gif",
        "https://tenor.com/17984527.gif",
        "https://tenor.com/17367595.gif",
    ],
    "tackle": [
        "https://tenor.com/17367576.gif",
        "https://tenor.com/17984508.gif",
        "https://tenor.com/14000188.gif",
        "https://tenor.com/17984528.gif",
        "https://tenor.com/17367596.gif",
    ],
    "throw": [
        "https://tenor.com/17367577.gif",
        "https://tenor.com/17984509.gif",
        "https://tenor.com/14000189.gif",
        "https://tenor.com/17984529.gif",
        "https://tenor.com/17367597.gif",
    ],
    "spit": [
        "https://tenor.com/17367578.gif",
        "https://tenor.com/17984510.gif",
        "https://tenor.com/14000190.gif",
        "https://tenor.com/17984530.gif",
        "https://tenor.com/17367598.gif",
    ],
    "yeet": [
        "https://tenor.com/17367579.gif",
        "https://tenor.com/17984511.gif",
        "https://tenor.com/14000191.gif",
        "https://tenor.com/17984531.gif",
        "https://tenor.com/17367599.gif",
    ],
}

MARRY_GIFS = [
    "https://tenor.com/17966152.gif",
    "https://tenor.com/13968470.gif",
    "https://tenor.com/16815477.gif",
    "https://tenor.com/17984513.gif",
    "https://tenor.com/17367581.gif",
]

PROPOSAL_GIFS = [
    "https://tenor.com/17984533.gif",
    "https://tenor.com/17367600.gif",
    "https://tenor.com/17984534.gif",
    "https://tenor.com/17367601.gif",
    "https://tenor.com/17984535.gif",
]

ACCEPT_GIFS = [
    "https://tenor.com/17984536.gif",
    "https://tenor.com/17367602.gif",
    "https://tenor.com/17984537.gif",
    "https://tenor.com/17367603.gif",
    "https://tenor.com/17984538.gif",
]

DECLINE_GIFS = [
    "https://tenor.com/17984539.gif",
    "https://tenor.com/17984532.gif",
    "https://tenor.com/17367604.gif",
    "https://tenor.com/17984540.gif",
    "https://tenor.com/17367605.gif",
]

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


# ── Marry View (Accept/Decline buttons) ───────────────

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
    embed.set_image(url="https://tenor.com/17984532.gif")
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