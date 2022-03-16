# Halo Infinite Stats Analysis

Simple GUI implementation to track stats of past Halo Infinite ranked crossplay games.

## Description

A random project idea I spent just under 10 total hours working on to complete. Using Autocode and HaloDotApi, you can now track your accuracy, K/D, and other statistics over your past 10 games, as well as see your past game history!

## Getting Started

### Usage (for non-developers)

Simply download the exe under releases (also found at https://github.com/EternalDusk/Infinite-Analysis/releases )

Run main.exe, and once the window pops up just enter in your username.

Then, in your web browser, navigate to http://localhost:8080/

### Dependencies

* lib
* Flask

### Installing

* From source:

```
git clone https://github.com/EternalDusk/Infinite-Analysis
cd Infinite-Analysis
```
Navigate to https://autocode.com/auth/, make a free account and get a General Use Identity Token (found under the Identity Tokens menu)

Open main.py, and under settings on line 21, replace <insert_token_here> with your token

### Executing program

* Run main.py or run release.exe

* Enter in the username you want to track

* Go to http://localhost:8080 to view your statistics (it may take a second to load)

## Help

If you run into any issues, feel free to leave an issue comment

OR

Join the discord (it's not very active, but I'll always be willing to help!)

## Authors

Contributors names and contact info

Eternal Dusk

[@EternalDusk](https://linktr.ee/EternalDusk)

## Version History

* v1.0
    * Initial Release
* v1.0.1
    * Fixed bug causing crash when player never played a ranked match
    * Fixed bug where player had space in their name
    * Table shows all game history, not just ranked
* v1.1.0
    * Removed unnecessary modal search bar code
    * Saved all teams data for each page
    * Added past games page
    * Fixed bug where player had less than 10 games played
    * Added better handling to determining ranked matches
    * Added game data to each game
    * Webpage automatically opens on program startup

## To-Do
- [ ] Medal Chest
- [ ] Custom Scoring System
- [ ] Automatically update/reload webpage on new game
- [ ] Filtering by custom/ranked/social games

## Acknowledgments

* [Autocode](https://www.autocode.com/)
* [HaloDotApi](https://halodotapi.com/)
* [StackOverflow](https://stackoverflow.com/) (cause God KNOWS I couldn't do this on my own :P )
