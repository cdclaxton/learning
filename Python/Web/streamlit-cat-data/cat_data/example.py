import datetime
import os
import streamlit.components.v1 as components
import streamlit as st

_RELEASE = True

if _RELEASE:

    root_dir = os.path.dirname(os.path.abspath(__file__))

    _header = components.declare_component(
        "header", path=os.path.join(root_dir, "header-frontend/build")
    )

    _information = components.declare_component(
        "information", path=os.path.join(root_dir, "information-frontend/build")
    )

    _result = components.declare_component(
        "result", path=os.path.join(root_dir, "result-frontend/build")
    )
else:

    _header = components.declare_component("header", url="http://localhost:3001")

    _information = components.declare_component(
        "information", url="http://localhost:3002"
    )

    _result = components.declare_component("result", url="http://localhost:3003")


def title(title, key=None):
    return _header(title=title)


def information(title, text, key=None):
    return _information(title=title, text=text, key=key)


def result(result_data, key=None):
    return _result(result_data=result_data, key=key)


st.markdown(
    """
    <style>
        .stMainBlockContainer {
            padding-left: 0rem;
            padding-right: 0rem;
            padding-top: 2rem;
            padding-bottom: 0rem;
        }
        .stAppHeader {
            background-color: rgba(255, 255, 255, 0.0);
            visibility: visible;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

title("Cat Data Processing Engine")

information(
    "Information",
    "The Cat Data Processing Engine performs data extraction and standardisation for cat-based datasets.",
)

results = [
    {
        "id": 1,
        "datasetName": "Cats residing in London in 2025",
        "dateUploaded": datetime.datetime.now().isoformat(),
        "numberOfRows": 3000,
        "numberOfRowsWithErrors": 2,
        "numberOfUniqueCats": 2657,
    },
    {
        "id": 2,
        "datasetName": "Ally cat arrests 2016",
        "dateUploaded": (
            datetime.datetime.now() - datetime.timedelta(days=2)
        ).isoformat(),
        "numberOfRows": 250,
        "numberOfRowsWithErrors": 10,
        "numberOfUniqueCats": 134,
    },
]

for idx in range(len(results)):
    result(results[idx], key=f"result-{idx}")
