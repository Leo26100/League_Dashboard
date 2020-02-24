library(shiny)
library(shinydashboard)

source("Worlds_2019/Source_Code_Dataframes.R")

sidebar <- dashboardSidebar(
)

body <- dashboardBody(
    )
ui <- dashboardPage(
    dashboardHeader(title = 'Season 9 Worlds'),
    sidebar,
    body
)

server <- function(input,output) { }

shinyApp(ui, server)

