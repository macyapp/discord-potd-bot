import os
import discord
import requests

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

    # GeeksforGeeks Daily
    gfg_data = requests.get(
        "https://practiceapi.geeksforgeeks.org/api/vr/problems-of-day/problem/today/",
        headers={"User-Agent": "Mozilla/5.0"}
    ).json()

    gfg_title = gfg_data['problem_name']
    gfg_link = gfg_data['problem_url']
    gfg_difficulty = gfg_data['difficulty']
    gfg_tags = ', '.join(gfg_data['tags']['topic_tags'])

    # LeetCode Daily
    lc_query = {
        "query": """
        query questionOfToday {
            activeDailyCodingChallengeQuestion {
                date
                link
                question {
                    title
                    titleSlug
                    difficulty
                    topicTags {
                        name
                    }
                }
            }
        }
        """
    }

    lc_data = requests.post(
        "https://leetcode.com/graphql",
        json=lc_query,
        headers={
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com/problemset/all/",
            "User-Agent": "Mozilla/5.0"
        }
    ).json()['data']['activeDailyCodingChallengeQuestion']

    lc_title = lc_data["question"]["title"]
    lc_link = "https://leetcode.com" + lc_data["link"]
    lc_difficulty = lc_data["question"]["difficulty"]
    lc_tags = ', '.join(tag["name"] for tag in lc_data["question"]["topicTags"])

    # Send Message
    message = f"""🔥📚 **Daily Coding Challenge** 🔍🚀

🟢 **GeeksforGeeks**
📝 Title: {gfg_title}
🔗 Link: {gfg_link}
📈 Difficulty: {gfg_difficulty}
🏷️ Tags: {gfg_tags}

🟡 **LeetCode**
📝 Title: {lc_title}
🔗 Link: {lc_link}
📈 Difficulty: {lc_difficulty}
🏷️ Tags: {lc_tags}
"""

    channel = client.get_channel(CHANNEL_ID)
    await channel.send(message)
    await client.close()

client.run(DISCORD_TOKEN)
