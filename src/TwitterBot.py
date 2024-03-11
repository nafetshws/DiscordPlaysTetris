import tweepy 
from TetrisBot import TetrisBot
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import random


class TwitterBot:

	def __init__(self, timeout):
		self.timeout = timeout
		self.creds = None
		self.last_tweet_id = 1340639094406311937
		self.init()
		

	def init(self):
		with open("twitter_credentials.json", "r") as f:
			self.creds = json.load(f)

	def return_retweet_count(self, api):
		tweet = api.get_status(self.last_tweet_id)
		return tweet.retweet_count

	def return_like_count(self, api):
		tweet = api.get_status(self.last_tweet_id)
		return tweet.favorite_count


	def return_reply_count(self, api):
		
		options = Options()
		options.add_argument("--headless")
		options.add_argument("--disable-gpu")
		driver = webdriver.Chrome(options=options,executable_path="D:\\Benutzer\\Stefan\\chromedriver.exe")
		driver.get("https://twitter.com/plays_tetris")
		try:
			wait = WebDriverWait(driver, 10)
			replie_count = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/section/div/div/div[1]/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/span/span'))).text
		except:
			replie_count = "0"
		driver.quit()
		return replie_count

	def post_board(self, api):
		image_path = "sprites/current_board.png"
		status = "Controls: Check out bio"
		data = api.update_with_media(image_path, status)
		self.last_tweet_id = data.id
		print(data.id)

	def check_control(self, api):
		return random.randint(0, 3)
		like_count = self.return_like_count(api)
		retweet_count = self.return_retweet_count(api)
		try:
			reply_count = int(self.return_reply_count(api))
		except:
			reply_count = 0
		if like_count > retweet_count and like_count > reply_count:
			return 0
		elif retweet_count > reply_count and retweet_count > like_count:
			return 2
		elif reply_count > retweet_count and reply_count > like_count:
			return 1
		else:
			return 3

	def main(self):
	
		#twitter
		auth = tweepy.OAuthHandler(self.creds["CONSUMER_KEY"], self.creds["CONSUMER_SECRET"])
		auth.set_access_token(self.creds["ACCESS_TOKEN"], self.creds["ACCESS_SECRET"])
		api = tweepy.API(auth)
		running = True
		tetris = TetrisBot()
		tetris.start_game()

		while running:
			tetris.move_down_tetromino(1)
			state = self.check_control(api)
			if state == 0:
				tetris.rotate()
			elif state == 1:
				tetris.move_left()
			elif state == 2:
				tetris.move_right()
			elif state == 3:
				tetris.move_down_tetromino(18)
			tetris.update_image()
			self.post_board(api)
			print("Posting board")
			time.sleep(15*60)

		
if __name__ == "__main__":
	bot = TwitterBot(2*60)
	bot.main()