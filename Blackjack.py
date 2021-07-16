import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import random
import asyncio

suits = ["spades", "diamonds", "clubs", "hearts"]
suit_emojis = ["♠", "♦", "♣", "♥"]


# returns a list with all the cards of a standard deck, each of which are a dictionary
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


# returns the hand, formatted for the blackjack embed
# if first=True, if the player's hand == 21 then automatically switch to 11 (since you can't win in the first round)
def show_hand(hand, holder="player", first=False, show_bot=False):

    if holder == "bot":
        pronoun = "Bot"

    else:
        pronoun = "Your"

    shown_hand = f"**__{pronoun} hand:__**\n"
    hand_val = 0
    has_ace = False
    x = 0
    for card in hand:
        emoji = card.get("suit_emoji")
        face = card.get("face")
        value = card.get("value")

        if holder == "bot" and x > 0 and not show_bot:
            emoji = ""
            face = "?"

        shown_hand += f"`{emoji} {face}`  "
        if value == 1:
            has_ace = True
        hand_val += value

        x += 1

    if has_ace:
        if hand_val + 10 < 22:
            hand_val += 10

    if first and hand_val == 21:

        hand_val = 11

    if holder == "bot" and not show_bot:
        hand_val = "?"

    shown_hand += f"\n\n**__Value:__**\n`{hand_val}`"

    return shown_hand


# returns -1 if user has gone over 21
# returns 1 if hand == 21
# if check enabled, check to see if the amount has gone over 21
def give_card(deck, hand, amount=1, check=True, player=True):

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
        global has_ace
        has_ace = False

        if card.get("value") == 1:
            has_ace = True

        hand_value += card.get("value")

        if hand_value == 21 and player:
            return 1

    if has_ace and hand_value <= 10:
        hand_value += 10


# returns the total value of a hand
def get_hand_val(hand):

    hand_value = 0

    for card in hand:
        card_value = card.get("value")
        hand_value += card_value
        if hand_value > 21:
            return -1

        if card_value == 1:
            global has_ace
            has_ace = True

    if has_ace == True and hand_value <= 11:
        hand_value += 10
    return hand_value


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
        give_card(deck, player_hand, 2, True)
        give_card(deck, bot_hand, 2, True)

        bj_desc = show_hand(player_hand, first=True) + "\n\n" + show_hand(bot_hand, "bot", first=True)

        blackjack_embed = discord.Embed(title=f"Hit or Stand", description=bj_desc, color=discord.Color.blue())
        blackjack_embed.set_author(name=f"{context.author.display_name}'s blackjack game", icon_url=context.author.avatar_url)
        blackjack_embed.set_footer(text="K, Q, J = 10  -  A = 1 or 11")

        await context.send(content="Type `h` to **hit** or `s` to **stand**.", embed=blackjack_embed)

        async def prompt():

            def check(m):
                return m.author == context.author and m.channel == context.channel

            # gets response
            msg = await self.client.wait_for('message', check=check, timeout=30)

            # counts as hit
            if str(msg.content[0]).lower() == "h":

                # creates a global variable "stand" that tells whether the bot has stood or not
                global stand
                stand = False

                # give the player a card and store the value of the return of function
                give_card_val = give_card(deck, player_hand)

                # loss
                if give_card_val == -1:
                    bj_desc = show_hand(player_hand) + "\n\n" + show_hand(bot_hand, "bot", show_bot=True)
                    blackjack_embed = discord.Embed(title=f"You lose", description=bj_desc, color=discord.Color.red())
                    blackjack_embed.set_author(name=f"{context.author.display_name}'s blackjack game",
                                               icon_url=context.author.avatar_url)
                    blackjack_embed.set_footer(text="K, Q, J = 10  -  A = 1 or 11")
                    await context.send(embed=blackjack_embed)
                # win
                elif give_card_val == 1:
                    bj_desc = show_hand(player_hand) + "\n\n" + show_hand(bot_hand, "bot", show_bot=True)
                    blackjack_embed = discord.Embed(title="You Win", description=bj_desc, color=discord.Color.green())
                    blackjack_embed.set_author(name=f"{context.author.display_name}'s blackjack game",
                                               icon_url=context.author.avatar_url)
                    blackjack_embed.set_footer(text="K, Q, J = 10  -  A = 1 or 11")
                    await context.send(embed=blackjack_embed)
                else:
                    bj_desc = show_hand(player_hand) + "\n\n" + show_hand(bot_hand, "bot")
                    blackjack_embed = discord.Embed(title="Hit or Stand", description=bj_desc, color=discord.Color.blue())
                    blackjack_embed.set_author(name=f"{context.author.display_name}'s blackjack game",
                                               icon_url=context.author.avatar_url)
                    blackjack_embed.set_footer(text="K, Q, J = 10  -  A = 1 or 11")
                    content = "Type `h` to **hit** or `s` to **stand**."
                    await context.send(content=content, embed=blackjack_embed)
                    await prompt()
            # if response is not a hit
            else:
                global bot_stand
                bot_stand = False
                # bot ai
                # if bot has not stood:
                while not bot_stand:

                    # if the bot has 11 or less, and therefore can't lose by being getting hit, then hit
                    if get_hand_val(bot_hand) < 12:
                        give_card(deck, bot_hand, player=False)

                    # elif the bot has more than 11 but less than 17, then have a random chance of getting hit
                    elif get_hand_val(bot_hand) < 17:
                        rand = random.randint(1, get_hand_val(bot_hand))
                        if rand < 9:
                            give_card(deck, bot_hand, player=False)
                            bot_stand = True
                    # if the bot hand is more than 17 then automatically stand
                    else:
                        bot_stand = True

                if str(msg.content[0]).lower() != "s":
                    await context.reply("You have responded with an invalid response. As a result, you have automatically stood")

                user_total = get_hand_val(player_hand)
                bot_total = get_hand_val(bot_hand)

                # user wins
                if user_total > bot_total or bot_total > 21:
                    bj_desc_three = show_hand(player_hand) + "\n\n" + show_hand(bot_hand, "bot", show_bot=True)
                    blackjack_embed = discord.Embed(title="You Win", description=bj_desc_three, color=discord.Color.green())
                    blackjack_embed.set_author(name=f"{context.author.display_name}'s blackjack game",
                                               icon_url=context.author.avatar_url)
                    blackjack_embed.set_footer(text="K, Q, J = 10  -  A = 1 or 11")
                    await context.send(embed=blackjack_embed)
                elif user_total < bot_total:
                    # loss
                    bj_desc = show_hand(player_hand) + "\n\n" + show_hand(bot_hand, "bot", show_bot=True)
                    blackjack_embed = discord.Embed(title=f"You lose", description=bj_desc, color=discord.Color.red())
                    blackjack_embed.set_author(name=f"{context.author.display_name}'s blackjack game",
                                               icon_url=context.author.avatar_url)
                    blackjack_embed.set_footer(text="K, Q, J = 10  -  A = 1 or 11")
                    await context.send(embed=blackjack_embed)
                else:
                    # tied
                    bj_desc = show_hand(player_hand) + "\n\n" + show_hand(bot_hand, "bot", show_bot=True)
                    blackjack_embed = discord.Embed(title=f"You Tied", description=bj_desc, color=discord.Color.dark_gold())
                    blackjack_embed.set_author(name=f"{context.author.display_name}'s blackjack game",
                                               icon_url=context.author.avatar_url)
                    blackjack_embed.set_footer(text="K, Q, J = 10  -  A = 1 or 11")
                    await context.send(embed=blackjack_embed)
        await prompt()


# set it up
def setup(client):
    client.add_cog(ClassName(client))
