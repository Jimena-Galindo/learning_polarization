#!/usr/bin/env Rscript

# read the dependencies
source("parameters_and_packages.R")

data <- fread(here("data", "clean", "all.csv"))
part1 <- fread(here("data", "clean", "part1.csv"))
part2 <- fread(here("data", "clean", "part2.csv"))

# regression with the number of variables that subjects were allowed to disclose
model1 <- lm(player.correct ~ C(player.number_variables) - 1, data = part2)
model2 <- lm(player.correct ~ C(revealed_variables_count) - 1, data = part2)

# cluster errors by group
model4 <- lm(player.correct ~ C(player.number_variables) - 1, data = part2)
m4coeffs_cl <- coeftest(model4, vcov = vcovCL, cluster = ~group_id, save = TRUE)

models <- list(m1 = model1, m2 = model2, m4 = m4coeffs_cl)

# save the model
saveRDS(models, here("computed_objects", "tables", "regressions.rds"))
