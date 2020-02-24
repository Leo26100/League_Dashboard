library(shiny)
library(shinydashboard)

source("Worlds_2019/Source_Code_Dataframes.R")

sidebar <- dashboardSidebar(
  menuItem('Dashboard', tabName = 'dashboard', icon = icon('dashboard')),
  menuItem('Picks Table', tabName = 'picks table', icon = icon('table')),
  menuItem('Bans Table', tabName = 'bans table', icon = icon('table'))
)

body <- dashboardBody(
  tabItems(
    tabItem(tabName = 'dashboard',
      h2('Dashboard')),
    tabItem(tabName = 'picks Table',
      h2('Picks Table')),
    tabItem(tabName = 'bans Table',
      h2('Bans Table'))
  )
)
ui <- dashboardPage(
    dashboardHeader(title = 'Season 9 Worlds'),
    sidebar,
    body
)

server <- function(input,output) { }

shinyApp(ui, server)

