import time
from collections import defaultdict

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Level Product Analytics",
    layout="wide",
)


def get_data(path):
    path[0].seek(0)
    df = pd.read_csv(path[0]).dropna(axis=0, inplace=False)
    return df


def get_df_column_datatype(df):
    columns = df.columns
    columns_type = {}
    for column in columns:
        try:
            df[column] = pd.to_numeric(df[column])
            column_type = "numeric"
            if len(np.unique(df[column])) < 30:
                column_type = "category"
        except:
            if len(np.unique(df[column])) < 30:
                column_type = "category"
            else:
                column_type = "string"
        columns_type[column] = column_type
    return df, columns_type


def filter_df(df):
    for column in df.columns:
        if df_column_datatype[column] == "numeric":
            df = df[(filters[column][0] <= df[column]) & (df[column] <= filters[column][1])]
        elif df_column_datatype[column] == "category":
            df = df[(df[column].isin(filters[column]))]
    return df


def set_plotmaker():
    st.empty()
    try:
        plotType = st.radio("Plot Type", ("Histogram", "Scatter", "Box", "Matrix"))
        st.text(f"{plotType} Plot Setting")
        if plotType == "Histogram":
            x = st.selectbox("X Data", columns_per_category['numeric'] + columns_per_category['category'], key="Histogram_X")
            y = st.slider("Bins", 5, 100, 10, key="Histogram_Bins")
        elif plotType == "Scatter":
            x = st.selectbox("X Data", columns_per_category['numeric'] + columns_per_category['category'], key="Scatter_X")
            y = st.selectbox("Y Data", columns_per_category['numeric'] + columns_per_category['category'] + ["Count"], key="Scatter_Y")
        elif plotType == "Box":
            x = st.selectbox("X Data", columns_per_category['category'], key="Box_X")
            y = st.selectbox("Y Data", columns_per_category['numeric'], key="Box_Y")
        else:
            x_col1, x_col2 = st.columns(2)
            with x_col1:
                x1 = st.selectbox("X1 Data", columns_per_category['numeric'], key="Maxrix_X1")
            with x_col2:
                x2 = st.selectbox("X2 Data", columns_per_category['numeric'], key="Matrix_X2")
            x = (x1, x2)
            y = st.selectbox("Y Data", columns_per_category['numeric'] + columns_per_category['category'], key="Scatter_Y")
        return plotType, x, y
    except Exception as e:
        print(e)
        pass


def get_heatmap_df(df1, df2):
    df1_min = np.nanmin(df1)
    df1_max = np.nanmax(df1)
    df2_min = np.nanmin(df2)
    df2_max = np.nanmax(df2)
    x1ticks = np.linspace(df1_min, df1_max, 10)
    x2ticks = np.linspace(df2_min, df2_max, 10)
    heatmap = pd.DataFrame(data=np.random.random((10, 10)), index=x2ticks, columns=x1ticks)
    return heatmap


