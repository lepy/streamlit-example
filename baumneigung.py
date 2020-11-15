import streamlit as st
import plotly.figure_factory as ff
import numpy as np
import pandas as pd
import plotly.express as px

# Add histogram data
rho = 680. # kg/m3
L = 40 #m
R = 0.3 #m
V = 0.3**2 * np.pi * L
Mg = V * rho
Fg = V * rho / 100 # kg -> kN
Fg = 120

def Fs(a, b, Fg):
    return Fg * np.tan(a*np.pi/180.) / np.cos(b*np.pi/180.)

st.write("Berechnung der max. Seilkraft")

st.sidebar.write("Parameter:")
Fg = st.sidebar.slider("Fg [kN] ... Gewichtskraft Baum (100 kg ~ 1 kN)",
                  min_value=0.,
                  max_value=200.,
                  value=(120.),
                  step=1.)

maxFs = st.sidebar.slider("max F_Seil [kN] ... max. Kraft der Seilwinde ",
                  min_value=0.,
                  max_value=100.,
                  value=(18.),
                  step=1.)


alpha = st.sidebar.slider("alpha [°] ... Neigung des Baumes",
                  min_value=0.,
                  max_value=20.,
                  value=(7.),
                  step=1.)

st.sidebar.write("beta [°] ... Neigung des Seils gegenüber der Horizontalen")

bs = np.linspace(0., 70., 100)
Fs_ = Fs(alpha, bs, Fg)

# df = px.data.tips()
# print(df)
df = pd.DataFrame({"beta":bs, "F_Seil":Fs(alpha, bs, Fg)})

fig = px.line(df, x="beta", y="F_Seil",#, color="sex",
                 labels=dict(beta="beta [°]", F_Seil="F_Seil [kN]")
                 )
#
# fig.add_hline(y=18., line_dash="dot", row="all", col="all",
#       annotation_text="max F_Seil",
#       # annotation_position="bottom right"
#       )

fig.add_vrect(x0=bs.min(), x1=bs.max(), y0=0, y1=maxFs, row="all", col=1,
              annotation_text="valid", annotation_position="bottom right",
              fillcolor="green", opacity=0.25, line_width=0)

st.write(r"$F_{Seil} = F_g \frac{\tan{\alpha}}{\cos{\beta}}$")
# Plot!
st.plotly_chart(fig, use_container_width=True)