# Twitter plays Tetris 
This is a bot which lets the Twitter community play Tetris. You can engage with the bot by liking, commenting and retweeting.
![Twitter plays Tetris](TwitterPlaysTetris.png)

## Controls
How can the community influence the game:
1. **Like**: Rotate (clockwise)
2. **Comment**: Move left
3. **Retweet**: Move right

The majority will decide what the next In-Game action will be.

## Game Updates
The game will be updated every 30 minutes. The reason for this limitation is the Twitter API (free tier).

## How to run
First you need to install pillow:
```shell
pip3 install pillow
```
Then you can run
```
python3 src/TetrisBot.py
```

## TODO
- update blank tile
- update game over png