"""
Domain objects
"""
class Album():
	id=None
	title=None
	link=None
	cover=None
	label=None
	duration=None
	fans=None
	release_date=None
	artist=None
	tracks=None

class Artist():
	id=None
	name=None
	link=None
	picture=None
	nb_album=None
	nb_fan=None	
	radio=None
		
class Comment():
	id=None
	text=None
	date=None
	album=None
	author=None
		
class Editorial():
	id=None
	name=None
		
		
class Folder():
	id=None
	title=None
	creator=None
	items=None

class Genre():
	id=None
	name=None
	artists=None
		
class Playlist():
	id=None
	title=None
	duration=None
	rating=None
	link=None
	picture=None
	creator=None
	tracks=None
	comments=None
	fans=None
		
class Radio():
	id=None
	title=None
	description=None
	picture=None
	genres=None
	top=None
	tracks=None
		
class Search():
	id=None
	readable=None
	title=None
	link=None
	duration=None
	preview=None
	artist=None
	album=None
	
class Track():
	id=None
	readable=None
	title=None
	link=None
	duration=None
	track_position=None
	disk_number=None
	rank=None
	release_date=None
	preview=None
	artist=None
	album=None
		
class User():
	id=None
	name=None
	lastname=None
	firstname=None
	email=None
	birthday=None
	inscription_date=None
	gender=None
	link=None
	picture=None
	country=None
	albums=None
	artists=None
	charts=None
	folders=None
	followings=None
	followers=None
	permissions=None
	personal_songs=None
	playlists=None
	radios=None