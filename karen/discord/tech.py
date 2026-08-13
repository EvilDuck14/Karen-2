import discord
from discord.ext import commands

from karen.discord.util import *

SUPERIOR_SPIDEY_SERVER_ID = 1354475065055379496

TECHS = {

    "Animation Canceling" : {
        "description" : "Description missing.",
        "youtube link" : "https://youtu.be/d5v0KE42isM?t=415",
        "discord link" : ""
    },

    "Movestack" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Bread & Butter" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Short Plink" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : 1440975851326930964
    },

    "Long Plink" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : 1440975851326930964
    },

    "Double Plink" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Flashstep" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "No Stick" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "FFAmestack" : {
        "description" : "Description missing.",
        "youtube link" : "https://youtu.be/4P51EF-CgnM",
        "discord link" : 1461308080670117971
    },

    "Saporen Tech" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Space Jam" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Saporen FFAmestack" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Unique 3 Hit" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Unique 2 Hit" : {
        "description" : "Description missing.",
        "youtube link" : "https://youtu.be/3ryIdDlHoX4?t=114",
        "discord link" : 1404533477809848441
    },

    "Overhead Preserve" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : 1396816077798768680
    },

    "Reverse Trigger" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "B Hop" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Wall Bounce" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Auto Stop" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Okancel" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : 1450824468535705724
    },

    "N Stop" : {
        "description" : "Description missing.",
        "youtube link" : "https://youtu.be/PJRNJURThRU",
        "discord link" : 1394991814414565468
    },

    "Swing Rebound" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Swing Surfing" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : 1396849601465810944
    },

    "Web Vault" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Infinite Swing" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Jumppercut" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Collision Cancel" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "LowZlam" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "FFAme Glide" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Efoma Flip" : {
        "description" : "Description missing.",
        "youtube link" : "https://youtu.be/4ItPFtUPTTw",
        "discord link" : 1450360149989527583
    },

    "Momentum Pull" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Makatore Pull" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Danny Pull" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Ino Pull" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Ghost Symbiote" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Symbiote Stalling" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Ghost Hop" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Ghost N Stop" : {
        "description" : "Description missing.",
        "youtube link" : "",
        "discord link" : ""
    }
}

