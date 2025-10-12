# Cat Data Processing Engine in Streamlit using custom React components

## Setup

Create a virtual environment and install the required libraries:

```bash
python -m venv ~/cdpe-venv
source ~/cdpe-venv/bin/activate
pip install -r requirements.txt
```

## Developing the components

A development server is run for each component so that changes made to the React components can be seen immediately :

| Component   | Port |
|-------------|------|
| Header      | 3001 |
| Information | 3002 |
| Result      | 3003 |

* Ensure `_RELEASE = False` in `example.py`.
* Run each of the required servers using different terminals:

```bash
cd cat_data/header-frontend
npm install
npm run start

cd cat_data/information-frontend
npm install
npm run start

cd cat_data/result-frontend
npm install
npm run start
```

Inside the root `streamlit-cat-data` directory run 

```bash
streamlit run cat_data/example.py
```

## Shipping the component

* Run `npm run build` inside each of the components' frontend folders, i.e.

```bash
cd cat_data/header-frontend
npm run build

cd cat_data/information-frontend
npm run build

cd cat_data/result-frontend
npm run build
```

* Set `_RELEASE = True` in `example.py`
* Run the app with `streamlit run cat_data/example.py`