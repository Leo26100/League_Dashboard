# League Tournament Dashboard  

I wanted to create a dashboard with stats/ standings of the tournaments that are going on right now in the League of Legends scenes. Right now I am focusing on the "Main Regions" which is North America (LCS), Europe (LEC), China (LPL), Korea (LCK). Currently working on the layout of the dashboard. I want to create pages that focuses on other regions and as well as one page dedicatied to international events.

All of the data comes from [Leaguepedia](https://lol.gamepedia.com/League_of_Legends_Esports_Wiki "Leaguepedia Homepage") through the use of their [API's](https://lol.gamepedia.com/Help:API_Documentation "APIs"). Really appreciate their hard work on maintaing all of this data (they are amazing!)



# Running the program and goals

### Running the program

```
cd Disk:\path to project\League_Dashboard
pip install -r requirements.txt
python index.py

```
### Goals
Here's an image of how it looks like right now  ![image](/docs/Prototype.png "Prototype") 

Right now the main page shows the four main regions and the following information
1. Standings for the tournament with the win rate
2. Graph with usual information regarding multiple things like Gold, Gold Difference, Dragons, Barons, Kills, ect. 
3. Histogram of the picks of this tournament

I want to make the following changes
+ Align the histograms of bans and picks together and add title and caption 
+ Change name for columns and graph axis
+ Add a rating system for the teams
+ Do the same for the other regions and international events/ playoffs


