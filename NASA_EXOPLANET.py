import streamlit as st
import plotly.graph_objects as go
import numpy as np
import google.generativeai as genai
import random

def add_background_image():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

        body {
            background-image: url('https://images.pexels.com/photos/1341279/pexels-photo-1341279.jpeg');
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            font-family: 'Roboto', sans-serif;
            color: white;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }

        .stApp {
            background-color: rgba(0, 0, 0, 0.7);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0px 0px 15px rgba(255, 255, 255, 0.2);
        }

        .stTextInput > div > input {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            font-weight: bold;
        }

        h1 {
            text-align: center;
            font-weight: 700;
            letter-spacing: 1px;
            text-shadow: 0px 0px 5px rgba(255, 255, 255, 0.8);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

genai.configure(api_key='AIzaSyCNRXcjXGej0mQyqvJWOR6N94wyM9n6wC8')
gemini_model = genai.GenerativeModel('gemini-pro')

def fetch_exoplanet_stats(planet_name):
    query = f"Give me key statistics and the exact visual color (in simple terms like 'light blue', 'red', 'green', 'blue','yellow', 'orange', 'brown' , 'white', 'black', 'cyan', 'gold',) of the exoplanet {planet_name}, with context from NASA."
    response = gemini_model.generate_content(query + " only show statistics points")

    if response and len(response.text) > 0:
        return response.text.strip()
    else:
        return "Statistics not found."

def extract_color(response_text):
    color_map = {
        "dark magenta": (139/255, 0, 139/255),
        "magenta": (255/255, 0, 255/255),
        "red": (1.0, 0.0, 0.0),
        "green": (0.0, 1.0, 0.0),
        "blue": (0.0, 0.0, 1.0),
        "yellow": (1.0, 1.0, 0.0),
        "orange": (1.0, 0.5, 0.0),
        "brown": (0.65, 0.16, 0.16),
        "white": (1.0, 1.0, 1.0),
        "black": (0.0, 0.0, 0.0),
        "light blue": (0.678, 0.847, 0.902),
        "cyan": (64/255, 224/255, 208/255),
        "gold": (255/255, 215/255, 0),
        "silver": (192/255, 192/255, 192/255),
    }

    for color_name, rgb_value in color_map.items():
        if color_name in response_text.lower():
            return rgb_value

    return (1.0, 1.0, 1.0)

def create_exoplanet_visualization(radius, color):
    theta = np.linspace(0, 2 * np.pi, 150)
    phi = np.linspace(0, np.pi, 150)
    theta, phi = np.meshgrid(theta, phi)

    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(phi)

    fig = go.Figure(data=[go.Mesh3d(x=x.flatten(),
                                      y=y.flatten(),
                                      z=z.flatten(),
                                      color=f'rgba({int(color[0]*255)}, {int(color[1]*255)}, {int(color[2]*255)}, 0.7)',
                                      opacity=0.7,
                                      lighting=dict(ambient=0.3, diffuse=1, specular=0.9, roughness=0.4),
                                      lightposition=dict(x=100, y=200, z=0))])

    fig.update_layout(scene=dict(
        xaxis=dict(nticks=4, range=[-radius*2, radius*2], backgroundcolor='rgba(0, 0, 0, 0)'),
        yaxis=dict(nticks=4, range=[-radius*2, radius*2], backgroundcolor='rgba(0, 0, 0, 0)'),
        zaxis=dict(nticks=4, range=[-radius*2, radius*2], backgroundcolor='rgba(0, 0, 0, 0)')),
        width=350,
        height=350,
        margin=dict(r=0, l=0, b=0, t=0),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)')

    return fig

def create_trend_graphs(planet_name):

    time = np.arange(0, 10, 1)
    density = np.random.rand(len(time)) * 100 + 200 
    atmospheric_levels = np.random.rand(len(time)) * 100

    density_fig = go.Figure()
    density_fig.add_trace(go.Scatter(x=time, y=density, mode='lines+markers', name='Density (kg/m³)', line=dict(color='green')))
    density_fig.update_layout(title="Density Trend Over Time", xaxis_title="Time (Hours)", yaxis_title="Density (kg/m³)", showlegend=True)

    atmospheric_fig = go.Figure()
    atmospheric_fig.add_trace(go.Scatter(x=time, y=atmospheric_levels, mode='lines+markers', name='Atmospheric Level', line=dict(color='blue')))
    atmospheric_fig.update_layout(title="Atmospheric Level Trend Over Time", xaxis_title="Time (Hours)", yaxis_title="Atmospheric Level (arbitrary units)", showlegend=True)

    return density_fig, atmospheric_fig

st.title("S L E E P Y")

add_background_image()

planet_name = st.text_input("Search for an exoplanet:", "")

num_stars = 15
star_positions = [(random.uniform(0, 1), random.uniform(0, 1), random.choice(["Proxima b", "Kepler-20e", "TRAPPIST-1d", "HD 189733b", "WASP-121b", "WASP-33b", "K2-18b", "55 Cancri e", "LHS 1140 b", "GJ 357 d", "K2-72e", "WASP-103b", "WASP-76b", "WASP-121b", "K2-135b"])) for _ in range(num_stars)]

star_fig = go.Figure()

for x, y, star_name in star_positions:
    star_x = x * 100
    star_y = y * 100
    star_fig.add_trace(go.Scatter(
        x=[star_x],
        y=[star_y],
        mode='markers+text',
        marker=dict(size=12, color='rgba(255, 255, 255, 0.8)', opacity=0.7, line=dict(width=2, color='white')),
        text=[star_name],
        textposition="top center",
        hoverinfo='text',
        name=star_name
    ))

star_fig.update_layout(
    title="Random Stars",
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    showlegend=False,
    width=700,
    height=400,
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor='rgba(0, 0, 0, 0)',
    plot_bgcolor='rgba(0, 0, 0, 0)',
)

if planet_name:
    st.write(f"Exploring: **{planet_name}**")

    col1, col2 = st.columns(2)

    with col1:
        exoplanet_stats = fetch_exoplanet_stats(planet_name)
        st.write("### Exoplanet Statistics")
        st.write(exoplanet_stats)

    with col2:
        color = extract_color(exoplanet_stats)
        radius = 10
        fig = create_exoplanet_visualization(radius, color)
        st.plotly_chart(fig, use_container_width=True)

    temperature_fig, atmospheric_fig = create_trend_graphs(planet_name)

    st.write("### Density Trend Graph")
    st.plotly_chart(temperature_fig, use_container_width=True)

    st.write("### Atmospheric Level Trend Graph")
    st.plotly_chart(atmospheric_fig, use_container_width=True)

st.write("### Star Field")
st.plotly_chart(star_fig, use_container_width=True)