TECH_NAMES = {
    "animationcanceling" : "Animation Canceling",
    "animationcancel" : "Animation Canceling",
    "animationcancelling" : "Animation Canceling",
    "animcanceling" : "Animation Canceling",
    "animcancel" : "Animation Canceling",
    "animcancelling" : "Animation Canceling",
    "canceling" : "Animation Canceling",
    "cancel" : "Animation Canceling",
    "cancelling" : "Animation Canceling",

    "movestack" : "Movestack",
    "stack" : "Movestack",

    "breadandbutter" : "Bread & Butter",
    "bread&butter" : "Bread & Butter",
    "breadnbutter" : "Bread & Butter",
    "bandb" : "Bread & Butter",
    "b&b" : "Bread & Butter",
    "bnb" : "Bread & Butter",

    "shortplink" : "Short Plink",
    "fastplink" : "Short Plink",
    "autoplink" : "Short Plink",

    "longplink" : "Long Plink",
    "plink" : "Long Plink",

    "doubleplink" : "Double Plink",
    "doubleswingoverhead" : "Double Plink",
    "dsoverhead" : "Double Plink",
    "dsoh" : "Double Plink",

    "flashstep" : "Flashstep",
    "flash" : "Flashstep",

    "nostick" : "No Stick",

    "ffamestack" : "FFAmestack",
    "ffame" : "FFAmestack",
    "abilitystack" : "FFAmestack",

    "saporentech" : "Saporen Tech",
    "saporen" : "Saporen Tech",
    "sap" : "Saporen Tech",

    "spacejam" : "Space Jam",
    "space" : "Space Jam",
    "jam" : "Space Jam",
    "sj" : "Space Jam",

    "saporenffamestack" : "Saporen FFAmestack",
    "saporenffame" : "Saporen FFAmestack",
    "saporenstack" : "Saporen FFAmestack",
    "sapffamestack" : "Saporen FFAmestack",
    "sapffame" : "Saporen FFAmestack",
    "sapstack" : "Saporen FFAmestack",

    "unique3hit" : "Unique 3 Hit",
    "uniquethreehit" : "Unique 3 Hit",
    "u3h" : "Unique 3 Hit",

    "unique2hit" : "Unique 2 Hit",
    "uniquetwohit" : "Unique 2 Hit",
    "u2h" : "Unique 2 Hit",

    "overheadpreserve" : "Overhead Preserve",
    "overheadslampreserve" : "Overhead Preserve",
    "ohpreserve" : "Overhead Preserve",
    "downslampreserve" : "Overhead Preserve",
    "slampreserve" : "Overhead Preserve",
    "preserve" : "Overhead Preserve",

    "reversetrigger" : "Reverse Trigger",
    "rt" : "Reverse Trigger",
    "backflash" : "Reverse Trigger",

    "bhop" : "B Hop",
    "bunnyhop" : "B Hop",
    "hop" : "B Hop",

    "wallbounce" : "Wall Bounce",
    "bounce" : "Wall Bounce",

    "autostop" : "Auto Stop",
    "autoswingstop" : "Auto Stop",
    "easyswingstop" : "Auto Stop",
    "simpleswingstop" : "Auto Stop",

    "okancel" : "Okancel",
    "ocancel" : "Okancel",
    "okcancel" : "Okancel",

    "nstop" : "N Stop",
    "stop" : "N Stop",
    "instantstop" : "N Stop",

    "swingrebound" : "Swing Rebound",
    "rebound" : "Swing Rebound",

    "swingsurfing" : "Swing Surfing",
    "swingsurf" : "Swing Surfing",
    "surfing" : "Swing Surfing",
    "surf" : "Swing Surfing",

    "webvault" : "Web Vault",
    "swingvault" : "Web Vault",
    "vault" : "Web Vault",

    "infiniteswing" : "Infinite Swing",
    "longswing" : "Infinite Swing",
    "swingstall" : "Infinite Swing",
    "swingstalling" : "Infinite Swing",

    "jumppercut" : "Jumppercut",
    "uppercutjump" : "Jumppercut",
    "upperjump" : "Jumppercut",

    "collisioncancel" : "Collision Cancel",
    "collision" : "Collision Cancel",

    "lowzlam" : "LowZlam",
    "lowslam" : "LowZlam",
    "lowswing" : "LowZlam",
    "zlam" : "LowZlam",
    "slam" : "LowZlam",

    "ffameglide" : "FFAme Glide",
    "glide" : "FFAme Glide",

    "efomaflip" : "Efoma Flip",
    "eflip" : "Efoma Flip",
    "superjump" : "Efoma Flip",

    "momentumpull" : "Momentum Pull",
    "longpull" : "Momentum Pull",
    "tiktokpull" : "Momentum Pull",
    "pull" : "Momentum Pull",

    "makatorepull" : "Makatore Pull",
    "makatore" : "Makatore Pull",

    "dannypull" : "Danny Pull",
    "danny" : "Danny Pull",
    "omnipull" : "Danny Pull",
    "omni" : "Danny Pull",

    "inopull" : "Ino Pull",
    "ino" : "Ino Pull",
    "efomaflippull" : "Ino Pull",
    "eflippull" : "Ino Pull",
    "efomapull" : "Ino Pull",
    "epull" : "Ino Pull",

    "ghostsymbiote" : "Ghost Symbiote",
    "ghost" : "Ghost Symbiote",

    "symbiotestalling" : "Symbiote Stalling",
    "symbiotestall" : "Symbiote Stalling",
    "symbstalling" : "Symbiote Stalling",
    "symbstall" : "Symbiote Stalling",
    "stalling" : "Symbiote Stalling",
    "stall" : "Symbiote Stalling",

    "ghosthop" : "Ghost Hop",
    "symbiotehop" : "Ghost Hop",
    "symbhop" : "Ghost Hop",

    "ghostnstop" : "Ghost N Stop",
    "ghoststop" : "Ghost N Stop",
    "ghostinstantstop" : "Ghost N Stop"
}

async def tech(ctx: commands.Context, *arr: str):
    if devModeMismatch(ctx):
        return

    inputString: str = " ".join(arr)
    print(f"\nreceived command: !tech {inputString}")

    title: str = "Tech"
    message: str = ""
    colour = INFO_COLOUR

    if inputString.lower().replace(" ", "") in TECH_NAMES.keys():
        title = TECH_NAMES[inputString.lower().replace(" ", "")]
        message = TECHS[title]["description"]

        if (TECHS[title]["discord link"] != "") and ((ctx.guild.id == SUPERIOR_SPIDEY_SERVER_ID) or (ctx.guild.id == DEV_SERVER_ID)):
            message += f"\n\n**Showcase thread:**\n<#{TECHS[title]["discord link"]}>"

    else:
        message = f"Unknown tech \"{inputString}\""
        colour = WARNING_COLOUR

    # sending message
    try:
        messageEmbed: discord.Embed = discord.Embed(
            title=title,
            description=message,
            color=colour
        )
        messageEmbed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar)
        await ctx.send(embed=messageEmbed)

        if TECHS[title]["youtube link"] != "":
            await ctx.send(f"\n[**YouTube:**]({TECHS[title]["youtube link"]})")
    except Exception as e:
        print(e)