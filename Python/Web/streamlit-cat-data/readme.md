# Cat Data Processing Engine in Streamlit using custom React components

## Setup

Create a virtual environment and install the required libraries:

```
python -m venv ~/cdpe-venv
source ~/cdpe-venv/bin/activate
pip install -r requirements.txt
```

## Developing the components

| Component   | Port |
|-------------|------|
| Header      | 3001 |
| Information | 3002 |
| Result      | 3003 |

```
# Run a server for each of the components -- this means that changes can be seen immediately
# Ensure _RELEASE is set to False in example.py
cd cat_data/header-frontend
npm install
npm run start

# Inside the streamlit-component directory (i.e. root)
streamlit run cat_data/example.py
```

## Shipping the component

Run `npm run build` inside each of the component's frontend folders.