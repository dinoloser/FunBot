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
