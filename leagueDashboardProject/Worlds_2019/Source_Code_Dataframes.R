#This is the source code that contains the data mining and the tidying from "Match History Game" Table and
#the "Pick Ban History" Table from the LOLEsports Wiki page

library(rvest)
library(httr)
library(tidyverse)
library(dplyr)

#Worlds match history----
#Match History Game Table is going to be used to get the winners for the Pick Ban History
#Mining and tidying the table
MatchHistory_url <- "https://lol.gamepedia.com/index.php?pfRunQueryFormName=MatchHistoryGame&title=Special%3ARunQuery%2FMatchHistoryGame&MHG%5Bpreload%5D=Tournament&MHG%5Btournament%5D=2019+Season+World+Championship%2FMain+Event&MHG%5Bteam%5D=&MHG%5Bteam1%5D=&MHG%5Bteam2%5D=&MHG%5Bban%5D=&MHG%5Brecord%5D=&MHG%5Bascending%5D%5Bis_checkbox%5D=true&MHG%5Blimit%5D=77&MHG%5Bwhere%5D=&MHG%5Btextonly%5D%5Bis_checkbox%5D=true&MHG%5Btextonly%5D%5Bvalue%5D=1&wpRunQuery=Run+query&pf_free_text="

MatchHistory_html <- read_html(MatchHistory_url)

MatchHistory_nonTidy_df <- html_table(MatchHistory_html, fill = TRUE)

MatchHistory_nonTidy_df <- MatchHistory_nonTidy_df[1] %>%
  as.data.frame()
MatchHistory_ColumnNames <- MatchHistory_nonTidy_df[1,]
names(MatchHistory_nonTidy_df) <- MatchHistory_ColumnNames

#ID the matches to be able to join the table with the Pick and Ban Tables

MatchHistory_nonTidy_df <- MatchHistory_nonTidy_df[3:length(MatchHistory_nonTidy_df$Date),] %>%
  rowid_to_column("ID")

#Subsetting Match History DF to Winner DF. This going to be used to join Winner_df with Picks_df and Bans_df
Winner_df <- MatchHistory_nonTidy_df['Winner'] %>%
  rowid_to_column("ID")

#Worlds Pick and Ban------
#Mining and tidying the Pick and Ban Table
xpath_pbh = "//*[@id='pbh-table']"
PickandBan_url <- "https://lol.gamepedia.com/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=Worlds%202019%20Main%20Event&PBH%5Btextonly%5D=Yes&pfRunQueryFormName=PickBanHistory"

PickandBan_html <- read_html(PickandBan_url)

PickandBan_df <- html_node(PickandBan_html, xpath = xpath_pbh)

PickandBan_df_non_tidy <- html_table(PickandBan_df, header = FALSE)

names <- PickandBan_df_non_tidy[2,]

names(PickandBan_df_non_tidy) <- names

PickandBan_df_non_tidy <- PickandBan_df_non_tidy[3:length(PickandBan_df_non_tidy$Phase),]%>%
  as_tibble() %>%
  separate(col = `RP1-2`, into = c("RP1", "RP2"), sep = ", ") %>%
  separate(col = `BP2-3`, into = c("BP2", "BP3"), sep = ", ") %>%
  separate(col = `BP4-5`, into = c("BP4", "BP5"), sep = ", ")

PickandBan_df_non_tidy <- PickandBan_df_non_tidy %>%
  rowid_to_column("ID") %>%
  subset(select = c(ID,Phase:Score, BB1:RR5))
#Creating two tables Picks_df that will focus on the champions that were picked and Bans_df that will focus on champions that were ban
#Tidying Picks Table----
#Pivot_longer from match to champion picked by role, order, phase
Picks_df_non_tidy <- PickandBan_df_non_tidy %>%
  subset(select = -c(BB1:RB3,RB4:BB5))

Picks_df <- Picks_df_non_tidy %>%
  pivot_longer(cols = c(BP1:RP5),
               names_to = "Side",
               values_to = "Champions") %>%
  pivot_longer(cols = c(BR1:RR5),
               names_to = "Selection",
               values_to = "Role")
Picks_df$Side <-  gsub("P","R",Picks_df$Side)

Picks_df <- Picks_df %>%
  filter(Side == Selection) %>%
  subset(select = c(Phase:Champions, Role, ID)) %>%
  separate(col = Side, into = c("Side", "Order"), sep = 2)
Picks_df$Side[Picks_df$Side == "RR"] <- "Red"
Picks_df$Side[Picks_df$Side == "BR"] <- "Blue"

Picks_df <- Picks_df %>%
  pivot_longer(cols = c(Blue:Red),
               names_to = "Color",
               values_to = "Team") %>%
  filter(Side == Color) %>%
  subset(select = c(Phase:Role, Team, ID))
#Edits to make Picks_df add winner in df
Picks_df <- full_join(Picks_df, Winner_df, by = 'ID')

Picks_df$Winner <- Picks_df$Team == Picks_df$Winner

Picks_df$Stage <- ifelse(grepl('^Day',Picks_df$Phase), "Group", "Knockout")
Picks_df$Stage <- ifelse(grepl('^Tiebreakers',Picks_df$Phase),"Group",Picks_df$Stage)

#Tidying bans table ----
#Pivot_longer from match to champion picked by order, phase
Bans_df_non_tidy <- PickandBan_df_non_tidy %>%
  subset(select = c(ID,Phase:RB3,RB4:BB5))

Bans_df <- Bans_df_non_tidy %>%
  pivot_longer(cols = c(BB1:BB5),
               names_to = "Side",
               values_to = "Champions") %>%
  separate(col = Side, into = c("Side", "Order"), sep = 2)

Bans_df$Side[Bans_df$Side == "BB"] <- "Blue"

Bans_df$Side[Bans_df$Side == "RB"] <- "Red"

Bans_df <- Bans_df %>%
  pivot_longer(cols = c(Blue:Red),
               names_to = "Color",
               values_to = "Team") %>%
  filter(Side == Color) %>%
  subset(select = c(ID, Phase:Champions, Team))
Bans_df <- full_join(Bans_df, Winner_df, by = 'ID')

Bans_df$Winner <- Bans_df$Team == Bans_df$Winner
Bans_df$Stage <- ifelse(grepl('^Day',Bans_df$Phase), "Group", "Knockout")
Bans_df$Stage <- ifelse(grepl('^Tiebreakers',Bans_df$Phase),"Group",Bans_df$Stage)
