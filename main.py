import discord
from discord.ext import commands
import os

# 봇 기본 설정
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 봇이 켜졌을 때
@bot.event
async def on_ready():
    print(f"{bot.user} 접속 완료!")
    await bot.change_presence(
        activity=discord.Game(name="서버 관리 중")
    )

# 신입 입장 알림
@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel

    if channel:
        await channel.send(
            f"🎉 {member.mention}님, 환영합니다!\n"
            f"우리 서버에서 즐거운 시간 보내세요 ♡"
        )

# 멤버 퇴장 알림
@bot.event
async def on_member_remove(member):
    channel = member.guild.system_channel

    if channel:
        await channel.send(
            f"👋 {member.display_name}님이 서버를 떠났습니다."
        )

# 도움말
@bot.command(name="도움말")
async def help_command(ctx):
    await ctx.send(
        "📌 **봇 명령어 안내**\n"
        "!도움말 - 명령어 확인\n"
        "!공지 내용 - 공지 보내기 (관리자)\n"
        "!청소 숫자 - 메시지 삭제 (관리자)\n"
        "!추방 @유저 - 멤버 추방 (관리자)\n"
        "!차단 @유저 - 멤버 차단 (관리자)"
    )

# 관리자 전용 공지
@bot.command()
@commands.has_permissions(administrator=True)
async def 공지(ctx, *, 내용):
    await ctx.send(
        f"📢 **서버 공지사항**\n\n{내용}"
    )

# 관리자 전용 메시지 청소
@bot.command()
@commands.has_permissions(administrator=True)
async def 청소(ctx, 개수: int):
    if 개수 < 1 or 개수 > 100:
        await ctx.send("1~100 사이의 숫자를 입력해 주세요.")
        return

    await ctx.channel.purge(limit=개수 + 1)
    await ctx.send("🧹 메시지를 정리했습니다.", delete_after=3)

# 관리자 전용 추방
@bot.command()
@commands.has_permissions(administrator=True)
async def 추방(ctx, member: discord.Member, *, 사유="사유 없음"):
    await member.kick(reason=사유)
    await ctx.send(f"🔨 {member.display_name}님을 추방했습니다.")

# 관리자 전용 차단
@bot.command()
@commands.has_permissions(administrator=True)
async def 차단(ctx, member: discord.Member, *, 사유="사유 없음"):
    await member.ban(reason=사유)
    await ctx.send(f"⛔ {member.display_name}님을 차단했습니다.")

# 특정 단어 자동 답장
자동답장 = {
    "안녕": "안녕하세요! 반가워요 ♡",
    "ㅎㅇ": "어서 와요! 반가워요!",
    "잘자": "좋은 꿈 꾸세요 🌙",
    "고마워": "별말씀을요! ♡",
    "봇아": "네! 부르셨나요?",
    "초월봇아": "네,주인님 호출하셨나요? 무엇을 도와드릴까요?",
    "심심해": "그럼 우리 서버에서 같이 놀아요! 🎮",
    "ㅋㅋ": "ㅋㅋㅋㅋ 무슨 일이에요?"
}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # 자동 답장
    if not message.content.startswith("!"):
        for 단어, 답장 in 자동답장.items():
            if 단어 in message.content:
                await message.reply(답장)
                break

    await bot.process_commands(message)

# 관리자 권한 오류 안내
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("⛔ 관리자만 사용할 수 있는 명령어입니다.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ 명령어 뒤에 필요한 내용을 입력해 주세요.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("⚠️ 해당 멤버를 찾을 수 없습니다.")

# 봇 실행
bot.run(os.environ["DISCORD_TOKEN"])
