###############################################
# Cleaning data
###############################################

# files to build:
part1 = data/clean/part1.csv
part2 = data/clean/part2.csv
all = data/clean/all.csv
pairs = data/clean/pairs.csv

# initialize clean_data as empty
clean_data = 
# add files to clean_data
clean_data += $(part1)
clean_data += $(part2)
clean_data += $(all)
clean_data += $(pairs)

# recipe that describes how to build the files from the raw data
$(part1) $(part2) $(all) $(pairs): data/raw/Part1_2023-06-05.csv data/raw/Part2_2023-06-05.csv data/raw/Part1_2023-06-08_1.csv data/raw/Part2_2023-06-08_1.csv $(model_accuracy) data/scripts/clean_data.py
	@echo "Cleaning our first file!"
	python data/scripts/clean_data.py

# This recipe concludes when clean_data is built
clean_data: $(clean_data)
	@echo "Data is now clean!"

clean_data_clean:
	rm -f $(clean_data)
	make clean_data


###############################################
# computing objects
###############################################

# files to build:
learning_part1                 = computed_objects/figures/learning_part1.png
learning_all                   = computed_objects/figures/learning_all.png
single_variable_time           = computed_objects/figures/single_variable_time.png
variable_choices_average       = computed_objects/figures/variable_choices_average.png
variable_choices_time          = computed_objects/figures/variable_choices_time.png
revealed_variables_pooled      = computed_objects/figures/revealed_variables_pooled.png
assigned_variables             = computed_objects/figures/assigned_variables.png
assigned_variables_time        = computed_objects/figures/assigned_variables_time.png
revealed_available             = computed_objects/figures/revealed_available.png
model_accuracy                 = computed_objects/tables/model_accuracy.csv
performance_part1              = computed_objects/figrues/performance_part1.png
p1_performance_throughout      = computed_objects/figures/p1_performance_throughout.png
p1_performace_effect_assigned  = computed_objects/figures/p1_performace_effect_assigned.png
p1_performace_effect_revealed  = computed_objects/figures/p1_performace_effect_revealed.png
p2_correct_rounds              = computed_objects/figures/p2_correct_rounds.png
p2_performance_effect_revealed = computed_objects/figures/p2_performance_effect_revealed.png
p2_performance_effect_assigned = computed_objects/figures/p2_performance_effect_assigned.png
p2_performance_by_model        = computed_objects/figures/p2_performance_by_model.png
p2_performance_model_choices_2var = computed_objects/figures/p2_performance_model_choices_2var.png
regression_revealed            = computed_objects/tables/regression_revealed.txt
regression_assigned            = computed_objects/tables/regression_assigned.txt
ttest_assigned                 = computed_objects/tables/ttest_assigned.txt
ttest_revealed                 = computed_objects/tables/ttest_revealed.txt
model_choices_2vars            = computed_objects/figures/model_choices_2vars.png
model_choices_all 		       = computed_objects/figures/model_choices_all.png
accuracy_rounds                = computed_objects/figures/accuracy_rounds.png
polarization_rounds_predicted  = computed_objects/figures/polarization_rounds_predicted.png
regression_predicted_polariz   = computed_objects/tables/regression_predicted_polariz.txt
ttest_predicted_polariz 	   = computed_objects/tables/ttest_predicted_polariz.txt
polarization 				   = computed_objects/figures/polarization.png
predicted_polarization_ttest   = computed_objects/tables/predicted_polarization_ttest.txt


# recipe that describes how to build the model_accuracy
$(model_accuracy): data/scripts/simulation_accuracy.py
	@echo "Model accuracy"
	python data/scripts/simulation_accuracy.py

# initialize plots as empty
plots =
# add files to plots
plots += $(learning_part1)
plots += $(learning_all)
plots += $(single_variable_time)
plots += $(variable_choices_average)
plots += $(variable_choices_time)
plots += $(revealed_variables_pooled)
plots += $(assigned_variables)
plots += $(assigned_variables_time)
plots += $(revealed_available)
plots += $(p1_performance_throughout)
plots += $(performance_part1)
plots += $(p1_performace_effect_assigned)
plots += $(p1_performace_effect_revealed)
plots += $(p2_correct_rounds)
plots += $(p2_performance_effect_revealed)
plots += $(p2_performance_effect_assigned)
plots += $(p2_performance_by_model)
plots += $(p2_performance_model_choices_2var)
plots += $(regression_revealed)
plots += $(regression_assigned)
plots += $(ttest_assigned)
plots += $(ttest_revealed)
plots += $(model_choices_2vars)
plots += $(model_choices_all)
plots += $(accuracy_rounds)
plots += $(polarization_rounds_predicted)
plots += $(regression_predicted_polariz)
plots += $(ttest_predicted_polariz)
plots += $(polarization)
plots += $(predicted_polarization_ttest)

# recipe that describes how to build the learning plots from the clean data
$(learning_part1) $(learning_all): $(part1) $(all) analysis/learning_plots.py
	@echo "Learning plots"
	python analysis/learning_plots.py


# recipe that describes how to build the variable choice plots from the clean data
$(single_variable_time) $(variable_choices_average) $(variable_choices_time): $(part2) analysis/variable_choices.py
	@echo "Variable choice plots"
	python analysis/variable_choices.py

# recipe that describes how to build the effects aggregate plots from the clean data
$(revealed_variables_pooled) $(assigned_variables) $(assigned_variables_time) $(revealed_available): $(part2) analysis/effects_aggregate.py
	@echo "Effects plots"
	python analysis/effects_aggregate.py

# recipe that describes hot yo build the part1 perfomance plots
$(p1_performance_throughout) $(performance_part1) $(p1_performace_effect_assigned) $(p1_performace_effect_revealed): $(part1) analysis/part1_performance.py
	@echo "Part1 performance plots"
	python analysis/part1_performance.py

# recipe that describes how to build the part2 perfomance plots
$(p2_correct_rounds) $(p2_performance_effect_revealed) $(p2_performance_effect_assigned) $(p2_performance_by_model) $(p2_performance_model_choices_2var): $(part2) $(part1) $(all) analysis/part2_performance.py
	@echo "Part2 performance plots"
	python analysis/part2_performance.py


#recipe that describes how to build the regression tables
$(regression_revealed) $(regression_assigned) $(ttest_assigned) $(ttest_revealed): $(part2) $(part1) $(all) analysis/regressions.py
	@echo "Regression tables"
	python analysis/regressions.py


# recipe that describes how to build the model choice plots
$(model_choices_2vars) $(model_choices_all) $(accuracy_rounds): $(part2) $(part1) $(all) analysis/model_choices.py
	@echo "Model choice plots"
	python analysis/model_choices.py

# recipe that describes how to build the polarization plots
$(polarization_rounds_predicted) $(regression_predicted_polariz) $(ttest_predicted_polariz) $(polarization) $(predicted_polarization_ttest): $(part2) $(part1) $(all) $(pairs) analysis/polarization.py
	@echo "Polarization plots"
	python analysis/polarization.py



# This recipe concludes when plots are built
plots: $(plots)
	@echo "Plots are now built!"

plots_clean:
	rm -f $(plots)
	make plots