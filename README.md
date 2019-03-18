# akoteka

The aim of this project is to produce a software which helps to organize and play media

<table border="0">
<tr>  
<td><img src='https://github.com/dallaszkorben/akoteka/blob/master/wiki/cardlist-simple.png' width='400'>
<td><img src='https://github.com/dallaszkorben/akoteka/blob/master/wiki/cardlist-filter.png' width='400'> 
<td><img src='https://github.com/dallaszkorben/akoteka/blob/master/wiki/cardlist-setting.png' width='400'> 
<tr/>
<tr>
<td>Normal view<br>
<td>Filter<br>
<td>Setting<br> 
<tr/>
<table>



## The main features are:
- Navigation in the Card hierarchy
  - <img src='https://github.com/dallaszkorben/akoteka/blob/master/wiki/card-navigation.png' width='600'>    

- Cards show the characteristics of the media
  - Title, Year, Length, Country, Sound, Subtitle, Director, Actor, Genre, Theme, Story
  - <img src='https://github.com/dallaszkorben/akoteka/blob/master/wiki/card-single.png' width='600'>    
- Indicate personal opinion about the media 
  - Favorite, Best, New
  - <img src='https://github.com/dallaszkorben/akoteka/blob/master/wiki/personalopinion.png' width='20'>   
- Paging Cards in card-holder
  - <img src='https://github.com/dallaszkorben/akoteka/blob/master/wiki/paging.gif' width='600'>

- Fast filtering Cards by title, genre, theme, director, actor ...
  - <img src='https://github.com/dallaszkorben/akoteka/blob/master/wiki/filter-fast.gif' width='600'>
  
- Advanced filtering Cards by title, genre, theme, language, director, actor, year ...
  - <img src='https://github.com/dallaszkorben/akoteka/blob/master/wiki/filter-advanced.gif' width='600'>

- Playing media one-by-one
- Continously playing media

## Usage

### Preconditions
 - Minimum Python3.6 should be installed on your computer
 - pip (compatible to the Python version) should be installed on your computer
 - The media collection should be already mounted on your file system

### Install

1. Run a console
2. On the console type the following  

		pip install akoteka

### Update

1. Run a console
2. On the console type the following  

		pip install akoteka --upgrade
		

### Run
1. Run a console
2. On the console type the following 

		akoteka
	
## Media

### Card folder

The application needs a special hierarchy of files to recognize media. A folder, which represents a Card, contains the 
- specific media file (**avi, mkv, mp4, mp3 ...**) 
- a descriptor file (**card.ini**) 
- optionaly an image (**image.jpg**).

### Container folder

Card Folders can contain many subfolders, which can themselves be a Card folder. 



### card.ini file

The **card.ini** file is a simple text file containing key-value pairs which describe the media. Here is an example:

### Card hierarchy

 



