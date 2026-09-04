import discord
from discord.ext import commands
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

# ── Action GIFs & Messages ────────────────────────────

ACTION_GIFS = {
    "kiss": [
        "https://tenor.com/view/kiss-anime-kiss-anime-gif-18292283",
        "https://tenor.com/view/anime-kiss-love-romantic-couple-gif-13968388",
        "https://tenor.com/view/anime-kiss-lip-kiss-gif-14566668",
        "https://tenor.com/view/anime-kiss-mwah-love-gif-17984512",
        "https://tenor.com/view/anime-kiss-smooch-gif-17367580",
    ],
    "marry": [
        "https://tenor.com/view/wedding-anime-couple-marriage-proposal-gif-17966152",
        "https://tenor.com/view/anime-wedding-marriage-love-couple-gif-13968470",
        "https://tenor.com/view/anime-marry-me-propose-engagement-gif-16815477",
        "https://tenor.com/view/anime-marriage-bride-groom-gif-17984513",
        "https://tenor.com/view/anime-wedding-ceremony-gif-17367581",
    ],
    "kick": [
        "https://tenor.com/view/anime-kick-fight-gif-17984490",
        "https://tenor.com/view/anime-kick-gif-17367568",
        "https://tenor.com/view/anime-kick-ass-kick-gif-14566285",
        "https://tenor.com/view/anime-flying-kick-gif-17984514",
        "https://tenor.com/view/anime-drop-kick-gif-17367582",
    ],
    "punch": [
        "https://tenor.com/view/anime-punch-fight-gif-17984493",
        "https://tenor.com/view/punch-anime-punch-gif-14000175",
        "https://tenor.com/view/anime-punch-gif-17367569",
        "https://tenor.com/view/anime-strong-punch-gif-17984515",
        "https://tenor.com/view/anime-uppercut-gif-17367583",
    ],
    "slap": [
        "https://tenor.com/view/anime-slap-gif-17984500",
        "https://tenor.com/view/anime-slap-gif-17367563",
        "https://tenor.com/view/slap-anime-slap-gif-14000176",
        "https://tenor.com/view/anime-hard-slap-gif-17984516",
        "https://tenor.com/view/anime-slap-fight-gif-17367584",
    ],
    "cuddle": [
        "https://tenor.com/view/anime-cuddle-hug-love-gif-17984496",
        "https://tenor.com/view/anime-cuddle-love-sweet-gif-13968472",
        "https://tenor.com/view/cuddle-anime-cuddle-gif-14000177",
        "https://tenor.com/view/anime-cuddle-snuggle-gif-17984517",
        "https://tenor.com/view/anime-cuddle-bed-gif-17367585",
    ],
    "lick": [
        "https://tenor.com/view/anime-lick-tongue-gif-17984503",
        "https://tenor.com/view/anime-lick-gif-17367566",
        "https://tenor.com/view/lick-anime-lick-gif-14000179",
        "https://tenor.com/view/anime-lick-face-gif-17984518",
        "https://tenor.com/view/anime-big-lick-gif-17367586",
    ],
    "hug": [
        "https://tenor.com/view/anime-hug-hug-anime-cuddle-gif-17984495",
        "https://tenor.com/view/anime-hug-gif-17367567",
        "https://tenor.com/view/hug-anime-hug-gif-14000178",
        "https://tenor.com/view/anime-big-hug-gif-17984519",
        "https://tenor.com/view/anime-group-hug-gif-17367587",
    ],
    "pat": [
        "https://tenor.com/view/anime-pat-head-pat-gif-17984499",
        "https://tenor.com/view/anime-pat-gif-17367564",
        "https://tenor.com/view/pat-anime-pat-gif-14000180",
        "https://tenor.com/view/anime-head-pat-gif-17984520",
        "https://tenor.com/view/anime-gentle-pat-gif-17367588",
    ],
    "bonk": [
        "https://tenor.com/view/anime-bonk-hit-head-gif-17984491",
        "https://tenor.com/view/anime-bonk-gif-17367570",
        "https://tenor.com/view/bonk-anime-bonk-gif-14000181",
        "https://tenor.com/view/anime-bonk-hammer-gif-17984521",
        "https://tenor.com/view/anime-bonk-stick-gif-17367589",
    ],
    "flirt": [
        "https://tenor.com/view/anime-flirt-wink-gif-17984501",
        "https://tenor.com/view/anime-flirt-gif-17367565",
        "https://tenor.com/view/anime-flirty-eyes-gif-14000182",
        "https://tenor.com/view/anime-flirt-smile-gif-17984522",
        "https://tenor.com/view/anime-flirt-blush-gif-17367590",
    ],
    "kill": [
        "https://tenor.com/view/anime-kill-murder-death-gif-17984492",
        "https://tenor.com/view/anime-kill-gif-17367571",
        "https://tenor.com/view/kill-anime-kill-gif-14000183",
        "https://tenor.com/view/anime-kill-sword-gif-17984523",
        "https://tenor.com/view/anime-death-stab-gif-17367591",
    ],
    "bite": [
        "https://tenor.com/view/anime-bite-gif-17367572",
        "https://tenor.com/view/anime-bite-chomp-gif-17984504",
        "https://tenor.com/view/bite-anime-bite-gif-14000184",
        "https://tenor.com/view/anime-bite-nom-gif-17984524",
        "https://tenor.com/view/anime-bite-shark-gif-17367592",
    ],
    "boop": [
        "https://tenor.com/view/anime-boop-gif-17367573",
        "https://tenor.com/view/anime-boop-nose-gif-17984505",
        "https://tenor.com/view/boop-anime-boop-gif-14000185",
        "https://tenor.com/view/anime-boop-sweet-gif-17984525",
        "https://tenor.com/view/anime-boop-finger-gif-17367593",
    ],
    "pinch": [
        "https://tenor.com/view/anime-pinch-gif-17367574",
        "https://tenor.com/view/anime-pinch-cheek-gif-17984506",
        "https://tenor.com/view/pinch-anime-pinch-gif-14000186",
        "https://tenor.com/view/anime-pinch-squeeze-gif-17984526",
        "https://tenor.com/view/anime-pinch-face-gif-17367594",
    ],
    "flick": [
        "https://tenor.com/view/anime-flick-gif-17367575",
        "https://tenor.com/view/anime-flick-forehead-gif-17984507",
        "https://tenor.com/view/flick-anime-flick-gif-14000187",
        "https://tenor.com/view/anime-flick-nose-gif-17984527",
        "https://tenor.com/view/anime-flick-head-gif-17367595",
    ],
    "tackle": [
        "https://tenor.com/view/anime-tackle-gif-17367576",
        "https://tenor.com/view/anime-tackle-hug-gif-17984508",
        "https://tenor.com/view/tackle-anime-tackle-gif-14000188",
        "https://tenor.com/view/anime-tackle-flying-gif-17984528",
        "https://tenor.com/view/anime-tackle-body-slam-gif-17367596",
    ],
    "throw": [
        "https://tenor.com/view/anime-throw-gif-17367577",
        "https://tenor.com/view/anime-throw-away-gif-17984509",
        "https://tenor.com/view/throw-anime-throw-gif-14000189",
        "https://tenor.com/view/anime-throw-far-gif-17984529",
        "https://tenor.com/view/anime-toss-gif-17367597",
    ],
    "spit": [
        "https://tenor.com/view/anime-spit-gif-17367578",
        "https://tenor.com/view/anime-spit-out-gif-17984510",
        "https://tenor.com/view/spit-anime-spit-gif-14000190",
        "https://tenor.com/view/anime-spit-water-gif-17984530",
        "https://tenor.com/view/anime-spit-dramatic-gif-17367598",
    ],
    "yeet": [
        "https://tenor.com/view/anime-yeet-gif-17367579",
        "https://tenor.com/view/anime-yeet-away-gif-17984511",
        "https://tenor.com/view/yeet-anime-yeet-gif-14000191",
        "https://tenor.com/view/anime-yeet-fly-gif-17984531",
        "https://tenor.com/view/anime-yeet-launch-gif-17367599",
    ],
}

