# packages and parameters for the project
library(data.table)
library(here)
library(huxtable)
library(broom)
library(magrittr)
library(languageserver)
library(reticulate)
library(car) # for linearHypothesis
library(lmtest) # for coefTest
library(sandwich) # for clustering errors

invisible(capture.output(renv::snapshot())) # keep the packages synced with the lockfile

# parameters
params = list(date_of_exp = '2023-04-01')