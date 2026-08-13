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
- [Tech](#commands-tech)
- [List](#commands-list)
- [Preferences](#commands-prefs)
- [Help](#commands-help)

### [Combo Comprehension](#comprehension)
- [Individual Actions](#comprehension-actions)
- [Movestacks](#comprehension-movestacks)
- [Named Sequences](#comprehension-sequences)
- [Mixed Inputs / Grammar](#comprehension-mixed)
- [Comments](#comprehension-comments)
- [Wait](#comprehension-wait)
- [Autocorrection](#comprehension-autocorrection)

### [Parameters](#params)
- [Advanced Mode](#params-a) 
- [Show Breakdown](#params-b) 
- [No Warnings](#params-n) 
- [Display Time](#params-t)
- [Display Time From Damage](#params-tfd)
- [Display Damage](#params-d)
- [Display DPS](#params-dps)
- [Display Ult Charge Generation](#params-ult)

### [License](#liscense)



<a id="install"></a>
## <br> Installation

If you're already in a Discord server which has Karen added, there's no need to install anything - you can start using commands in the designated channels right away! Jump to the [section on usage](#commands) for a detailed explanation of how to use these commands to their fullest potential.

<a id="install-discord"></a>
### Adding to Discord

If you want to add Karen to your Discord server, you can do it using [this link](https://discord.com/oauth2/authorize?client_id=1343900821405827072&permissions=18432&integration_type=0&scope=bot). Karen requests minimal premissions to function, but it does need to be able to read and send messages to function.

<a id="install-data"></a>
### Data Sharing

Karen keeps a tally of how many times each combo has been evaluated to help understand how it is being used. It also knows how many servers it is running on. Karen **does not** read messages in your server besides commands (but as a PSA, Discord is fundamentally a public platform, and you should never consider your messages in any server to be truly private).



<a id="commands"></a>
## <br> Commands

All commands are accessed using a `!` followed by the name of the command and any associated arguments. For example, one might run the command `!eval tracer > overhead > tracer > uppercut` which would, as expected, give information on the combo provided. For more information on how to write a combo that Karen will understand, see the section on [combo comprehension](#comprehension).

<a id="commands-eval"></a>
### Evaluate

<a id="commands-tech"></a>
### Tech

<a id="commands-list"></a>
### List

The `!list` command causes Karen to output a list of all named combos.
Lists of all actions available in combos, 

<a id="commands-prefs"></a>
### Preferences

The `!prefs` command allows a user to set a default list of [parameters](#params) to execute with each command. For example, if a user runs `!prefs -n`, then every time they run a command with no parameters specified, the "no warnings" parameter will be automatically added. 

If any parameters are explicitly given to a command, the user's preferences are ignored. This means that a user can access the command's default behaviour by using an empty parameter (eg. `!eval t -`).

<a id="commands-help"></a>
### Help

The `!help` command will give a list of all recognised commands and link to this documentation. More information can be found on any command using `!help [command]`.



<a id="comprehension"></a>
## <br> Combo Comprehension

To make Karen as intuitive and efficient to use as possible, many ways of describing the same combo are supported. There are three broad categories of notation:
- Long-form: `tracer > get over here targetting > uppercut`
- Short-form: `tGu`
- Named sequences: `bread and butter`

A user can mix and match notations, and Karen will do its best to interpret what is meant. Regardless of the user's chosen notation, Karen will always output the full long-form sequence with its output so that the user can verify that their input was understood correctly.

<a id="comprehension-actions"></a>
### Individual Actions

<a id="comprehension-movestacks"></a>
### Movestacks

<a id="comprehension-sequences"></a>
### Named Sequences

<a id="comprehension-mixed"></a>
### Mixed Inputs / Grammar

<a id="comprehension-comments"></a>
### Comments

<a id="comprehension-wait"></a>
### Wait

<a id="comprehension-autocorrection"></a>
### Autocorrection




<a id="params"></a>
## <br> Parameters

Each command supports the addition of parameters which allow the user to adjust the format/information presented in the output of the command. A user can save a default set of parameters using the [prefs](#commands-prefs) command.

<a id=params-a></a>
### Advanced Mode (--a)

<a id=params-b></a>
### Show Breakdown (--b)

<a id=params-n></a>
### No Warnings (--n)

<a id=params-t></a>
### Display Time (--t)

<a id=params-tfd></a>
### Display Time From Damage (--tfd)

<a id=params-d></a>
### Display Damage (--d)

<a id=params-dps></a>
### Display DPS (--dps)

<a id=params-ult></a>
### Display Ult Charge Generation (--ult)



<a id="liscense"></a>
## <br> Liscense
`Karen` is distributed under the terms of the [MIT license](https://spdx.org/licenses/MIT.html).