def run_plotmaker(df, plotxy):
    if plotxy is not None:
        plot, x, y = plotxy
        print(plot)
        if plot == "Histogram":
            print(2)
            x, xlabel = df[x], x
            fig, ax = plt.subplots(figsize=(13, 6.5))
            ax.set_xlabel(xlabel)
            ax.set_ylabel("count")
            print(y)
            ax.hist(x, bins=y)
            ax.grid()
            ax.set_title(f"{xlabel}")
            st.pyplot(fig)

        elif plot == "Scatter":
            x, xlabel = df[x], x
            y, ylabel = df[y], y
            fig, ax = plt.subplots(figsize=(13, 6.5))
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.scatter(x, y)
            ax.grid()
            ax.set_title(f"{ylabel} / {xlabel}")
            st.pyplot(fig)

        elif plot == "Box":
            x, xlabel = df[x], x
            y, ylabel = df[y], y
            fig, ax = plt.subplots(figsize=(13, 6.5))
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            boxdatas = []
            xticks = sorted(x.unique())
            for xx in xticks:
                boxdata = np.array(y[x == xx])
                boxdatas.append(boxdata[~np.isnan(pd.to_numeric(boxdata, errors='coerce'))])
            ax.boxplot(boxdatas)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.set_xticks(list(range(1, len(xticks) + 1)), xticks)
            ax.set_title(f"{ylabel} / {xlabel}")
            st.pyplot(fig)

        elif plot == "Matrix":
            x1, xlabel1 = df[x[0]], x[0]
            x2, xlabel2 = df[x[1]], x[1]
            y, ylabel = df[y], y
            fig1_col, fig2_col = st.columns(2)

            size = 31
            x1ticks = np.linspace(np.nanmin(x1), np.nanmax(x1), size)
            x2ticks = np.linspace(np.nanmin(x2), np.nanmax(x2), size)
            x1space = x1ticks[1] - x1ticks[0]
            x2space = x2ticks[1] - x2ticks[0]
            realx1ticks = np.round(np.linspace(np.nanmin(x1), np.nanmax(x1), 7), 1)
            realx2ticks = np.round(np.linspace(np.nanmin(x2), np.nanmax(x2), 7), 1)

            number_heatmap_df = pd.DataFrame(data=np.zeros((size - 1, size - 1)), index=x2ticks[:-1],
                                             columns=x1ticks[:-1])
            value_heatmap_df = pd.DataFrame(data=np.zeros((size - 1, size - 1)), index=x2ticks[:-1],
                                            columns=x1ticks[:-1])
            for x1tick in x1ticks[:-1]:
                for x2tick in x2ticks[:-1]:
                    number_heatmap_df[x1tick][x2tick] = np.sum((x1 >= x1tick) & (x1 < x1tick + x1space) &
                                                               (x2 >= x2tick) & (x2 < x2tick + x2space))
                    value_heatmap_df[x1tick][x2tick] = np.average(y[(x1 >= x1tick) & (x1 < x1tick + x1space) &
                                                                    (x2 >= x2tick) & (x2 < x2tick + x2space)])

            with fig1_col:
                fig1, ax1 = plt.subplots(figsize=(5, 6.5))
                fig11 = ax1.pcolor(number_heatmap_df, cmap="Blues", vmin=0)
                fig1.colorbar(fig11, orientation="horizontal", pad=0.15, label='number')
                ax1.set_xlabel(xlabel1)
                ax1.set_ylabel(xlabel2)
                ax1.set_xticklabels(realx1ticks)
                ax1.set_yticklabels(realx2ticks)
                ax1.set_title(f"number / \n{xlabel1} + {xlabel2}")
                st.pyplot(fig1)

            with fig2_col:
                fig2, ax2 = plt.subplots(figsize=(5, 6.5))
                fig22 = ax2.pcolor(value_heatmap_df, cmap="Blues", vmin=0)
                fig2.colorbar(fig22, orientation="horizontal", pad=0.15, label=ylabel)
                ax2.set_xlabel(xlabel1)
                ax2.set_ylabel(xlabel2)
                ax2.set_xticklabels(realx1ticks)
                ax2.set_yticklabels(realx2ticks)
                ax2.set_title(f"{ylabel} / \n{xlabel1} + {xlabel2}")
                st.pyplot(fig2)

title_col, setting_col = st.columns(2)

with title_col:
    st.title("ease EDA")

with setting_col:
    _, _, setting_col2 = st.columns(3)
    with setting_col2:
        st.text("⠀")
        with st.expander("Draw Setting"):
            draw_custom_plot = st.checkbox("custom plot", True)
            draw_full_table = st.checkbox("Full table", True)

file = st.file_uploader('File Uploader:', accept_multiple_files=True)
if len(file) > 0:
    df = get_data(file)
    df, df_column_datatype = get_df_column_datatype(df)
    columns_per_category = defaultdict(list, {})
    for column in df.columns:
        columns_per_category[df_column_datatype[column]].append(column)

    # filters
    filters = {}
    with st.expander("Search Filter"):
        for column in df.columns:
            if df_column_datatype[column] == "numeric":
                filters[column] = st.slider(column, min(df[column]), max(df[column]), (min(df[column]), max(df[column])), key=column)
            elif df_column_datatype[column] == "category":
                filters[column] = st.multiselect(column, pd.unique(df[column]), default=pd.unique(df[column]), key=column)

    # creating a single-element container
    placeholder = st.empty()

    with placeholder.container():
        if len(file) > 0:
            df = get_data(file)
            df = filter_df(df)

            if draw_custom_plot:
                plotxy = set_plotmaker()
                run_plotmaker(df, plotxy)

            if draw_full_table:
                st.markdown("### Full Data")
                st.dataframe(df)
            time.sleep(1)
