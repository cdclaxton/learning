# Custom React components in Streamlit

## Setup

```
pip install -r requirements.txt
```

## Running the app

```
python -m streamlit run main.py
```

## Developing the component

```
# Run a server for the components -- this means that changes can be seen immediately
# Ensure _RELEASE is set to False in example.py
cd discrete_slider/frontend
npm install
npm start

# Inside the streamlit-component directory (i.e. root)
streamlit run discrete_slider/example.py
```

## Shipping the component

```
cd discrete_slider/frontend
npm run build

# Then change _RELEASE to True in example.py
```