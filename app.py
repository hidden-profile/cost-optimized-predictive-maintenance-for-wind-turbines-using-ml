import streamlit as st
import numpy as np
import pickle

st.set_page_config(
    page_title="ReneWind - Wind Turbine Failure Prediction",
    layout="wide",
    initial_sidebar_state="collapsed"
)

hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

custom_css = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: 
       linear-gradient(rgba(210, 236, 199, 0.7), rgba(236, 246, 216, 0.7)),
       url("https://img.freepik.com/free-vector/realistic-3d-wind-turbines-blue-sky-background_107791-19383.jpg");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
    color: #2f3e1f;
}}

.title-style {{
    font-size: 56px;
    font-weight: 800;
    color: #f0f7e9;
    text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.7);
    text-align: center;
    margin-top: 30px;
    margin-bottom: 10px;
}}

.subtitle-style {{
    font-size: 28px;
    text-align: center;
    color: #f7ffe6;
    margin-bottom: 30px;
}}

.stButton>button {{
    background: linear-gradient(90deg, #00bfa5, #76ff03);
    color: #0d0d0d;
    padding: 14px 32px;
    border-radius: 12px;
    font-size: 20px;
    font-weight: 600;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.4);
    transition: 0.3s;
    border: none;
}}
.stButton>button:hover {{
    background: linear-gradient(90deg, #76ff03, #00bfa5);
    color: #0d0d0d;
}}

.result-box {{
    font-size: 26px;
    text-align: center;
    border-radius: 15px;
    padding: 24px;
    color: #ffffff;
    font-weight: 700;
    box-shadow: 4px 4px 12px rgba(0,0,0,0.5);
}}

.stNumberInput label {{
    color: #006A71;
    font-weight: 600;
    font-size: 15px;
}}

div.stNumberInput input {{
    background-color: #A6D6D6;
    border-radius: 5px;
    padding: 6px;
    color: #015551;
    border: 1px solid #ccc;
}}
input[type=number]::-webkit-inner-spin-button:hover,
input[type=number]::-webkit-outer-spin-button:hover {{
    background-color: #00bfa5 !important;
}}
hr {{
    border: none;
    border-top: 2px solid #94c947;
    margin: 25px 0;
}}

div[data-testid="stMarkdownContainer"] .stMarkdown p {{
    background-color: rgba(255, 255, 255, 0.85);
    padding: 10px;
    border-radius: 10px;
    font-size: 16px;
    color: black;
}}

div[data-testid="stNotificationContentInfo"] {{
    background-color: #e0f7fa !important;
    color: #004d40 !important;
    border-radius: 12px;
    padding: 16px;
    font-size: 16px;
    font-weight: 600;
}}
.info{{
        color:black !important;
        background-color: #77CDFF !important;
        border-radius:10px;
        text-align:center;
         margin-bottom:10px;
    }}
    .info p{{
    padding: 40px;
    }}
@media only screen and (max-width: 768px) {{
    .title-style {{
        font-size: 36px;
        margin-top: 20px;
    }}
    .subtitle-style {{
        font-size: 20px;
    }}
    .stButton>button {{
        padding: 10px 24px;
        font-size: 16px;
    }}
    .result-box {{
        font-size: 20px;
        padding: 16px;
    }}
    .stNumberInput label {{
        font-size: 14px;
    }}
    .info{{
        color:black !important;
        background-color: #77CDFF !important;
        border-radius:10px;
        text-align:center;
        margin-bottom:10px;
    }}
}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown('<div class="title-style">🌱 ReneWind</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-style">Predicting Wind Turbine Failures with Smart AI</div>', unsafe_allow_html=True)

banner_url = "https://as2.ftcdn.net/v2/jpg/10/78/71/59/1000_F_1078715951_GVCR8Ikw8diAQ1vEoPQE8InlluH64lmO.jpg"
st.image(banner_url, use_container_width=True)

try:
    with open("modelx.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("⚠️ Model file not found! Please upload 'modelx.pkl'.")
    st.stop()

st.markdown("### 🧾 Enter Sensor Readings Below")
st.markdown("<hr>", unsafe_allow_html=True)

attribute_names = [
    "Rotor Speed (rpm)", "Wind Speed (m/s)", "Ambient Temperature (°C)", "Humidity (%)",
    "Vibration Sensor 1 (g)", "Vibration Sensor 2 (g)", "Power Output (kW)", "Blade Pitch Angle (°)",
    "Generator Temperature (°C)", "Gearbox Oil Temperature (°C)", "Nacelle Position (°)", "Yaw Angle (°)",
    "Torque (Nm)", "Pressure Sensor 1 (Pa)", "Pressure Sensor 2 (Pa)", "Current Phase A (A)",
    "Current Phase B (A)", "Current Phase C (A)", "Voltage Phase A (V)", "Voltage Phase B (V)",
    "Voltage Phase C (V)", "Active Power (kW)", "Reactive Power (kVAR)", "Apparent Power (kVA)",
    "Power Factor", "Bearing Temperature 1 (°C)", "Bearing Temperature 2 (°C)", "Hydraulic Pressure (bar)",
    "Cooling System Temperature (°C)", "Ambient Pressure (Pa)", "Rotor Blade 1 Angle (°)", "Rotor Blade 2 Angle (°)",
    "Rotor Blade 3 Angle (°)", "Generator Speed (rpm)", "Tower Vibration (mm/s)", "Control System Status",
    "Brake System Status", "Lubrication Oil Level (%)", "Hydraulic Oil Temperature (°C)", "Emergency Stop Status"
]

input_values = []
col1, col2 = st.columns(2)
for i, name in enumerate(attribute_names):
    if i % 2 == 0:
        val = col1.number_input(f"🔹 {name}", value=0.0, format="%.3f")
    else:
        val = col2.number_input(f"🔹 {name}", value=0.0, format="%.3f")
    input_values.append(val)

if st.button("🔍 Predict Failure"):
    input_array = np.array(input_values).reshape(1, -1)
    prediction = model.predict(input_array)[0]

    if prediction == 1:
        st.markdown(
            '<div class="result-box" style="background-color:#f44336;">'
            '❌ Prediction: The Wind Turbine is Likely to FAIL!'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="result-box" style="background-color:#66bb6a;">'
            '✅ Prediction: The Wind Turbine is Operating Normally.'
            '</div>',
            unsafe_allow_html=True
        )

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 🌬️ Did You Know?")
st.markdown('<p class="info">One wind turbine can power over 1,500 homes per year – a fantastic example of sustainable, clean energy!</p>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<center>© 2025 | <strong>Developed by Karri Gayathri</strong> | Final Year Major Project</center>", unsafe_allow_html=True)