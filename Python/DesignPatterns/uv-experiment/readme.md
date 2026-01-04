# uv Python package and project manager

## Installation

```bash
# Install
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version

# Update the version
uv self update
```

## Managing Python versions

```bash
# Show available Python versions
uv python list

# Install a specific version
uv python install 3.12

# Upgrade Python to the latest patch release
uv python upgrade 3.12

```

## Running a standalone script

```bash
# Run a script with no dependencies
uv run example_no_deps.py

# Run a script with no dependencies an command line args
uv run example_no_deps.py Chris

# Run a script with dependencies
uv run --with numpy --with matplotlib example_deps.py
```

Create a script and add inline dependencies

```bash
# Initialise a script
uv init --script example_deps2.py --python 3.11

# Add a dependency
uv add --script example_deps2.py 'numpy' 'matplotlib'

# Run the script (uv automatically creates an environment with the dependencies
# to run the script)
uv run example_deps2.py

# Create a lock file
uv lock --script example_deps2.py
```

## Making a project

```bash
# Create a new project in a new directory
uv init hello_world
cd hello_world

# Run the auto-generated main.py file (note that it creates a virtual 
# environment)
uv run main.py

# Add dependencies to the project
uv add numpy matplotlib

# To remove a dependency from the project
uv remove numpy

# To upgrade a package
uv lock --upgrade-package numpy

# Get the version of the package
uv version

# Manually update the environment and activate it
uv sync
source .venv/bin/activate
python main.py

# Update the version to a specific version
uv version 1.0.0

# Increase the version using semantics
# major, minor, patch, stable, alpha, beta, rc, post, dev
uv version --bump minor

# Build a distribution
uv build
ls -la ./dist

# Test the installation of the package
cd ..
uv run --with hello_world --no-project -- python -c "import hello_world"
```