ACTION_MESSAGES = {
    "kiss": [
        "{author} gives {target} a sweet kiss! 💋",
        "{author} plants a kiss on {target}'s cheek! 😘",
        "{author} kisses {target} passionately! 🔥",
        "{author} sneakily steals a kiss from {target}! 🥰",
    ],
    "marry": [
        "{author} proposes to {target}! Will they say yes? 💍",
        "{author} marries {target} in a beautiful ceremony! 💒",
        "{author} and {target} are now married! Congrats! 🎉",
        "{author} sweeps {target} off their feet and elopes! 💕",
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
        "{author} gives {target} a mighty bonk! 🛍️",
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
        "{author} CHOMP — {target} got bit! 💈",
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
        "{author} pinches {target} — ouch! 🨫",
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
    "kiss": "#FF69B4", "marry": "#FF69B4", "cuddle": "#FF69B4", "hug": "#FF69B4", "flirt": "#FF69B4",
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


# ── Generic action command factory ─────────────────────

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


# ── Special marry command ────────────────────────────

@bot.command(name="marry")
async def cmd_marry(ctx, member: discord.Member = None):
    if member is None or member == ctx.author:
        await ctx.send("You need to mention someone to marry!")
        return

    record_use(ctx.author.id, member.id, "marry")
    count = get_count(ctx.author.id, member.id, "marry")

    author_key = str(ctx.author.id)
    target_key = str(member.id)
    marriage_key = f"{author_key}_{target_key}"

    # If not married yet, record the date
    if marriage_key not in marriages:
        marriages[marriage_key] = {
            "author_id": ctx.author.id,
            "target_id": member.id,
            "date": datetime.now(timezone.utc).isoformat()
        }
        save_json(MARRIAGE_FILE, marriages)

    # Build the embed
    msg_template = random.choice(ACTION_MESSAGES["marry"])
    message = msg_template.format(author=ctx.author.mention, target=member.mention)
    gif_url = random.choice(ACTION_GIFS["marry"])
    color = discord.Color.from_str("#FF69B4")
    embed = discord.Embed(description=message, color=color)
    embed.set_image(url=gif_url)

    # Marriage date & days since
    wedding_date = datetime.fromisoformat(marriages[marriage_key]["date"])
    days_married = (datetime.now(timezone.utc) - wedding_date).days
    date_str = wedding_date.strftime("%B %d, %Y")
    embed.add_field(
        name="💍 Married since",
        value=f"{date_str} — **{days_married}** day{'s' if days_married != 1 else ''} together!",
        inline=False
    )

    embed.set_footer(text=f"#{count} — you've married them {count} times")
    await ctx.send(embed=embed)


# ── Stats command ──────────────────────────────

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


# ── Divorce command ───────────────────────────────

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
    embed.set_image(url="https://tenor.com/view/anime-sad-cry-gif-17984532")
    await ctx.send(embed=embed)


# ── On ready ──────────────────────────────────

@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online and ready!")
    print(f"   Bot ID: {bot.user.id}")
    print(f"   Servers: {len(bot.guilds)}")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=";kiss | ;stats | ;bonk"
    ))


# ── Run ───────────────────────────────────

if __name__ == "__main__":
    import os
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        token = "YOUR_BOT_TOKEN_HERE"
    bot.run(token)