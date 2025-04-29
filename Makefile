# Makefile for TopoChip Analysis Project

# Create the conda environment
env:
	@echo "🔧 Creating conda environment from environment.yml..."
	conda env create -f environment.yml

# Activate the environment and start JupyterLab
start:
	@echo "🚀 Starting JupyterLab..."
	jupyter lab

# Remove the conda environment
clean:
	@echo "🧹 Removing conda environment 'topochip-env'..."
	conda remove --name topochip-env --all -y

# Export current environment to file (useful for updates)
export:
	@echo "📦 Exporting environment to environment.yml..."
	conda env export --no-builds | grep -v "prefix" > environment.yml
