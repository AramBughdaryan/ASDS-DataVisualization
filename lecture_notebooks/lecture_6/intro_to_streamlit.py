import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
import time

st.title("This is my first Streamlit app!")
st.header("This is a header")
st.markdown("Stremlit is **_really_ cool**")

# ## displaing dataframes

# dataframe = pd.DataFrame(np.random.randn(5, 10), columns=('col %d' % i for i in range(10)))

# st.write(dataframe)

# # st.data_editor(dataframe)

# ## displaying charts

# # st.line_chart(dataframe)
# # st.area_chart(dataframe)

# # fig = plt.figure(figsize=(10, 5))
# # ax = plt.axes()

# # ax.plot(dataframe)

# # st.pyplot(fig)

# # fig, axes = plt.subplots(1, 2, figsize=(10, 5))
# # axes[0].plot(dataframe["col 0"], )
# # axes[1].bar(range(dataframe.shape[0]), dataframe["col 1"])

# # st.pyplot(fig)


# ## plotly plots
# if st.checkbox("Show plotly plot"):
#     fig = px.line(dataframe)
#     st.plotly_chart(fig)

# plotly_type = st.selectbox("Select plotly plot type", ["line", "bar", "scatter"])

# if plotly_type == "line":
#     fig = px.line(dataframe)
# elif plotly_type == "bar":
#     fig = px.bar(dataframe)
# else:
#     fig = px.scatter(dataframe)

# st.plotly_chart(fig)


# if st.button("show bar plot"):
#     st.bar_chart(dataframe)


# with st.expander("show bar plot"):
#     st.bar_chart(dataframe)

# ## sliders

# # n_points = st.slider("number of points",1,20,5)

# # dataframe = pd.DataFrame(np.random.randn(10, n_points), columns=('col %d' % i for i in range(n_points)))

# # st.write(dataframe)

# # ## input text

# # title = st.text_input("Movie title", "enter a title")
# # if title == "enter a title":
# #     st.write("")
# # else:
# #     st.write(title)

# # title = st.text_input("Movie title", "")
# # st.write(title)

# form = st.form(key="my_form")
# text_input = form.text_input("Movie title")
# text_input2 = form.text_input("Another Movie title")
# submit_button = form.form_submit_button("Submit")
# if submit_button:
#     st.write(text_input)
#     st.write(text_input2)


# @st.cache_data
# def get_data():
#     data = pd.DataFrame(np.random.randn(10, 10), columns=('col %d' % i for i in range(10)))
#     time.sleep(5)
#     return data

# dataframe = get_data()
# st.write(dataframe)
# if st.checkbox("Show plot"):
#     st.line_chart(dataframe)


# image = np.array(Image.open("owl.jpeg"))

# st.image(image)

@st.cache_data
def read_shnik_data():
    data = pd.read_parquet("shnik_2021.parquet")
    return data.head(500_000)


if __name__ == '__main__':
    data = read_shnik_data()
    data_columns = ['Ազգանուն', "Անուն", 'Հայրանուն', 'Մարզ', 'Համայնք', 'Բնակավայր', 'հասցե', 'Ամսի համար', 'Տարի', 'Ամիս', 'Օր']
    data.columns = data_columns
    st.write(data.head(50))

    input_dict = {}
    for el in data_columns:
        input_dict[el] = st.text_input(el, "")

    print(input_dict)
    tmp_data = data.copy()
    for el, value in input_dict.items():
        if value:
            print(el, value)
            tmp_data = tmp_data[tmp_data[el] == value]
    st.write(tmp_data)
    
    st.bar_chart(tmp_data['Մարզ'].value_counts())
    # st.hist(tmp_data['Տարի'].tolist())
    ## dashboard
    ## 1) input field for name, surename, middle name, anything else
    ## 2) submit button
    ## 3) display some interesting statistics and plots based on the inputted name, surename, middle name, anything else