import discord
from discord.ext import commands
import random
import json
import os
from collections import defaultdict

# ── Bot setup ──────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=";", intents=intents)

# ── Stats storage ─────────────────────────────────────
STATS_FILE = "stats.json"

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)

stats = load_stats()

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
    save_stats(stats)

# ── Action GIFs & Messages ────────────────────────────

ACTION_GIFS = {
    "kiss": [
        "https://tenor.com/view/kiss-anime-kiss-anime-gif-18292283",
        "https://tenor.com/view/anime-kiss-love-romantic-couple-gif-13968388",
        "https://tenor.com/view/anime-kiss-lip-kiss-gif-14566668",
    ],
    "marry": [
        "https://tenor.com/view/wedding-anime-couple-marriage-proposal-gif-17966152",
        "https://tenor.com/view/anime-wedding-marriage-love-couple-gif-13968470",
        "https://tenor.com/view/anime-marry-me-propose-engagement-gif-16815477",
    ],
    "kick": [
        "https://tenor.com/view/anime-kick-fight-gif-17984490",
        "https://tenor.com/view/anime-kick-gif-17367568",
        "https://tenor.com/view/anime-kick-ass-kick-gif-14566285",
    ],
    "punch": [
        "https://tenor.com/view/anime-punch-fight-gif-17984493",
        "https://tenor.com/view/punch-anime-punch-gif-14000175",
        "https://tenor.com/view/anime-punch-gif-17367569",
    ],
    "slap": [
        "https://tenor.com/view/anime-slap-gif-17984500",
        "https://tenor.com/view/anime-slap-gif-17367563",
        "https://tenor.com/view/slap-anime-slap-gif-14000176",
    ],
    "cuddle": [
        "https://tenor.com/view/anime-cuddle-hug-love-gif-17984496",
        "https://tenor.com/view/anime-cuddle-love-sweet-gif-13968472",
        "https://tenor.com/view/cuddle-anime-cuddle-gif-14000177",
    ],
    "lick": [
        "https://tenor.com/view/anime-lick-tongue-gif-17984503",
        "https://tenor.com/view/anime-lick-gif-17367566",
        "https://tenor.com/view/lick-anime-lick-gif-14000179",
    ],
    "hug": [
        "https://tenor.com/view/anime-hug-hug-anime-cuddle-gif-17984495",
        "https://tenor.com/view/anime-hug-gif-17367567",
        "https://tenor.com/view/hug-anime-hug-gif-14000178",
    ],
    "pat": [
        "https://tenor.com/view/anime-pat-head-pat-gif-17984499",
        "https://tenor.com/view/anime-pat-gif-17367564",
        "https://tenor.com/view/pat-anime-pat-gif-14000180",
    ],
    "bonk": [
        "https://tenor.com/view/anime-bonk-hit-head-gif-17984491",
        "https://tenor.com/view/anime-bonk-gif-17367570",
        "https://tenor.com/view/bonk-anime-bonk-gif-14000181",
    ],
    "flirt": [
        "https://tenor.com/view/anime-flirt-wink-gif-17984501",
        "https://tenor.com/view/anime-flirt-gif-17367565",
        "https://tenor.com/view/anime-flirty-eyes-gif-14000182",
    ],
    "kill": [
        "https://tenor.com/view/anime-kill-murder-death-gif-17984492",
        "https://tenor.com/view/anime-kill-gif-17367571",
        "https://tenor.com/view/kill-anime-kill-gif-14000183",
    ],
    "bite": [
        "https://tenor.com/view/anime-bite-gif-17367572",
        "https://tenor.com/view/anime-bite-chomp-gif-17984504",
        "https://tenor.com/view/bite-anime-bite-gif-14000184",
    ],
    "boop": [
        "https://tenor.com/view/anime-boop-gif-17367573",
        "https://tenor.com/view/anime-boop-nose-gif-17984505",
        "https://tenor.com/view/boop-anime-boop-gif-14000185",
    ],
    "pinch": [
        "https://tenor.com/view/anime-pinch-gif-17367574",
        "https://tenor.com/view/anime-pinch-cheek-gif-17984506",
        "https://tenor.com/view/pinch-anime-pinch-gif-14000186",
    ],
    "flick": [
        "https://tenor.com/view/anime-flick-gif-17367575",
        "https://tenor.com/view/anime-flick-forehead-gif-17984507",
        "https://tenor.com/view/flick-anime-flick-gif-14000187",
    ],
    "tackle": [
        "https://tenor.com/view/anime-tackle-gif-17367576",
        "https://tenor.com/view/anime-tackle-hug-gif-17984508",
        "https://tenor.com/view/tackle-anime-tackle-gif-14000188",
    ],
    "throw": [
        "https://tenor.com/view/anime-throw-gif-17367577",
        "https://tenor.com/view/anime-throw-away-gif-17984509",
        "https://tenor.com/view/throw-anime-throw-gif-14000189",
    ],
    "spit": [
        "https://tenor.com/view/anime-spit-gif-17367578",
        "https://tenor.com/view/anime-spit-out-gif-17984510",
        "https://tenor.com/view/spit-anime-spit-gif-14000190",
    ],
    "yeet": [
        "https://tenor.com/view/anime-yeet-gif-17367579",
        "https://tenor.com/view/anime-yeet-away-gif-17984511",
        "https://tenor.com/view/yeet-anime-yeet-gif-14000191",
    ],
}

