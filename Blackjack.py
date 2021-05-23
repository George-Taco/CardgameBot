import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import random
import asyncio

suits = ["spades", "diamonds", "clubs", "hearts"]
suit_emojis = ["♠", "♦", "♣", "♥"]


# creates a list with all the cards of a standard deck
def create_deck():

    deck = []
    suit_number = 0

    for x in range(4):

        suit_name = suits[suit_number]

        suit_emoji = suit_emojis[suit_number]

        suit_number += 1

        for i in range(13):
            num = i + 1
            if num == 1:
                face = "A"
            elif num == 11:
                face = "J"
                num = 10
            elif num == 12:
                face = "Q"
                num = 10
            elif num == 13:
                face = "K"
                num = 10
            else:
                face = str(num)
            card = {"value": num, "face": face, "suit_name": suit_name, "suit_emoji": suit_emoji}
            deck.append(card)
    return deck


def show_hand(hand, holder="player"):

    if holder == "bot":
        pronoun = "Bot"
    else:
        pronoun = "Your"

    shown_hand = f"**__{pronoun} hand:__**\n"
    hand_val = 0
    has_ace = False
    for card in hand:
        emoji = card.get("suit_emoji")
        face = card.get("face")
        value = card.get("value")
        shown_hand += f"`{emoji} {face}`  "
        if value == 1:
            has_ace = True
        hand_val += value

    if has_ace:
        if hand_val + 10 < 22:
            hand_val += 10

    shown_hand += f"\n\n**__Value:__**\n`{hand_val}`"

    return shown_hand


# returns -1 if user has gone over 21
# if check enabled, check to see if the amount has gone over 21
def give_card(deck, hand, amount=1, check=True):

    hand_value = 0

    if check:

        for card in hand:
            hand_value += card.get("value")

    for i in range(amount):

        card = random.choice(deck)

        hand.append(card)

        deck.remove(card)

        if hand_value + card.get("value") > 21:
            return -1

        hand_value += card.get("value")


# create a class with what ever name you want.
class ClassName(commands.Cog):

    # initialize it
    def __init__(self, client):
        self.client = client

    @commands.command(name="blackjack")
    async def blackjack(self, context):

        deck = create_deck()
        player_hand = []
        bot_hand = []

        # gives the player and the bot each two cards
        give_card(deck, player_hand, 2, False)
        give_card(deck, bot_hand, 2, False)

        bj_desc = show_hand(player_hand) + "\n\n" + show_hand(bot_hand, "bot")

        blackjack_embed = discord.Embed(title=f"Hit or Stand", description=bj_desc, color=discord.Color.blue())
        blackjack_embed.set_author(name=f"{context.author.display_name}'s blackjack game", icon_url=context.author.avatar_url)
        blackjack_embed.set_footer(text="K, Q, J = 10  |  A = 1 or 11")

        await context.send(embed=blackjack_embed)

        def check(m):
            return m.author == context.author and m.channel == context.channel

        msg = await self.client.wait_for('message', check=check)

        # counts as hit
        if msg.content[0] == "h":
            if give_card(deck, player_hand) == -1:
                bj_desc = show_hand(player_hand) + "\n\n" + show_hand(bot_hand, "bot")

                blackjack_embed = discord.Embed(title=f"You lose", description=bj_desc, color=discord.Color.red())
                blackjack_embed.set_author(name=f"{context.author.display_name}'s blackjack game",
                                           icon_url=context.author.avatar_url)
                blackjack_embed.set_footer(text="K, Q, J = 10  |  A = 1 or 11")

            else:
                bj_desc = show_hand(player_hand) + "\n\n" + show_hand(bot_hand, "bot")

                blackjack_embed = discord.Embed(title="You don't lose", description=bj_desc, color=discord.Color.green())
                blackjack_embed.set_author(name=f"{context.author.display_name}'s blackjack game",
                                           icon_url=context.author.avatar_url)
                blackjack_embed.set_footer(text="K, Q, J = 10  |  A = 1 or 11")

            await asyncio.sleep(1)
            await context.send(embed=blackjack_embed)


# set it up
def setup(client):
    client.add_cog(ClassName(client))
