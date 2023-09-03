echo "Making a templated Ebitengine game ..."

# Check there are 2 command line arguments
if [ "$#" -ne 1 ]; then
    echo "Error: folder name required"
    exit
fi

# Get the name of the project from the first command line argument
folderName=$1
echo "Project name: $folderName"

# Check to see if the folder already exists
if [ -d "$folderName" ]; then
    echo "Error: $folderName already exists"
    exit
fi

# Make the folder
echo "Making folder: $folderName"
mkdir $folderName
cd $folderName

# Run go mod
echo "Running go mod init ..."
go mod init github.com/cdclaxton/ebitengine/$folderName

echo "Running go get ..."
go get github.com/hajimehoshi/ebiten/v2

# Create the template
echo "Creating template ..."
cp ../ebitengine-template.go.template main.go

echo "Complete"