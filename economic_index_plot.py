import pandas as pd
from plotly.offline import plot
import plotly.express as px
index_archive = pd.read_csv('economic_index_adjusted.csv')
fig = px.line(index_archive, x="datetime", y="economic_index", color='economic')
plot(fig, filename='ecnomic_index.html')