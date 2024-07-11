# Setup

```bash
# Update the OS
sudo apt-get update
sudo apt-get upgrade

# Setup VS Code
# Download the .deb amd64 file from https://code.visualstudio.com/download
```

## R

```bash
# Install R
sudo apt-get install gdebi-core

export R_VERSION=4.4.1
cd ~
curl -O https://cdn.rstudio.com/r/debian-11/pkgs/r-${R_VERSION}_1_amd64.deb
sudo gdebi r-${R_VERSION}_1_amd64.deb

# Check the version
/opt/R/${R_VERSION}/bin/R --version

# Create symlinks
sudo ln -s /opt/R/${R_VERSION}/bin/R /usr/local/bin/R
sudo ln -s /opt/R/${R_VERSION}/bin/Rscript /usr/local/bin/Rscript

# Install the required libraries
sudo apt-get install libudunits2-dev libxml2-dev libfontconfig1-dev

# Install JAGS
sudo apt-get install jags
```

Start R and then install the required packages:

```R
sudo apt-get install libudunits2-dev libxml2-dev libfontconfig1-dev jags

# rjags
Sys.setenv(LD_RUN_PATH="/usr/lib/x86_64-linux-gnu/JAGS/modules-4")
install.packages('rjags', dependencies=TRUE, repos='http://cran.rstudio.com/')

install.packages('jsonlite', dependencies=TRUE, repos='http://cran.rstudio.com/')
install.packages('functional', dependencies=TRUE, repos='http://cran.rstudio.com/')
install.packages('languageserver', dependencies=TRUE, repos='http://cran.rstudio.com/')
install.packages('rjags', dependencies=TRUE, repos='http://cran.rstudio.com/')
```

Alternatively:

```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key '95C0FAF38DB3CCAD0C080A7BDC78B2DDEABC47B7'
# Add to /etc/apt/sources.list:
# deb http://cloud.r-project.org/bin/linux/debian bookworm-cran40/
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install r-base r-base-dev
```

## Python

```bash
# Install a version of Python with a GUI
sudo apt-get install python3-tk python3-pip

# Install libraries
pip install -r ./Python/requirements.txt
```

## Golang

```bash
# Remove old version
sudo rm -rf /usr/local/go

# Download and install a new version
cd ~
wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz

# Add the path by editing .profile
# vim $HOME/.profile
# Add the following line to the end
# export PATH=$PATH:/usr/local/go/bin

# Check Golang is installed
go version

# Ebitengine development
sudo apt install libc6-dev libglu1-mesa-dev libgl1-mesa-dev libxcursor-dev libxi-dev libxinerama-dev libxrandr-dev libxxf86vm-dev libasound2-dev pkg-config
```