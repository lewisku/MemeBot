import os
import redditmemes
import database

def parseUserArguments(num):
	#set some defaults. Subject to change
	acceptablePop = 20
	
	#check database for memes
	for i in range (0, num):
		newMeme = [database.getMeme(list())]

		#check usage, availability		
		if newMeme[0] is None or newMeme[0].popularity <= acceptablePop:
			#cycle through subreddits. 
			#Keep track of current subreddit in subFile.txt
			with open('subFile.txt','r') as subredditChoice:
				choice = int(subredditChoice.read())
				
			
			sub = ["me_irl","meow_irl","woofbarkwoof","notmyjob","firstworldanarchists", "memes","blackpeopletwitter"]
				
			#call Zach's function to get 30 memes
			if choice > len(sub)-1:
				choice = 0
			filenames = redditmemes.getSomeMemes(sub[choice], 10)
			choice = choice + 1
			if choice > len(sub)-1:
				choice = 0
			filenames += redditmemes.getSomeMemes(sub[choice],10)
			choice = choice + 1
			if choice > len(sub)-1:
				choice = 0
			filenames += redditmemes.getSomeMemes(sub[choice],10)
			choice = choice + 1			
			
			#write index value of next subreddit back to file	
			choice_s = repr(choice)
			with open('subFile.txt','w') as subredditChoice:
				subredditChoice.write(choice_s)
			
			id = list()
			for i,x in enumerate(filenames):
				#parsing filename (dont use this info yet but may in future)
				extension = x.split(".")[-1]
				subreddit = x.split("_")[-6]
				if subreddit == "irl":
					subreddit = x.split("_")[-7] + "_irl"
					source = x.split("_")[-8]
				else:
					source = x.split("_")[-7]	
				imgHost = x.split("_")[-2]
				id = x.split("_")[-1]
				
				#concatenate to form link to image
				link = "http://i.imgur.com/" + id 
				
				#Populate object fields
				popularity = 25
				tagsList = subreddit
				
				#create local object
				if i != 0:
					newMeme.append(database.Meme(link,tagsList,popularity))
				else:
					newMeme.append(database.Meme(link,tagsList,0))
				#save to database
			
			m=1
			n = 2
			while n < 9:
				database.storeMeme(newMeme[m])
				m += 7
				if m > len(newMeme)-1:
					m = n
					n += 1
				
			return newMeme[1].imgLink

		else:
			#If database meme is accepted
			newMeme[0].popularity = 0
			database.storeMeme(newMeme[0])
		

	#return meme link to bot
	return newMeme[0].imgLink
parseUserArguments(1)
