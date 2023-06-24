import disnake
from disnake.ext import commands
import json

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sanctions_data = {}
        self.load_sanctions()

        def load_sanctions(self):
            try:
                with open("sanctions.json", "r") as file:
                    self.sanctions_data = json.load(file)
            except FileNotFoundError:
                self.sanctions_data = {}
        
        def save_sanctions(self):
            with open("sanctions.json", "w") as file:
                json.dump(self.sanctions_data, file)
        

        @commands.slash_command(name="ban", description="Ban un membre du serveur.")
        @commands.has_permissions(ban_members=True)
        async def ban(self, ctx, member: commands.MemberConverter, *, reason=None):
            """Bannit un membre"""
            if reason is None:
                reason = "Aucune raison spécifiée."

            self.sanctions_data[member.id] = {
                "ban": True,
                "reason": reason
            }
            self.save_sanctions()
            
            await member.ban(reason=reason)
            embed = disnake.Embed(
                title=f"{member.mention}, viens d'etre ban",
                description=f"Bannie pour {reason}.",
                color=disnake.Color.green()
            )
            await ctx.send(embed=embed)

        @commands.slash_command(name="warn", description="Warn un membre du serveur.")
        @commands.has_permissions(kick_members=True)
        async def warn(self, ctx, member: commands.MemberConverter, *, reason=None):
            """Warn un membre"""
            if reason is None:
                reason = "Aucune raison spécifiée."

            if member.id not in self.sanctions_data:
                self.sanctions_data[member.id] = {
                    "type": "warn",
                    "reasons": [reason]
                }
            else:
                self.sanctions_data[member.id]["reasons"].append(reason)
            self.save_sanctions()

            embed = disnake.Embed(
                title=f"{member.mention}, viens d'etre warn",
                description=f"Warn pour {reason}.",
                color=disnake.Color.green()
            )
            await ctx.send(embed=embed)
            

def setup(bot):
    bot.add_cog(Moderation(bot))