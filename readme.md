# Karen 2.0.0

> *"Congratulations on completing the rigorous Training Wheels Protocol and gaining access to your suit’s full capabilities... Would you like me to engage Enhanced Combat Mode?"* - Karen

Karen is named after Spider-Man's virtual assistant in *Spider-Man: Homecoming*, who advised Peter in strategy and combat. This tool is designed to quickly, easily, and accurately analyse Spider-Man's combos in Marvel Rivals. 

Karen is designed to be used as a Discord bot to aid with labbing and communication of combos / ideas. This means that users don't have to concern themselves with installing anything - just join a [Discord server with the bot](https://discord.gg/5bFRxaCzCS), or add Karen to your own server using the [invite link](#install-local-discord).



## <br> Table of Contents

### [Installation](#install)
- [Adding to Discord](#install-discord)
- [Data Sharing](#install-data)

### [Commands](#commands)
- [Evaluate](#commands-eval)
- [Compare](#commands-comp)
- [Tech](#commands-tech)
- [List](#commands-list)
- [Unsend](#commands-unsend)
- [Preferences](#commands-prefs)
- [Help](#commands-help)

### [Combo Comprehension](#comprehension)
- [Individual Actions](#comprehension-actions)
- [Named Sequences](#comprehension-sequences)
- [Movestacks](#comprehension-movestacks)
- [Mixed Inputs / Grammar](#comprehension-mixed)
- [Comments](#comprehension-comments)
- [Wait](#comprehension-wait)
- [Autocorrection](#comprehension-autocorrection)
    <!-- 
    - [Swing Correction](#comprehension-autocorrection-swing)
    - [Movestack Detection](#comprehension-autocorrection-movestack) 
    -->

### [Parameters](#params)
- [Outputs](#params-outputs)
    <!-- 
    - [Time](#params-outputs-t)
    - [Time From Damage](#params-outputs-tfd)
    - [Damage](#params-outputs-d)
    - [Raw DPS](#params-outputs-rdps)
    - [DPS](#params-outputs-dps)
    - [Ult Charge](#params-outputs-uc)
    - [No Warnings](#params-outputs-n) 
    -->
- [Damage Boost](#params-boost)
- [Healing Per Second](#params-hps)
- [Season](#params-season)

### [Warnings](#warn)
- [Improper Formatting](#warn-format)
- [Impossible GOHT](#warn-goht)
- [Impossible Kick](#warn-kick)
- [Downtime Awaiting Cooldowns](#warn-downtime)

### [License](#license)



<a id="install"></a>
## <br> Installation

If you're already in a Discord server which has Karen added, there's no need to install anything - you can start using commands in the designated channels right away! Jump to the [section on usage](#usage) for a detailed explanation of how to use these commands to their fullest potential.

<a id="install-discord"></a>
### Adding to Discord

If you want to add Karen to your Discord server, you can do it using [this link](<!-- to do -->). Karen requests minimal premissions to function, but it does need to be able to read and send messages to function.

<a id="install-data"></a>
### Data Sharing

By default, Karen collects data to help understand how it is being used. This includes a count of how many servers are running the bot, how often it is used on each server, and a tally of how many times each combo has been calculated. Karen **does not** read messages in your server besides commands (but as a PSA, Discord is fundamentally a public platform, and you should never consider your messages in any server to be truly private).

When Karen is added to a server, the server owner will receive a message with the option between sharing data anonymously (which may be preferred by small servers) or to associate their server name with their data.



<a id="commands"></a>
## <br> Commands

All commands are accessed using a `!` followed by the name of the command and any associated arguments. For example, one might run the command `!eval tracer > overhead > tracer > uppercut` which would, as expected, give information on the combo provided. For more information on how to write a combo that Karen will understand, see the section on [combo comprehension](#comprehension).

<a id="commands-eval"></a>
### Evaluate

<a id="commands-comp"></a>
### Compare

<a id="commands-tech"></a>
### Tech

<a id="commands-list"></a>
### List

The `!list` command causes Karen to output a list of all named combos.

<a id="commands-unsend"></a>
### Unsend

The `!unsend` command allows a user to cause Karen to unsend their previous output. A user cannot unsend the output of another user's command.

<a id="commands-prefs"></a>
### Preferences

The `!prefs` command allows a user to set a default list of [parameters](#params) to execute with each command. For example, if a user runs `!prefs -n`, then every time they run a command with no parameters specified, the "no warnings" parameter will be automatically added. 

If any parameters are explicitly given to a command, the user's preferences are ignored. This means that a user can access the command's default behaviour by using an empty parameter (eg. `!eval t -`).

<a id="commands-help"></a>
### Help

The `!help` command will give a list of all recognised commands and link to this documentation. More information can be found on any command via `!help [command]`.



<a id="comprehension"></a>
## <br> Combo Comprehension

To make Karen as intuitive and efficient to use as possible, many ways of describing the same combo are supported. There are three broad categories of notation:
- Long-form: `tracer > get over here targetting > uppercut`
- Short-form: `tgu`
- Named sequences: `bread and butter`

A user can mix and match notations, and Karen will do its best to interpret what is meant. Regardless of the user's chosen notation, Karen will always output the full long-form sequence with its output so that the user can verify that their input was understood correctly.



<a id="params"></a>
## <br> Parameters

Each command supports the addition of parameters which allow the user to adjust the format/information presented in the output of the command. A user can save a default set of parameters using the [prefs](#commands-prefs) command.



<a id="warn"></a>
## <br> Warnings

When Karen is unable to parse a command, or unconfident that it has understood the intention of the user, it will output a warning alongside its regular output. These warnings are fairly self-explanatory, but have been documented here for the sake of completeness.



<a id="liscense"></a>
## <br> Liscense
`Karen` is distributed under the terms of the [MIT license](https://spdx.org/licenses/MIT.html).