ACTION_MESSAGES = {
    "kiss": [
        "{author} gives {target} a sweet kiss! 💋",
        "{author} plants a kiss on {target}'s cheek! 😘",
        "{author} kisses {target} passionately! 🔥",
    ],
    "marry": [
        "{author} proposes to {target}! Will they say yes? 💍",
        "{author} marries {target} in a beautiful ceremony! 💒",
        "{author} and {target} are now married! Congrats! 🎉",
    ],
    "kick": [
        "{author} kicks {target} across the room! 🦶💨",
        "{author} delivers a powerful kick to {target}! 🥋",
        "{author} roundhouse kicks {target}! 💥",
    ],
    "punch": [
        "{author} punches {target} square in the face! 👊",
        "{author} throws a haymaker at {target}! 💪",
        "{author} lands a solid punch on {target}! 💥",
    ],
    "slap": [
        "{author} slaps {target} across the face! 🖐️",
        "{author} gives {target} a hard slap! 😱",
        "{author} slaps {target} — what did they do?! 😲",
    ],
    "cuddle": [
        "{author} cuddles {target} warmly! 🥰",
        "{author} snuggles up to {target}! 🧸",
        "{author} wraps {target} in a cozy cuddle! 💕",
    ],
    "lick": [
        "{author} licks {target}! 👅",
        "{author} gives {target} a big lick! 😝",
        "{author} sneakily licks {target}! 🤪",
    ],
    "hug": [
        "{author} gives {target} a warm hug! 🤗",
        "{author} wraps {target} in a big hug! 🫂",
        "{author} hugs {target} tightly! 💞",
    ],
    "pat": [
        "{author} pats {target} on the head! 🐱",
        "{author} gently pats {target}! ✨",
        "{author} gives {target} a reassuring pat! 🥹",
    ],
    "bonk": [
        "{author} bonks {target} on the head! 🔨",
        "{author} gives {target} a mighty bonk! 🛎️",
        "{author} bonks {target} — straight to horny jail! 🚨",
    ],
    "flirt": [
        "{author} flirts with {target}! 😏",
        "{author} winks at {target} seductively! 💋",
        "{author} slides into {target}'s DMs IRL! 🔥",
    ],
    "kill": [
        "{author} kills {target}! 💀",
        "{author} eliminates {target}! ⚔️",
        "{author} murders {target} brutally! 🔪",
    ],
    "bite": [
        "{author} bites {target}! 🦷",
        "{author} chomps down on {target}! 🐊",
        "{author} gives {target} a little nibble! 😬",
    ],
    "boop": [
        "{author} boops {target}'s nose! 👆",
        "{author} gently boops {target}! 🥹",
        "{author} sneaks a boop on {target}! ✨",
    ],
    "pinch": [
        "{author} pinches {target}'s cheek! 🤏",
        "{author} gives {target} a little pinch! 😈",
        "{author} pinches {target} — ouch! 🫣",
    ],
    "flick": [
        "{author} flicks {target}'s forehead! 👋",
        "{author} gives {target} a quick flick! 🤪",
        "{author} flicks {target} — right on the nose! 😛",
    ],
    "tackle": [
        "{author} tackles {target} to the ground! 🏈",
        "{author} leaps and tackles {target}! 💨",
        "{author} full-on tackles {target}! 💥",
    ],
    "throw": [
        "{author} throws {target} across the room! 🌀",
        "{author} yeets {target} into the distance! 🚀",
        "{author} hurls {target} like a frisbee! 🥏",
    ],
    "spit": [
        "{author} spits on {target}! 💦",
        "{author} hocks a loogie at {target}! 🤮",
        "{author} spits in {target}'s general direction! 🧂",
    ],
    "yeet": [
        "{author} YEETS {target} into the void! 🌌",
        "{author} sends {target} flying across the server! 🚀",
        "{author} violently yeets {target} into orbit! 🛸",
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


def action_embed(author: discord.Member, target: discord.Member, action: str):
    msg_template = random.choice(ACTION_MESSAGES[action])
    message = msg_template.format(author=author.mention, target=target.mention)
    gif_url = random.choice(ACTION_GIFS[action])
    color = discord.Color.from_str(COLOR_MAP.get(action, "#FF0000"))
    embed = discord.Embed(description=message, color=color)
    embed.set_image(url=gif_url)
    return embed


# ── Generic action command factory ────────────────────

def make_action_command(name: str):
    @bot.command(name=name)
    async def cmd(ctx, member: discord.Member = None):
        if member is None or member == ctx.author:
            await ctx.send(f"You need to mention someone to {name}!")
            return
        record_use(ctx.author.id, member.id, name)
        embed = action_embed(ctx.author, member, name)
        await ctx.send(embed=embed)
    return cmd

for action in ACTION_GIFS:
    make_action_command(action)


# ── Stats command ─────────────────────────────────────

@bot.command(name="stats")
async def cmd_stats(ctx, member: discord.Member = None):
    """Shows your command usage stats. Use ;stats @user to see stats with that person."""
    author_key = str(ctx.author.id)
    target_key = str(member.id) if member else None

    if member is None:
        # Show all of your stats
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

        # Find top target
        top_target_id = max(target_totals, key=target_totals.get)
        top_target = ctx.guild.get_member(int(top_target_id))
        top_target_name = top_target.display_name if top_target else f"User {top_target_id}"

        # Find top command
        top_cmd = max(command_totals, key=command_totals.get)

        embed = discord.Embed(
            title=f"📊 {ctx.author.display_name}'s Command Stats",
            description=f"**Total commands used:** {total}",
            color=discord.Color.blue()
        )
        embed.add_field(name="🎯 Most targeted", value=top_target_name, inline=True)
        embed.add_field(name="⚡ Favorite command", value=f";{top_cmd}", inline=True)

        # Top 5 targets
        sorted_targets = sorted(target_totals.items(), key=lambda x: -x[1])[:5]
        targets_text = ""
        for t_key, count in sorted_targets:
            t_member = ctx.guild.get_member(int(t_key))
            t_name = t_member.display_name if t_member else f"User {t_key}"
            targets_text += f"• {t_name}: **{count}** times\n"
        if targets_text:
            embed.add_field(name="Top targets", value=targets_text or "None", inline=False)

        await ctx.send(embed=embed)

    else:
        # Stats with a specific person
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
        embed.add_field(name="Command breakdown", value=cmd_list or "None", inline=False)

        await ctx.send(embed=embed)


# ── On ready ──────────────────────────────────────────

@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online and ready!")
    print(f"   Bot ID: {bot.user.id}")
    print(f"   Servers: {len(bot.guilds)}")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=";kiss | ;stats | ;bonk"
    ))


# ── Run ───────────────────────────────────────────────

if __name__ == "__main__":
    import os
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        token = "YOUR_BOT_TOKEN_HERE"
    bot.run(token)