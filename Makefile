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


###############################################
# computing objects
###############################################

# files to build:
learning_part1 = computed_objects/figures/learning_part1.png
learning_all = computed_objects/figures/learning_all.png
single_variable_time = computed_objects/figures/single_variable_time.png
variable_choices_average = computed_objects/figures/variable_choices_average.png
variable_choices_time = computed_objects/figures/variable_choices_time.png
revealed_variables_pooled = computed_objects/figures/revealed_variables_pooled.png
assigned_variables = computed_objects/figures/assigned_variables.png
assigned_variables_time = computed_objects/figures/assigned_variables_time.png
revealed_available = computed_objects/figures/revealed_available.png

model_accuracy = computed_objects/tables/model_accuracy.csv


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

# This recipe concludes when plots are built
plots: $(plots)
	@echo "Plots are now built!"