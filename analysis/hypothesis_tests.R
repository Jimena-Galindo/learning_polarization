#!/usr/bin/env Rscript

# read the dependencies
source("parameters_and_packages.R")

data <- fread(here("data", "clean", "all.csv"))
part1 <- fread(here("data", "clean", "part1.csv"))
part2 <- fread(here("data", "clean", "part2.csv"))

# read the regression models
regs <- readRDS(here("computed_objects", "tables", "regressions.rds"))
model1 <- regs$m1
model2 <- regs$m2
model4 <- lm(player.correct ~ C(player.number_variables) - 1, data = part2)

# Define the individual hypotheses
hypothesis1 <- "C(player.number_variables)1 = 0.5"
hypothesis2 <- "C(player.number_variables)2 - C(player.number_variables)1=0"
hypothesis3 <- "C(player.number_variables)3 - C(player.number_variables)2=0"
hypothesis4 <- "C(player.number_variables)4 - C(player.number_variables)3=0"
hypothesis5 <- "C(player.number_variables)5 - C(player.number_variables)4=0"

model1 <- regs$m1
test_result1 <- car::linearHypothesis(model1, hypothesis1) %>% tidy()
test_result2 <- car::linearHypothesis(model1, hypothesis2) %>% tidy()
test_result3 <- car::linearHypothesis(model1, hypothesis3) %>% tidy()
test_result4 <- car::linearHypothesis(model1, hypothesis4) %>% tidy()
test_result5 <- car::linearHypothesis(model1, hypothesis5) %>% tidy()

results_tbl1 <- rbind(test_result1, test_result2, test_result3, test_result4, test_result5) %>% as.data.table()
results_tbl1 <- results_tbl1[, .(Hypothesis = term,
                               Estimate = estimate,
                               `p-value` = p.value)]

results_tbl1[1, 1] <- "b_1=.5"
results_tbl1[2, 1] <- "b_2-b1=0"
results_tbl1[3, 1] <- "b_3-b2=0"
results_tbl1[4, 1] <- "b_4-b3=0"
results_tbl1[5, 1] <- "b_5-b4=0"

# Do it for model 4 (clustered errors)

cov_matrix <- vcovCL(model4, cluster = ~group_id)

# test the hypotheses with the clustered standard errors
test_result1 <- car::linearHypothesis(model4, hypothesis1, vcov = cov_matrix) %>% tidy()
test_result2 <- car::linearHypothesis(model4, hypothesis2, vcov = cov_matrix) %>% tidy()
test_result3 <- car::linearHypothesis(model4, hypothesis3, vcov = cov_matrix) %>% tidy()
test_result4 <- car::linearHypothesis(model4, hypothesis4, vcov = cov_matrix) %>% tidy()
test_result5 <- car::linearHypothesis(model4, hypothesis5, vcov = cov_matrix) %>% tidy()

results_tbl4 <- rbind(test_result1, test_result2, test_result3, test_result4, test_result5) %>% as.data.table()
results_tbl4 <- results_tbl4[, .(Hypothesis = term,
                               Estimate = estimate,
                               `p-value` = p.value)]

results_tbl4[1, 1] <- "b_1=.5"
results_tbl4[2, 1] <- "b_2-b1=0"
results_tbl4[3, 1] <- "b_3-b2=0"
results_tbl4[4, 1] <- "b_4-b3=0"
results_tbl4[5, 1] <- "b_5-b4=0"


# Hypotheses test for the second model (revealed_variables_count)
# Define the individual hypotheses
hypothesis1 <- "C(revealed_variables_count)0 = 0.5"
hypothesis2 <- "C(revealed_variables_count)1 - C(revealed_variables_count)0=0"
hypothesis3 <- "C(revealed_variables_count)2 - C(revealed_variables_count)1=0"
hypothesis4 <- "C(revealed_variables_count)3 - C(revealed_variables_count)2=0"
hypothesis5 <- "C(revealed_variables_count)4 - C(revealed_variables_count)3=0"
hypothesis6 <- "C(revealed_variables_count)5 - C(revealed_variables_count)4=0"

test_result1 <- car::linearHypothesis(model2, hypothesis1) %>% tidy()
test_result2 <- car::linearHypothesis(model2, hypothesis2) %>% tidy()
test_result3 <- car::linearHypothesis(model2, hypothesis3) %>% tidy()
test_result4 <- car::linearHypothesis(model2, hypothesis4) %>% tidy()
test_result5 <- car::linearHypothesis(model2, hypothesis5) %>% tidy()
test_result6 <- car::linearHypothesis(model2, hypothesis6) %>% tidy()


results_tbl2 <- rbind(test_result1, test_result2, test_result3, test_result4, test_result5, test_result6) %>% 
    as.data.table()

results_tbl2 <- results_tbl2[, .(Hypothesis = term,
                               Estimate = estimate,
                               `p-value` = p.value)]

results_tbl2[1, 1] <- "b_0=.5"
results_tbl2[2, 1] <- "b_1-b0=0"
results_tbl2[3, 1] <- "b_2-b1=0"
results_tbl2[4, 1] <- "b_3-b2=0"
results_tbl2[5, 1] <- "b_4-b3=0"
results_tbl2[6, 1] <- "b_5-b4=0"

# save the results to a list

hypothesis_tests <- list(tbl1 = results_tbl1, tbl2 = results_tbl2, tbl4 = results_tbl4)

# save the model
saveRDS(hypothesis_tests, here("computed_objects", "tables", "hypothesis_tests.rds"))