import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

TARGET_POKEMON_NAME = "水躍魚 (Mudkip)"

@bot.event
async def on_ready():
    print(f"已成功登入為 {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"已同步 {len(synced)} 個斜線指令")
    except Exception as e:
        print(f"同步指令失敗：{e}")

@bot.tree.command(name="report_mudkip", description="回報野生水躍魚出沒地點")
@app_commands.describe(
    location="地點名稱或地標（例如：大安森林公園捷運站2號出口）",
    coordinates="經緯度座標（選填，例如：25.0330, 121.5430）",
    iv="已知的 IV 數值（選填）"
)
async def report_mudkip(
    interaction: discord.Interaction, 
    location: str, 
    coordinates: str = "未提供", 
    iv: str = "未知"
):
    embed = discord.Embed(
        title=f"💧 發現野生 {TARGET_POKEMON_NAME}！",
        color=discord.Color.blue()
    )
    embed.add_field(name="📍 出沒地點", value=location, inline=False)
    embed.add_field(name="🧭 座標", value=coordinates, inline=True)
    embed.add_field(name="📊 IV 資訊", value=iv, inline=True)
    embed.set_footer(text=f"回報者：{interaction.user.display_name}")

    if "," in coordinates:
        clean_coords = coordinates.replace(" ", "")
        map_url = f"https://www.google.com/maps/search/?api=1&query={clean_coords}"
        embed.add_field(name="🗺️ 地圖導航", value=f"[點此開啟 Google 地圖]({map_url})", inline=False)

    await interaction.response.send_message(embed=embed)

if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("找不到 DISCORD_TOKEN，請確認 .env 檔案是否設定正確！")
    bot.run(TOKEN)