import discord
from discord.ext import commands

from karen.discord.util import *

SUPERIOR_SPIDEY_SERVER_ID = 1354475065055379496

TECHS = {

    "Animation Canceling" : {
        "description" : "Some animations cancel other early, meaning that a combo can be made faster or slower by the ordering of inputs depending on the alignment of animation cancels.\n\nFor instance, `uppercut > tracer` is slow, since tracers don't cancel the uppercut animation. However, swings do cancel the uppercut animation and tracers cancel the swing animation, so `uppercut > swing whiff > tracer` is significantly faster. ",
        "youtube link" : "https://youtu.be/d5v0KE42isM?t=415",
        "discord link" : ""
    },

    "Movestack" : {
        "description" : "When the behaviours/animations of multiple inputs overlap, this is called a movestack. Movestacks allow for damage to be dealt more quickly than usual, but are generally more difficult and/or expensive.\n\nFor example, the FFAmestack overlaps the get over here (targetting) and uppercut animations.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Bread & Butter" : {
        "description" : "A very beginner friendly sequence for starting combos or confirming kills on damaged targets. Spidey's kit is naturally designed to incentivise this sequence, using a tracer to tag the opponent enables a lock-on attack in the form of goht, then uppercut capitalises on the closed distance with its large hit box, ripping the tracer tag for increased damage.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Short Plink" : {
        "description" : "Usually used as a very fast follow up to an uppercut, the short plink is an autoswing followed by an overhead slam. This is the fastest way to get an overhead in most situations, but comes at the cost of a swing.",
        "youtube link" : "",
        "discord link" : 1440975851326930964
    },

    "Long Plink" : {
        "description" : "A long plink is a manual swing instantly canceled into a tracer, followed by an overhead slam. This is common way to extend combos for minimal resource investment, especially after an uppercut. While it's slower than a short plink, it doessn't consume a swing, and it does much more damage if the opponent isn't yet tagged by a tracer.",
        "youtube link" : "",
        "discord link" : 1440975851326930964
    },

    "Double Plink" : {
        "description" : "A double plink, or double swing overhead, is a swing whiff immediately canceled by a tracer, which is canceled into an autoswing, and finally an overhead slam.\n\nThis is a compromise between the short and long plinks - it deals more damage to untagged targets than a short plink, and is only slightly slower. It's much faster than a long plink, but costs a swing.",
        "youtube link" : "https://youtu.be/C3i2FLHeN9w",
        "discord link" : ""
    },

    "Flashstep" : {
        "description" : "A flashstep involves briefly holding down the autoswing button in order to quickly move behind your target mid-combo. This makes the user incredibly difficult to track, which is useful for dodging cc abilities.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Hydro Bounce" : {
        "description" : "Double jumps can be used without slowing down a combo, and using an autoswing immediately refunds Spidey's double jump if it successfully attaches to a wall.\n\nThis allows Spidey to use two double jumps during a Double Plink in order to evade attacks and cc abilities used by his target.",
        "youtube link" : "https://youtu.be/wlSKRDP0_lM",
        "discord link" : ""
    },

    "Jumppercut" : {
        "description" : "Spidey is able to gain extra height while uppercutting by jumping during the uppercut animation. By positioning himself above the enemy as they get knocked upwards, their momentum can be redirected to the side. This can serve as an additional displacement tool in Spidey's kit.",
        "youtube link" : "",
        "discord link" : 1475963630167134369
    },

    "No Stick" : {
        "description" : "If autoswing is used when there isn't a valid sticking point for the swing visible on screen (within 30m and at least 5m above eye level), or if there is a ceiling less than 5 meters above Spidey's head, then no swing will be used, but the animation canceling properties and overhead reward of an autoswing are still given. This allows Spidey all of the benefits of using autoswings without the downside of consuming swing charges.",
        "youtube link" : "",
        "discord link" : ""
    },

    "FFAmestack" : {
        "description" : "By inputting get over here (targetting) and then uppercut in very quick succession, Spidey can movestack the abilities. This can also be achieved by binding these abilities to the same button (the second bind for these abilities is useful for this).\n\nNote that the uppercut damage registers fairly early in the animation, so using a FFAmestack at ranges much larger than 4m will cause the uppercut damage to miss.",
        "youtube link" : "https://youtu.be/4P51EF-CgnM",
        "discord link" : 1461308080670117971
    },

    "Saporen Tech" : {
        "description" : "By inputting get over here (targetting) as or just before a melee hit lands on a tagged target, the ability will still register even as the tag is removed.",
        "youtube link" : "",
        "discord link" : 1480594802000007229
    },

    "Space Jam" : {
        "description" : "A Space Jam is essentially a Saporen Tech modified to work with an uppercut. By using an uppercut and performing a very tight swing cancel, there is a window where get over here targetting can register before the tracer tag is ripped by the uppercut. This is much more difficult than a regular Saporen Tech.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Saporen FFAmestack" : {
        "description" : "A Saporen Tech can be chained into a FFAmestack. This sequence alone is almost enough damage to kill squishy targets.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Unique 3 Hit" : {
        "description" : "Aiming a swing at the sky or at a surface more than 30 meters away will cause it not to connect, delaying the overhead reward for long enough to use one punch and start another. When the overhead award registers, the second punch continues underneath the overhead slam animation, causing a movestack.\n\nThis sequence of 3 hits, punch > hidden punch > overhead slam, is referred to as the \"Unique 3 Hit Combo\".",
        "youtube link" : "https://youtu.be/3DqsAIYhlBc?t=374",
        "discord link" : ""
    },

    "Unique 2 Hit" : {
        "description" : "When a punch starts and an overhead slam is immediately awarded, the punch continues underneath the overhead slam animation, causing two distinct hits. This is similar to the Unique 3 Hit, but the overhead award comes much sooner.\n\nIt isn't fully understood why U2H occurs, since it tends to happen when there shouldn't be a possible window for the punch to start before the overhead is awarded. This means that it is likely caused by a quirk in the game's netcode.\n\nThere is an ongoing bounty for this tech - anyone who makes significant progress in the understanding of U2H is eligable to win a skin from Evil Duck.",
        "youtube link" : "https://youtu.be/3ryIdDlHoX4?t=114",
        "discord link" : 1404533477809848441
    },

    "Overhead Preserve" : {
        "description" : "Due to the ordering of overhead reward calculations, overhead availability can be preserved through actions that would usually take them away, such as get over here (targeting), by ensuring that the swing is still in use as the other ability is used.",
        "youtube link" : "https://youtu.be/wFTJpgDGexs",
        "discord link" : 1396816077798768680
    },

    "Reverse Trigger" : {
        "description" : "By canceling a melee attack very early with a tracer, it is sometimes possible for the tracer to register its damage before the melee attack lands, causing the tracer to be ripped by the melee attack that came before it. This is highly inconsistent.",
        "youtube link" : "",
        "discord link" : 1448989484929650719
    },

    "B Hop" : {
        "description" : "When Spidey falls far enough, he enters a falling animation which triggers a rolling animation when he lands. This animation is slow, and causes Spidey to lose all momentum.\n\nThe falling/rolling animations can be canceled with tracers or any cooldown, which frees Spidey to be able to input a jump immediately upon landing to carry momentum.\n\nLikewise, when using a low web zip, the animation can be canceled with a tracer or any cooldown (except for a swing) to cancel the zip/rolling animations and free Spidey to perform hops.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Wall Bounce" : {
        "description" : "Using a web swing while pressed against a wall causes Spidey to be flung away from the wall, often at an unpredictable angle.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Auto Stop" : {
        "description" : "Spidey's momentum can be cancelled by briefly holding autoswing, although this requires autoswing to be able to find an anchor point, and consumes a swing cooldown if successful. For these reasons, N Stop is generally superior for canceling momentum.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Okancel" : {
        "description" : "Spidey can carry airborne momentum further by quickly chaining a double jump and a 1 frame autoswing (most easily performed by binding autoswing to the scroll wheel). This requires the autoswing to connect, and uses a swing cooldown, so it is generally inferior to Ghost Hopping.",
        "youtube link" : "",
        "discord link" : 1450824468535705724
    },

    "N Stop" : {
        "description" : "Spidey's momentum can be cancelled by using a double jump immediately followed by an uppercut, symbiote, or ult. The timing for this is very tight, but can be performed consistently.",
        "youtube link" : "https://youtu.be/PJRNJURThRU",
        "discord link" : 1394991814414565468
    },

    "Swing Rebound" : {
        "description" : "Hitting a wall at certain angles while swinging allows Spidey to rebound off of the wall for a quick direction change. This can be used for more efficient pathing or to re-engage with the same swing that was used to disengage.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Swing Surfing" : {
        "description" : "By hitting a wall mid-swing with the correct speed, Spidey can coast or \"surf\" along the wall while continuing to swing, increasing his options for swing pathing.",
        "youtube link" : "",
        "discord link" : 1396849601465810944
    },

    "Web Vault" : {
        "description" : "By aiming a swing at the top of a wall and continuing to look at it throughout the swing, Spidey will vault over the wall. Knowing this is useful for efficiently pathing to to top of a ledge when more conventional swing attach points aren't obvious.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Infinite Swing" : {
        "description" : "By keeping momentum within a certain range and turning to keep moving perpendicular to the swing attach point, Spidey can continue a swing indefinitely. This can be used to dodge fire while stalling a point, but can be very difficult to sustain for a long time.",
        "youtube link" : "https://youtube.com/shorts/k4-wZSWtZTU",
        "discord link" : ""
    },

    "Collision Cancel" : {
        "description" : "A low swing zip is canceled immediately if Spidey collides with a wall, which allows a quick way to engage with an overhead slam.",
        "youtube link" : "",
        "discord link" : ""
    },

    "LowZlam" : {
        "description" : "A LowZlam is when Spidey engages a target with a low, fast swing, charging up an overhead as he approaches. With good timing, this is a very strong way to engage, as it keeps get over here available for later use, and the long windup of the overhead slam is performed while Spidey hasn't even arrived yet, offsetting the overhead's greatest weakness.",
        "youtube link" : "",
        "discord link" : ""
    },

    "FFAme Glide" : {
        "description" : "A FFAme Glide involves using a low web zip while standing on the ground, then canceling it with an uppercut and immediately holding jump. Since the jump registers through the uppercut animation, this is functionally a B Hop with the lift of an uppercut. This can be useful for setting up Momentum Pulls.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Efoma Flip" : {
        "description" : "An Efoma Flip (or Super Jump) allows Spidey to rapidly fling himself in a controlled direction (often backwards). It is most consistent on low frame rates, but has been demonstrated to be able to be performed consistenltly on high frame rates with good technique.\n\nAn E Flip is performed by looking at the ground at a roughly 45 degree angle, holding a directional movement input, using a web zip, and as soon as the web connects to the floor, cancelling it with a tracer and immediately double jumping (ideally with the scroll wheel).",
        "youtube link" : "https://youtu.be/4ItPFtUPTTw",
        "discord link" : 1450360149989527583
    },

    "Momentum Pull" : {
        "description" : "By building momentum before landing get over here on a target, Spidey can pull opponents up to 50 meters - much further than is usually possible. This also allows targets to be pulled much further over pits than can be achieved by a standing pull, so that characters with small amounts of mobility still can't recover.\n\nThere are many variations and setups, but the most common setup for a Momentum Pull is a low swing zip cancelled by a tracer, followed by a double jump and immediate uppercut. Then the uppercut can be cancelled with a swing whiff quickly weaved into get over here.",
        "youtube link" : "https://youtu.be/JR64N7ZQAPM",
        "discord link" : ""
    },

    "Makatore Pull" : {
        "description" : "By using get over here and zipping away from the target right as they begin to get displaced, Spidey can pull targets further than the usual pull distance without having to build momentum beforehand.",
        "youtube link" : "https://youtube.com/shorts/f8ppzRDci94",
        "discord link" : ""
    },

    "Danny Pull" : {
        "description" : "While Spidey is using a low web zip, he is able to pass through enemies without colliding with their hitboxes. A Dani Pull (or Omni Pull) leverages this fact to pull targets in any direction.\n\nFirst, you zip right beside the target, then uppercut, zip through them in the desired direction of the pull, use get over here before landing, and B Hop to carry the momentum.",
        "youtube link" : "https://youtube.com/shorts/lcJSsHgnVRw",
        "discord link" : ""
    },

    "Ino Pull" : {
        "description" : "An Ino Pull is a Momentum Pull which is set up by using an Efoma Flip to gain momentum.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Ghost Symbiote" : {
        "description" : "If symbiote is cancelled immediately with a swing, the cooldown won't be used, but it will still refund the user's double jump. This enables Ghost Hopping.",
        "youtube link" : "",
        "discord link" : ""
    },

    "Ghost Hop" : {
        "description" : "By chaining double jumps and Ghost Symbiotes, Spidey can stay airborne indefinitely without using any cooldowns. This can be used to to stall in place, or to carry airborne momentum.",
        "youtube link" : "https://youtube.com/shorts/PCa3bsZXoUk",
        "discord link" : ""
    },

    "Ghost N Stop" : {
        "description" : "An N Stop can be performed with a Ghost Symbiote, allowing for an instant momentum cancel that doesn't consume any cooldowns.",
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

    "hydrobounce" : "Hydro Bounce",
    "hydro" : "Hydro Bounce",
    "airbounce" : "Hydro Bounce",
    "bounce" : "Hydro Bounce",

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

    "autostop" : "Auto Stop",
    "autoswingstop" : "Auto Stop",
    "easyswingstop" : "Auto Stop",
    "simpleswingstop" : "Auto Stop",

    "okancel" : "Okancel",
    "ocancel" : "Okancel",
    "okcancel" : "Okancel",
    "ok" : "Okancel",

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

    "symbiotestalling" : "Ghost Hop",
    "symbiotestall" : "Ghost Hop",
    "symbstalling" : "Ghost Hop",
    "symbstall" : "Ghost Hop",
    "stalling" : "Ghost Hop",
    "stall" : "Ghost Hop",
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