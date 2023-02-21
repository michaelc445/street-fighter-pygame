<p align="center">
  <img src="game/assets/screenshots/readme_headerv1.jpg"/>
</p>


<div align="center">
<a href="https://discord.gg/rrVNskkC"><img src="https://camo.githubusercontent.com/b12a95e20b7ca35f918c0ab5103fe56b6f44c067/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636861742d6f6e253230646973636f72642d3732383964612e737667" alt="Discord" /></a>
</div>


<p align="center">
  <strong>Welcome to Martial Mayhem, the online multiplayer fighting game made with pygame.</strong>

  <img width="704" alt="Game screenshot" src="game/assets/screenshots/nomadvwizard.png">
</p>

# Getting Started

Go to your favourite terminal, clone the repository, then:

    pip3 -m install requirements.txt
    python3 main.py
    
### To Download the game

Do the above, then:

    -> in main.spec, change the path in line 9 to the path where your python packages are located
    -> be sure to use double backslashes
    -> in the terminal where main.spec is located
    pyinstaller main.spec

# How To Play

- Select your Fighter and the map
- Win rounds by attacking the opponent until their health bar is depleted
- First fighter to win 3 rounds wins the game!


# Game Modes

<div align="left">
  <img width="200" alt = "singleplayer" src="game/assets/screenshots/single.jpg"/>
  <strong>Battle against the computer in an intense one on one match!</strong>
</div>
<div align="left">
  <img width="200" alt = "local" src="game/assets/screenshots/local.png"/>
  <strong>Play your friend locally using the same keyboard!</strong>
</div>
<div align="left">
  <img width="200" alt = "multiplayer" src="game/assets/screenshots/multi.png"/>
  <strong>Queue up for an intense match online!</strong>
</div>
We use a server provided by NetSoc, which can host up to 10 simultaneous games.

# Controls

## Player 1
    W - jump
    A - move left
    S - block
    D - move right

    R - light attack
    T - heavy attack

## Player 2
    up arrow - jump
    left arrow - move left
    down arrow - block
    right arrow - move right

    N - light attack
    M - heavy attack

# Characters

## Wizard
<p align="left">
  <img src="game/assets/screenshots/wizardchar.png"/>
</p>
A zoner with powerful ranged attacks, stay away and poke the enemy from range!

    light attack - quick spammable projectile with small damage and knockback
    heavy attack - a large slow projectile with massive damage and knockback

## Warrior
<p align="left">
  <img src="game/assets/screenshots/warriorchar.png"/>
</p>
A bruiser with ppowerful melee attacks, don't let him get close!

    light attack - quick sword swing good for staggering the opponent
    heavy attack - heavy sword swing which does devastating damage

## Nomad
<p align="left">
  <img src="game/assets/screenshots/nomadchar.png"/>
</p>
A specialist of all fighting styles, dangerous at any range!

    light attack - a quick and deadly sword swing with short range
    heavy attack - a projectile with big knockback on hit

# Credits

Check out the [Credits](CREDITS.md) page and show some love to the artists who let us use their tile sets.

# Contributing

Feel free to join the [Discord channel](https://discord.gg/rrVNskkC) if you want to contribute!

