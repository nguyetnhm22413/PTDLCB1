# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1evpc_APdvUmY4XoB9hBAEK0Ztk5FT263
"""

import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(np.random.randn(20, 5), columns=["a", "b", "c", "d", "e"])
st.line_chart(chart_data)