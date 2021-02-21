# openlegend-discord-dicebot
An OpenLegend RPG dice bot for Discord servers 

## Configuration

Set your Discord token in env variable ```DISCORD_OPENLEGEND_BOT_TOKEN```

## Usage

```/roll [flags] [attribute] [advantage] [quantity]```

```/r [flags] [attribute] [advantage] [quantity]```
    
Flags:

 ```-R```: Repeat the roll 
 
 ```-V```: Vicious Strike: Exploding dice have advantage 
 
 ```-D```: Destructive Trance: Explode on max or one less

### Raw Dice Using xdice Patterns

```/!r [xdice pattern]``` 

```/!roll [xdice pattern]```

```xdice pattern```: Given pattern should be as described in [xdice documentation](https://xdice.readthedocs.io/en/latest/dice_notation.html#patterns). Use this to roll "raw", i.e. without any Openlegend RPG specific logic. 

## Used External Libraries 

- [Rapptz/discord.py](https://github.com/Rapptz/discord.py)
- [cro-ki/xdice](https://github.com/cro-ki/xdice)
