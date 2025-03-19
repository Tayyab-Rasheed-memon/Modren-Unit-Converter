# unit_converter.py
import streamlit as st
import pandas as pd
import time
import base64

# Set page configuration
st.set_page_config(page_title="Animated Unit Converter", layout="wide")

# Custom CSS with animations
st.markdown(f"""
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

:root {{
    --primary: #6366f1;
    --secondary: #8b5cf6;
    --accent: #ec4899;
}}

body {{
    background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
    font-family: 'Inter', sans-serif;
    color: #0f172a;
}}

.developer-card {{
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 2rem;
    margin: 1.5rem;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    animation: float 3s ease-in-out infinite;
}}

@keyframes float {{
    0% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-10px); }}
    100% {{ transform: translateY(0px); }}
}}

.profile-img {{
    width: 150px;
    height: 150px;
    border-radius: 50%;
    margin: 0 auto 1.5rem;
    border: 3px solid #6366f1;
    animation: border-pulse 2s infinite;
}}

@keyframes border-pulse {{
    0% {{ border-color: #6366f1; }}
    50% {{ border-color: #8b5cf6; }}
    100% {{ border-color: #6366f1; }}
}}

.result-card {{
    background: rgba(255, 255, 255, 0.9);
    border-radius: 15px;
    padding: 2rem;
    margin: 1rem 0;
    animation: slideInRight 0.5s ease-out;
}}

@keyframes slideInRight {{
    0% {{ transform: translateX(100px); opacity: 0; }}
    100% {{ transform: translateX(0); opacity: 1; }}
}}

.stButton>button {{
    transition: all 0.3s ease !important;
    animation: button-glow 1.5s infinite;
}}

@keyframes button-glow {{
    0% {{ box-shadow: 0 0 5px #6366f155; }}
    50% {{ box-shadow: 0 0 15px #6366f1aa; }}
    100% {{ box-shadow: 0 0 5px #6366f155; }}
}}
</style>
""", unsafe_allow_html=True)

def img_to_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.sidebar.warning(f"Image not found: {str(e)}")
        return None

def developer_profile():
    base64_img = img_to_base64("github_dp_oval.png")
    img_src = "https://via.placeholder.com/150/6366f1/ffffff?text=IT"
    if base64_img:
        img_src = f"data:image/png;base64,{base64_img}"
    
    st.sidebar.markdown(f"""
    <div class="developer-card">
        <div style="text-align: center;">
            <img src="{img_src}" class="profile-img">
            <h3 style="color: #1e293b; margin-bottom: 0.5rem;">Ibrahim Tayyab</h3>
            <p style="color: #475569; margin-bottom: 1rem;">(Tayyab.R)</p>
            <div style="color: #6366f1; font-size: 1.2rem;">
                <i class="fas fa-calculator"></i> Unit Conversion Expert
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "category" not in st.session_state:
    st.session_state.category = "Length"
if "from_unit" not in st.session_state:
    st.session_state.from_unit = "Meter"
if "to_unit" not in st.session_state:
    st.session_state.to_unit = "Centimeter"

# Conversion factors
CONVERSION_FACTORS = {
    "Length": {
        "Meter": 1,
        "Centimeter": 100,
        "Kilometer": 0.001,
        "Inch": 39.3701,
        "Foot": 3.28084
    },
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Weight": {
        "Kilogram": 1,
        "Gram": 1000,
        "Pound": 2.20462,
        "Ounce": 35.274
    }
}

def convert_units(value, from_unit, to_unit, category):
    try:
        if from_unit == to_unit:
            return value, "No conversion needed"
            
        if category == "Temperature":
            converters = {
                ("Celsius", "Fahrenheit"): lambda x: (x * 9/5) + 32,
                ("Fahrenheit", "Celsius"): lambda x: (x - 32) * 5/9,
                ("Celsius", "Kelvin"): lambda x: x + 273.15,
                ("Kelvin", "Celsius"): lambda x: x - 273.15,
                ("Fahrenheit", "Kelvin"): lambda x: (x - 32) * 5/9 + 273.15,
                ("Kelvin", "Fahrenheit"): lambda x: (x - 273.15) * 9/5 + 32
            }
            return converters[(from_unit, to_unit)](value), "Converted"
        else:
            factor = (CONVERSION_FACTORS[category][to_unit] 
                     / CONVERSION_FACTORS[category][from_unit])
            return value * factor, f"{value} × {factor:.4f}"
    except Exception as e:
        return None, str(e)

# Main app
developer_profile()
st.title("✨ Modren Unit Converter")

# Category selection
st.session_state.category = st.sidebar.selectbox(
    "Category", 
    list(CONVERSION_FACTORS.keys()), 
    key="category_select"
)

# Get available units for current category
units = list(CONVERSION_FACTORS[st.session_state.category].keys() 
           if st.session_state.category != "Temperature" 
           else CONVERSION_FACTORS[st.session_state.category])

# Validate current units
if st.session_state.from_unit not in units:
    st.session_state.from_unit = units[0]
if st.session_state.to_unit not in units:
    st.session_state.to_unit = units[0]

# Conversion UI
col1, col2, col3 = st.columns([3, 1, 3])
with col1:
    from_unit = st.selectbox(
        "From", 
        units, 
        index=units.index(st.session_state.from_unit),
        key="from_unit_select"
    )

with col2:
    st.markdown("<div style='height: 100px; display: flex; align-items: center; justify-content: center;'>➔</div>", 
              unsafe_allow_html=True)
    if st.button("🔄 Swap Units"):
        st.session_state.from_unit, st.session_state.to_unit = st.session_state.to_unit, st.session_state.from_unit
        st.rerun()  # Corrected line

with col3:
    to_unit = st.selectbox(
        "To", 
        units, 
        index=units.index(st.session_state.to_unit),
        key="to_unit_select"
    )
    value = st.number_input("Value", value=1.0, min_value=0.0, step=0.1)

# Update session state
st.session_state.from_unit = from_unit
st.session_state.to_unit = to_unit

# Conversion
if st.button("Convert", type="primary"):
    with st.spinner("Converting..."):
        time.sleep(0.5)
        converted, formula = convert_units(value, from_unit, to_unit, st.session_state.category)
        if converted is not None:
            result = f"{value} {from_unit} = {converted:.4f} {to_unit}"
            st.session_state.history.append(result)
            st.markdown(f"""
            <div class="result-card">
                <h3 style="color: #1e293b;">{result}</h3>
                <p style="color: #475569;">Formula: {formula}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"Error: {formula}")

# History
with st.expander("📜 Conversion History"):
    for entry in reversed(st.session_state.history):
        st.markdown(f"<div style='padding: 1rem; margin: 0.5rem 0; background: rgba(241, 245, 249, 0.5); border-radius: 8px;'>{entry}</div>", 
                  unsafe_allow_html=True)
    if st.button("Clear History"):
        st.session_state.history = []# # unit_converter.py
# import streamlit as st
# import pandas as pd
# import base64
# import time

# # Set page configuration
# st.set_page_config(page_title="Animated Unit Converter", layout="wide")

# # Custom CSS with unique animations
# st.markdown(f"""
# <style>
# @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

# body {{
#     background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
#     font-family: 'Inter', sans-serif;
#     color: #0f172a;
# }}

# .developer-card {{
#     background: rgba(255, 255, 255, 0.95);
#     border-radius: 20px;
#     padding: 2rem;
#     margin: 1.5rem;
#     box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
#     animation: float 3s ease-in-out infinite;
# }}

# @keyframes float {{
#     0% {{ transform: translateY(0px); }}
#     50% {{ transform: translateY(-10px); }}
#     100% {{ transform: translateY(0px); }}
# }}

# .profile-img {{
#     width: 150px;
#     height: 150px;
#     border-radius: 50%;
#     margin: 0 auto 1.5rem;
#     border: 3px solid #6366f1;
#     animation: border-pulse 2s infinite;
# }}

# @keyframes border-pulse {{
#     0% {{ border-color: #6366f1; }}
#     50% {{ border-color: #8b5cf6; }}
#     100% {{ border-color: #6366f1; }}
# }}

# .result-card {{
#     background: rgba(255, 255, 255, 0.9);
#     border-radius: 15px;
#     padding: 2rem;
#     margin: 1rem 0;
#     animation: slideInRight 0.5s ease-out;
# }}

# @keyframes slideInRight {{
#     0% {{ transform: translateX(100px); opacity: 0; }}
#     100% {{ transform: translateX(0); opacity: 1; }}
# }}

# .stButton>button {{
#     transition: all 0.3s ease !important;
#     animation: button-glow 1.5s infinite;
# }}

# @keyframes button-glow {{
#     0% {{ box-shadow: 0 0 5px #6366f155; }}
#     50% {{ box-shadow: 0 0 15px #6366f1aa; }}
#     100% {{ box-shadow: 0 0 5px #6366f155; }}
# }}
# </style>
# """, unsafe_allow_html=True)

# def img_to_base64(image_path):
#     try:
#         with open(image_path, "rb") as img_file:
#             return base64.b64encode(img_file.read()).decode()
#     except Exception as e:
#         st.sidebar.warning(f"Image not found: {str(e)}")
#         return None

# def developer_profile():
#     base64_img = img_to_base64("github_dp_oval.png")
#     img_src = "https://via.placeholder.com/150/6366f1/ffffff?text=IT"  # Default image
#     if base64_img:
#         img_src = f"data:image/png;base64,{base64_img}"
    
#     st.sidebar.markdown(f"""
#     <div class="developer-card">
#         <div style="text-align: center;">
#             <img src="{img_src}" class="profile-img">
#             <h3 style="color: #1e293b; margin-bottom: 0.5rem;">Ibrahim Tayyab</h3>
#             <p style="color: #475569; margin-bottom: 1rem;">(Tayyab.R)</p>
#             <div style="color: #6366f1; font-size: 1.2rem;">
#                 <i class="fas fa-calculator"></i> Unit Conversion Expert
#             </div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# # Initialize session state
# if "history" not in st.session_state:
#     st.session_state.history = []
# if "from_unit" not in st.session_state:
#     st.session_state.from_unit = "Meter"
# if "to_unit" not in st.session_state:
#     st.session_state.to_unit = "Centimeter"

# # Conversion factors
# CONVERSION_FACTORS = {
#     "Length": {
#         "Meter": 1,
#         "Centimeter": 100,
#         "Kilometer": 0.001,
#         "Inch": 39.3701,
#         "Foot": 3.28084
#     },
#     "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
#     "Weight": {
#         "Kilogram": 1,
#         "Gram": 1000,
#         "Pound": 2.20462,
#         "Ounce": 35.274
#     }
# }

# # Conversion functions
# def celsius_to_fahrenheit(c): return (c * 9/5) + 32
# def fahrenheit_to_celsius(f): return (f - 32) * 5/9
# def celsius_to_kelvin(c): return c + 273.15
# def kelvin_to_celsius(k): return k - 273.15

# def convert_value(value, from_unit, to_unit, category):
#     try:
#         if category == "Temperature":
#             converters = {
#                 ("Celsius", "Fahrenheit"): celsius_to_fahrenheit,
#                 ("Fahrenheit", "Celsius"): fahrenheit_to_celsius,
#                 ("Celsius", "Kelvin"): celsius_to_kelvin,
#                 ("Kelvin", "Celsius"): kelvin_to_celsius
#             }
#             return converters[(from_unit, to_unit)](value), "Converted"
#         else:
#             factor = CONVERSION_FACTORS[category][to_unit] / CONVERSION_FACTORS[category][from_unit]
#             return value * factor, f"{value} × {factor:.4f}"
#     except Exception as e:
#         return None, str(e)

# # Main app
# developer_profile()
# st.title("✨ Animated Unit Converter")

# # Conversion UI
# col1, col2, col3 = st.columns([3, 1, 3])
# with col1:
#     category = st.selectbox("Category", list(CONVERSION_FACTORS.keys()))
#     units = list(CONVERSION_FACTORS[category].keys() 
#                 if category != "Temperature" 
#                 else CONVERSION_FACTORS[category])
#     from_unit = st.selectbox("From", units, key="from_unit")

# with col2:
#     st.markdown("<div style='height: 100px; display: flex; align-items: center; justify-content: center;'>➔</div>", 
#               unsafe_allow_html=True)
#     if st.button("🔄 Swap Units"):
#         st.session_state.from_unit, st.session_state.to_unit = st.session_state.to_unit, st.session_state.from_unit
#         st.rerun()

# with col3:
#     to_unit = st.selectbox("To", units, key="to_unit")
#     value = st.number_input("Value", value=1.0, min_value=0.0, step=0.1)

# # Conversion
# if st.button("Convert", type="primary"):
#     with st.spinner("Converting..."):
#         time.sleep(0.5)
#         converted, formula = convert_value(value, from_unit, to_unit, category)
#         if converted is not None:
#             result = f"{value} {from_unit} = {converted:.4f} {to_unit}"
#             st.session_state.history.append(result)
#             st.markdown(f"""
#             <div class="result-card">
#                 <h3 style="color: #1e293b;">{result}</h3>
#                 <p style="color: #475569;">Formula: {formula}</p>
#             </div>
#             """, unsafe_allow_html=True)
#         else:
#             st.error(f"Error: {formula}")

# # History
# with st.expander("📜 Conversion History"):
#     for entry in reversed(st.session_state.history):
#         st.markdown(f"<div style='padding: 1rem; margin: 0.5rem 0; background: rgba(241, 245, 249, 0.5); border-radius: 8px;'>{entry}</div>", 
#                   unsafe_allow_html=True)
#     if st.button("Clear History"):
#         st.session_state.history = []












# # unit_converter.py
# import streamlit as st
# import pandas as pd
# import base64
# import json

# # Set page configuration
# st.set_page_config(page_title="Modern Unit Converter", layout="wide")

# # Custom CSS with error handling
# st.markdown("""
# <style>
# @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

# body {
#     background: linear-gradient(135deg, #a1c4fd, #d4fc79);
#     font-family: 'Inter', sans-serif;
#     color: #333;
# }
# .developer-card {
#     background: rgba(255, 255, 255, 0.9);
#     border-radius: 15px;
#     padding: 20px;
#     margin: 10px;
#     box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
# }
# .developer-text {
#     font-size: 1.2em;
#     color: #2c3e50;
#     margin-top: 10px;
#     text-align: center;
# }
# .dark-theme {
#     background: linear-gradient(135deg, #2c3e50, #4ca1af);
#     color: #fff;
# }
# .stButton>button {
#     background: linear-gradient(90deg, #6b7280, #9ca3af);
#     color: white;
#     border-radius: 12px;
# }
# .result-card {
#     background: rgba(255, 255, 255, 0.8);
#     border-radius: 20px;
#     padding: 25px;
#     margin-top: 20px;
# }
# </style>
# """, unsafe_allow_html=True)

# def img_to_base64(image_path):
#     try:
#         with open(image_path, "rb") as img_file:
#             return base64.b64encode(img_file.read()).decode()
#     except Exception as e:
#         st.sidebar.warning(f"Image not found: {str(e)}")
#         return None

# def developer_profile():
#     base64_img = img_to_base64("profile.jpg")
#     img_src = "https://via.placeholder.com/150"  # Default image
#     if base64_img:
#         img_src = f"data:image/png;base64,{base64_img}"
    
#     st.sidebar.markdown(f"""
#     <div class="developer-card">
#         <div style="text-align: center;">
#             <img src="{img_src}" width="100" style="border-radius: 50%; margin-bottom: 15px;">
#             <div class="developer-text">
#                 <h3>Ibrahim Tayyab</h3>
#                 <p>(Tayyab.R)</p>
#                 <p>Unit Converter Specialist</p>
#             </div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# # Initialize session state
# if "history" not in st.session_state:
#     st.session_state.history = []
# if "from_unit" not in st.session_state:
#     st.session_state.from_unit = "Meter"
# if "to_unit" not in st.session_state:
#     st.session_state.to_unit = "Centimeter"
# if "dark_mode" not in st.session_state:
#     st.session_state.dark_mode = False

# # Conversion factors (same as previous)
# CONVERSION_FACTORS = {
#     "Length": {"Meter": 1, "Centimeter": 100, "Kilometer": 0.001, "Inch": 39.3701, "Foot": 3.28084},
#     "Area": {"Square Meter": 1, "Square Kilometer": 0.000001, "Square Foot": 10.7639, "Acre": 0.000247105},
#     "Volume": {"Cubic Meter": 1, "Liter": 1000, "Gallon (US)": 264.172, "Cubic Foot": 35.3147},
#     "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
#     "Data Transfer Rate": {"Bit per second": 1, "Kilobit per second": 0.001, "Megabit per second": 0.000001, "Gigabit per second": 1e-9},
#     "Digital Storage": {"Byte": 1, "Kilobyte": 0.001, "Megabyte": 1e-6, "Gigabyte": 1e-9},
#     "Energy": {"Joule": 1, "Kilojoule": 0.001, "Calorie": 0.239006, "Kilowatt-hour": 2.77778e-7},
#     "Frequency": {"Hertz": 1, "Kilohertz": 0.001, "Megahertz": 1e-6, "Gigahertz": 1e-9},
#     "Fuel Economy": {"Miles per gallon": 1, "Kilometers per liter": 0.425144, "Liters per 100 km": 235.215},
#     "Mass": {"Kilogram": 1, "Gram": 1000, "Pound": 2.20462, "Ounce": 35.274},
#     "Plane Angle": {"Degree": 1, "Radian": 0.0174533, "Gradian": 1.11111},
#     "Pressure": {"Pascal": 1, "Kilopascal": 0.001, "Bar": 1e-5, "PSI": 0.000145038},
#     "Speed": {"Meter per second": 1, "Kilometer per hour": 3.6, "Mile per hour": 2.23694, "Knot": 1.94384},
#     "Time": {"Second": 1, "Minute": 0.0166667, "Hour": 0.000277778, "Day": 1.15741e-5}
# }

# # Temperature conversion functions
# def celsius_to_fahrenheit(c): return (c * 9/5) + 32
# def fahrenheit_to_celsius(f): return (f - 32) * 5/9
# def celsius_to_kelvin(c): return c + 273.15
# def kelvin_to_celsius(k): return k - 273.15

# def convert_value(value, from_unit, to_unit, category):
#     factors = CONVERSION_FACTORS[category]
#     if category == "Temperature":
#         converters = {
#             ("Celsius", "Fahrenheit"): celsius_to_fahrenheit,
#             ("Fahrenheit", "Celsius"): fahrenheit_to_celsius,
#             ("Celsius", "Kelvin"): celsius_to_kelvin,
#             ("Kelvin", "Celsius"): kelvin_to_celsius,
#             ("Fahrenheit", "Kelvin"): lambda f: celsius_to_kelvin(fahrenheit_to_celsius(f)),
#             ("Kelvin", "Fahrenheit"): lambda k: celsius_to_fahrenheit(kelvin_to_celsius(k))
#         }
#         return converters.get((from_unit, to_unit), lambda x: x)(value), "Converted"
#     else:
#         base_value = value / factors[from_unit]
#         return base_value * factors[to_unit], f"{value} {from_unit} × ({factors[to_unit]}/{factors[from_unit]})"

# # UI Components
# developer_profile()
# st.title("Modern Unit Converter")

# # Category selection
# category = st.sidebar.selectbox("Category", list(CONVERSION_FACTORS.keys()))
# units = list(CONVERSION_FACTORS[category].keys()) if isinstance(CONVERSION_FACTORS[category], dict) else CONVERSION_FACTORS[category]

# # Conversion UI
# col1, col2, col3 = st.columns([3, 1, 3])
# with col1:
#     st.session_state.from_unit = st.selectbox("From", units, index=units.index(st.session_state.from_unit) if st.session_state.from_unit in units else 0)
# with col2:
#     if st.button("↔ Swap"):
#         st.session_state.from_unit, st.session_state.to_unit = st.session_state.to_unit, st.session_state.from_unit
#         st.rerun()
# with col3:
#     st.session_state.to_unit = st.selectbox("To", units, index=units.index(st.session_state.to_unit) if st.session_state.to_unit in units else 0)

# value = st.number_input("Value", value=1.0)

# if st.button("Convert"):
#     try:
#         converted, formula = convert_value(value, st.session_state.from_unit, st.session_state.to_unit, category)
#         result = f"{value} {st.session_state.from_unit} = {converted:.4f} {st.session_state.to_unit}"
#         st.session_state.history.append(result)
#         st.markdown(f"""
#         <div class="result-card">
#             <h3>{result}</h3>
#             <p>Formula: {formula}</p>
#         </div>
#         """, unsafe_allow_html=True)
#     except Exception as e:
#         st.error(f"Error: {str(e)}")

# # History and Theme
# st.sidebar.header("Conversion History")
# for entry in reversed(st.session_state.history[-5:]):
#     st.sidebar.write(entry)
# if st.sidebar.button("Clear History"):
#     st.session_state.history = []

# if st.sidebar.button("Toggle Dark Mode"):
#     st.session_state.dark_mode = not st.session_state.dark_mode
#     st.markdown("<script>document.body.classList.toggle('dark-theme')</script>", unsafe_allow_html=True)

































































































































































# # unit_converter.py
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import json
# import base64
# from PIL import Image

# # Set page configuration
# st.set_page_config(page_title="Modern Unit Converter", layout="wide")

# # Custom CSS with developer credit
# st.markdown(f"""
# <style>
# @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

# body {{
#     background: linear-gradient(135deg, #a1c4fd, #d4fc79);
#     font-family: 'Inter', sans-serif;
#     color: #333;
# }}
# .developer-card {{
#     background: rgba(255, 255, 255, 0.9) !important;
#     border-radius: 15px;
#     padding: 20px;
#     margin: 10px;
#     box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
# }}
# .developer-text {{
#     font-size: 1.2em;
#     color: #2c3e50;
#     margin-top: 10px;
#     text-align: center;
# }}
# .dark-theme {{
#     background: linear-gradient(135deg, #2c3e50, #4ca1af) !important;
#     color: #fff !important;
# }}
# .stButton>button {{
#     background: linear-gradient(90deg, #6b7280, #9ca3af);
#     color: white;
#     border-radius: 12px;
# }}
# .result-card {{
#     background: rgba(255, 255, 255, 0.8);
#     border-radius: 20px;
#     padding: 25px;
#     margin-top: 20px;
# }}
# </style>
# """, unsafe_allow_html=True)

# # Image to base64 converter
# def img_to_base64(image_path):
#     with open(image_path, "rb") as img_file:
#         return base64.b64encode(img_file.read()).decode()

# # Developer profile section
# def developer_profile():
#     # Replace 'profile.jpg' with your actual image file
#     img_path = "profile.jpg"
#     base64_img = img_to_base64(img_path)
    
#     st.sidebar.markdown(f"""
#     <div class="developer-card">
#         <div style="text-align: center;">
#             <img src="data:image/png;base64,{base64_img}" width="100" style="border-radius: 50%; margin-bottom: 15px;">
#             <div class="developer-text">
#                 <h3>Ibrahim Tayyab</h3>
#                 <p>(Tayyab.R)</p>
#                 <p>Unit Converter Specialist</p>
#             </div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# # Initialize session state
# if "history" not in st.session_state:
#     st.session_state.history = []
# if "from_unit" not in st.session_state:
#     st.session_state.from_unit = "Meter"
# if "to_unit" not in st.session_state:
#     st.session_state.to_unit = "Centimeter"
# if "dark_mode" not in st.session_state:
#     st.session_state.dark_mode = False

# # Conversion factors for all categories
# CONVERSION_FACTORS = {
#     "Length": {
#         "Meter": 1,
#         "Centimeter": 100,
#         "Kilometer": 0.001,
#         "Inch": 39.3701,
#         "Foot": 3.28084
#     },
#     "Area": {
#         "Square Meter": 1,
#         "Square Kilometer": 0.000001,
#         "Square Foot": 10.7639,
#         "Acre": 0.000247105
#     },
#     "Volume": {
#         "Cubic Meter": 1,
#         "Liter": 1000,
#         "Gallon (US)": 264.172,
#         "Cubic Foot": 35.3147
#     },
#     "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
#     "Data Transfer Rate": {
#         "Bit per second": 1,
#         "Kilobit per second": 0.001,
#         "Megabit per second": 0.000001,
#         "Gigabit per second": 1e-9
#     },
#     "Digital Storage": {
#         "Byte": 1,
#         "Kilobyte": 0.001,
#         "Megabyte": 1e-6,
#         "Gigabyte": 1e-9
#     },
#     "Energy": {
#         "Joule": 1,
#         "Kilojoule": 0.001,
#         "Calorie": 0.239006,
#         "Kilowatt-hour": 2.77778e-7
#     },
#     "Frequency": {
#         "Hertz": 1,
#         "Kilohertz": 0.001,
#         "Megahertz": 1e-6,
#         "Gigahertz": 1e-9
#     },
#     "Fuel Economy": {
#         "Miles per gallon": 1,
#         "Kilometers per liter": 0.425144,
#         "Liters per 100 km": 235.215
#     },
#     "Mass": {
#         "Kilogram": 1,
#         "Gram": 1000,
#         "Pound": 2.20462,
#         "Ounce": 35.274
#     },
#     "Plane Angle": {
#         "Degree": 1,
#         "Radian": 0.0174533,
#         "Gradian": 1.11111
#     },
#     "Pressure": {
#         "Pascal": 1,
#         "Kilopascal": 0.001,
#         "Bar": 1e-5,
#         "PSI": 0.000145038
#     },
#     "Speed": {
#         "Meter per second": 1,
#         "Kilometer per hour": 3.6,
#         "Mile per hour": 2.23694,
#         "Knot": 1.94384
#     },
#     "Time": {
#         "Second": 1,
#         "Minute": 0.0166667,
#         "Hour": 0.000277778,
#         "Day": 1.15741e-5
#     }
# }

# # Temperature conversion functions
# def celsius_to_fahrenheit(c):
#     return (c * 9/5) + 32

# def fahrenheit_to_celsius(f):
#     return (f - 32) * 5/9

# def celsius_to_kelvin(c):
#     return c + 273.15

# def kelvin_to_celsius(k):
#     return k - 273.15

# # Main conversion function
# def convert_value(value, from_unit, to_unit, category):
#     factors = CONVERSION_FACTORS[category]
#     if category == "Temperature":
#         if from_unit == to_unit:
#             return value, "No conversion needed"
#         converters = {
#             ("Celsius", "Fahrenheit"): celsius_to_fahrenheit,
#             ("Fahrenheit", "Celsius"): fahrenheit_to_celsius,
#             ("Celsius", "Kelvin"): celsius_to_kelvin,
#             ("Kelvin", "Celsius"): kelvin_to_celsius,
#             ("Fahrenheit", "Kelvin"): lambda f: celsius_to_kelvin(fahrenheit_to_celsius(f)),
#             ("Kelvin", "Fahrenheit"): lambda k: celsius_to_fahrenheit(kelvin_to_celsius(k))
#         }
#         return converters[(from_unit, to_unit)](value), "Converted"
#     else:
#         base_value = value / factors[from_unit]
#         converted = base_value * factors[to_unit]
#         return converted, f"{value} {from_unit} × ({factors[to_unit]}/{factors[from_unit]})"

# # UI Components
# developer_profile()  # Add profile section to sidebar
# st.title("Modern Unit Converter")

# # Category selection
# category = st.sidebar.selectbox("Category", list(CONVERSION_FACTORS.keys()))
# units = list(CONVERSION_FACTORS[category].keys()) if category != "Temperature" else CONVERSION_FACTORS[category]

# # Main conversion UI
# col1, col2, col3 = st.columns([3, 1, 3])
# with col1:
#     st.session_state.from_unit = st.selectbox("From", units, index=units.index(st.session_state.from_unit) if st.session_state.from_unit in units else 0)
# with col2:
#     st.write("")  # Spacer
#     if st.button("↔ Swap"):
#         st.session_state.from_unit, st.session_state.to_unit = st.session_state.to_unit, st.session_state.from_unit
#         st.rerun()
# with col3:
#     st.session_state.to_unit = st.selectbox("To", units, index=units.index(st.session_state.to_unit) if st.session_state.to_unit in units else 0)

# value = st.number_input("Value", value=1.0)

# # Perform conversion
# if st.button("Convert"):
#     try:
#         converted, formula = convert_value(value, st.session_state.from_unit, st.session_state.to_unit, category)
#         result = f"{value} {st.session_state.from_unit} = {converted:.4f} {st.session_state.to_unit}"
#         st.session_state.history.append(result)
#         st.markdown(f"""
#         <div class="result-card">
#             <h3>{result}</h3>
#             <p>Formula: {formula}</p>
#         </div>
#         """, unsafe_allow_html=True)
#     except Exception as e:
#         st.error(f"Conversion error: {str(e)}")

# # History Section
# st.sidebar.header("Conversion History")
# for entry in reversed(st.session_state.history[-5:]):
#     st.sidebar.write(entry)
# if st.sidebar.button("Clear History"):
#     st.session_state.history = []

# # Theme Toggle
# if st.sidebar.button("Toggle Dark Mode"):
#     st.session_state.dark_mode = not st.session_state.dark_mode
#     st.markdown("<script>document.body.classList.toggle('dark-theme');</script>", unsafe_allow_html=True)





















# # unit_converter.py

# import streamlit as st
# import pandas as pd
# import time

# # Set page configuration
# st.set_page_config(page_title="Modern Unit Converter", layout="wide")

# # Custom CSS and JavaScript for animations and modern UI
# st.markdown(
#     """
#     <style>
#     @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');

#     body {
#         background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
#         font-family: 'Poppins', sans-serif;
#         color: #333;
#     }
#     .stButton>button {
#         background: linear-gradient(90deg, #ff6f61, #ff9a76);
#         color: white;
#         border: none;
#         border-radius: 12px;
#         padding: 12px 24px;
#         font-size: 16px;
#         transition: transform 0.2s ease-in-out;
#     }
#     .stButton>button:hover {
#         transform: scale(1.05);
#         background: linear-gradient(90deg, #ff9a76, #ff6f61);
#     }
#     .result-card {
#         background: rgba(255, 255, 255, 0.8);
#         border-radius: 20px;
#         padding: 25px;
#         box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
#         backdrop-filter: blur(10px);
#         margin-top: 20px;
#         text-align: center;
#         animation: fadeIn 0.5s ease-in-out;
#     }
#     @keyframes fadeIn {
#         0% { opacity: 0; transform: translateY(20px); }
#         100% { opacity: 1; transform: translateY(0); }
#     }
#     .spinner {
#         border: 4px solid #f3f3f3;
#         border-top: 4px solid #ff6f61;
#         border-radius: 50%;
#         width: 30px;
#         height: 30px;
#         animation: spin 1s linear infinite;
#         margin: 20px auto;
#     }
#     @keyframes spin {
#         0% { transform: rotate(0deg); }
#         100% { transform: rotate(360deg); }
#     }
#     .swap-button {
#         animation: rotate 0.3s ease-in-out;
#     }
#     @keyframes rotate {
#         0% { transform: rotate(0deg); }
#         100% { transform: rotate(360deg); }
#     }
#     .stSelectbox, .stNumberInput, .stTextInput {
#         background: rgba(255, 255, 255, 0.9);
#         border-radius: 12px;
#         padding: 10px;
#         box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
#     }
#     .sidebar .stButton>button {
#         background: linear-gradient(90deg, #ff4b4b, #ff7878);
#     }
#     .category-icon {
#         margin-right: 10px;
#         font-size: 20px;
#         color: #ff6f61;
#     }
#     .unit-info {
#         font-size: 12px;
#         color: #666;
#         cursor: pointer;
#         margin-left: 5px;
#     }
#     .quick-convert {
#         background: rgba(255, 255, 255, 0.7);
#         border-radius: 12px;
#         padding: 15px;
#         margin-bottom: 20px;
#         box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
#     }
#     </style>
#     <script>
#     function showUnitInfo(unit, info) {
#         alert(`Unit Info: ${unit}\\n${info}`);
#     }
#     </script>
#     """,
#     unsafe_allow_html=True
# )

# # Title
# st.markdown("<h1 style='text-align: center; color: #333;'>Modern Unit Converter</h1>", unsafe_allow_html=True)

# # Initialize session state
# if "history" not in st.session_state:
#     st.session_state.history = []
# if "favorites" not in st.session_state:
#     st.session_state.favorites = []
# if "from_unit" not in st.session_state:
#     st.session_state.from_unit = "Meter"
# if "to_unit" not in st.session_state:
#     st.session_state.to_unit = "Centimeter"
# if "show_result" not in st.session_state:
#     st.session_state.show_result = False

# # Sidebar for category selection
# st.sidebar.header("Unit Category")
# category = st.sidebar.selectbox(
#     "Select Category",
#     ["Length", "Weight", "Temperature", "Area", "Volume"],
#     format_func=lambda x: f"<i class='fas fa-{ 'ruler' if x == 'Length' else 'weight' if x == 'Weight' else 'thermometer-half' if x == 'Temperature' else 'square' if x == 'Area' else 'cube' } category-icon'></i> {x}".format(x=x),
#     key="category"
# )

# # Define conversion factors
# length_units = {
#     "Meter": 1,
#     "Centimeter": 100,
#     "Kilometer": 0.001,
#     "Millimeter": 1000,
#     "Inch": 39.3701,
#     "Foot": 3.28084
# }

# weight_units = {
#     "Kilogram": 1,
#     "Gram": 1000,
#     "Milligram": 1000000,
#     "Pound": 2.20462,
#     "Ounce": 35.274
# }

# temperature_units = ["Celsius", "Fahrenheit", "Kelvin"]

# area_units = {
#     "Square Meter": 1,
#     "Square Kilometer": 0.000001,
#     "Square Centimeter": 10000,
#     "Square Mile": 0.0000003861,
#     "Square Foot": 10.7639
# }

# volume_units = {
#     "Cubic Meter": 1,
#     "Liter": 1000,
#     "Milliliter": 1000000,
#     "Cubic Foot": 35.3147,
#     "Gallon (US)": 264.172
# }

# # Temperature conversion functions
# def celsius_to_fahrenheit(celsius):
#     return (celsius * 9/5) + 32

# def fahrenheit_to_celsius(fahrenheit):
#     return (fahrenheit - 32) * 5/9

# def celsius_to_kelvin(celsius):
#     return celsius + 273.15

# def kelvin_to_celsius(kelvin):
#     return kelvin - 273.15

# def fahrenheit_to_kelvin(fahrenheit):
#     celsius = fahrenheit_to_celsius(fahrenheit)
#     return celsius_to_kelvin(celsius)

# def kelvin_to_fahrenheit(kelvin):
#     celsius = kelvin_to_celsius(kelvin)
#     return celsius_to_fahrenheit(celsius)

# # Conversion function
# def convert_value(value, from_unit, to_unit, category):
#     if category == "Length":
#         value_in_base = value / length_units[from_unit]
#         converted_value = value_in_base * length_units[to_unit]
#         formula = f"Multiply {value} {from_unit} by {length_units[to_unit] / length_units[from_unit]} to get {to_unit}"
#         return converted_value, formula

#     elif category == "Weight":
#         value_in_base = value / weight_units[from_unit]
#         converted_value = value_in_base * weight_units[to_unit]
#         formula = f"Multiply {value} {from_unit} by {weight_units[to_unit] / weight_units[from_unit]} to get {to_unit}"
#         return converted_value, formula

#     elif category == "Area":
#         value_in_base = value / area_units[from_unit]
#         converted_value = value_in_base * area_units[to_unit]
#         formula = f"Multiply {value} {from_unit} by {area_units[to_unit] / area_units[from_unit]} to get {to_unit}"
#         return converted_value, formula

#     elif category == "Volume":
#         value_in_base = value / volume_units[from_unit]
#         converted_value = value_in_base * volume_units[to_unit]
#         formula = f"Multiply {value} {from_unit} by {volume_units[to_unit] / volume_units[from_unit]} to get {to_unit}"
#         return converted_value, formula

#     else:  # Temperature
#         if from_unit == to_unit:
#             return value, f"No conversion needed: {from_unit} to {to_unit}"
#         if from_unit == "Celsius" and to_unit == "Fahrenheit":
#             converted_value = celsius_to_fahrenheit(value)
#             formula = f"({value} °C × 9/5) + 32 = {converted_value} °F"
#         elif from_unit == "Fahrenheit" and to_unit == "Celsius":
#             converted_value = fahrenheit_to_celsius(value)
#             formula = f"({value} °F - 32) × 5/9 = {converted_value} °C"
#         elif from_unit == "Celsius" and to_unit == "Kelvin":
#             converted_value = celsius_to_kelvin(value)
#             formula = f"{value} °C + 273.15 = {converted_value} K"
#         elif from_unit == "Kelvin" and to_unit == "Celsius":
#             converted_value = kelvin_to_celsius(value)
#             formula = f"{value} K - 273.15 = {converted_value} °C"
#         elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
#             converted_value = fahrenheit_to_kelvin(value)
#             formula = f"(({value} °F - 32) × 5/9) + 273.15 = {converted_value} K"
#         else:  # Kelvin to Fahrenheit
#             converted_value = kelvin_to_fahrenheit(value)
#             formula = f"(({value} K - 273.15) × 9/5) + 32 = {converted_value} °F"
#         return converted_value, formula

# # Quick Convert feature
# st.markdown("<h3 style='text-align: center; color: #666;'>Quick Convert</h3>", unsafe_allow_html=True)
# quick_options = {
#     "1 Meter to Centimeter": ("Length", "Meter", "Centimeter", 1.0),
#     "1 Kilogram to Pound": ("Weight", "Kilogram", "Pound", 1.0),
#     "1 Celsius to Fahrenheit": ("Temperature", "Celsius", "Fahrenheit", 1.0),
#     "1 Square Meter to Square Foot": ("Area", "Square Meter", "Square Foot", 1.0),
#     "1 Liter to Gallon (US)": ("Volume", "Liter", "Gallon (US)", 1.0)
# }
# quick_select = st.selectbox("Select a Quick Conversion", list(quick_options.keys()), key="quick_convert")
# if st.button("Apply Quick Convert"):
#     quick_category, quick_from, quick_to, quick_value = quick_options[quick_select]
#     st.session_state.category = quick_category
#     st.session_state.from_unit = quick_from
#     st.session_state.to_unit = quick_to
#     st.session_state.value = quick_value
#     st.rerun()

# # Select units based on category
# if category == "Length":
#     units = list(length_units.keys())
# elif category == "Weight":
#     units = list(weight_units.keys())
# elif category == "Area":
#     units = list(area_units.keys())
# elif category == "Volume":
#     units = list(volume_units.keys())
# else:
#     units = temperature_units

# # Main UI layout
# col1, col2, col3 = st.columns([3, 1, 3])

# with col1:
#     # Unit search
#     search_from = st.text_input("Search From Unit", key="search_from")
#     filtered_from_units = [unit for unit in units if search_from.lower() in unit.lower()]
#     if not filtered_from_units:
#         filtered_from_units = units
#     st.session_state.from_unit = st.selectbox("From", filtered_from_units, key="from_unit_select")
#     # Unit info button
#     st.markdown(
#         f"<span class='unit-info' onclick=\"showUnitInfo('{st.session_state.from_unit}', 'Base conversion factor: {length_units.get(st.session_state.from_unit, 1)}')\"><i class='fas fa-info-circle'></i></span>",
#         unsafe_allow_html=True
#     )
#     value = st.number_input("Value", value=1.0, step=0.1, key="value")

# with col2:
#     st.write("")  # Spacer
#     st.markdown("<h3 style='text-align: center;'>=</h3>", unsafe_allow_html=True)
#     if st.button("🔄 Swap Units", key="swap"):
#         st.session_state.from_unit, st.session_state.to_unit = st.session_state.to_unit, st.session_state.from_unit
#         st.rerun()

# with col3:
#     # Unit search
#     search_to = st.text_input("Search To Unit", key="search_to")
#     filtered_to_units = [unit for unit in units if search_to.lower() in unit.lower()]
#     if not filtered_to_units:
#         filtered_to_units = units
#     st.session_state.to_unit = st.selectbox("To", filtered_to_units, key="to_unit_select")
#     # Unit info button
#     st.markdown(
#         f"<span class='unit-info' onclick=\"showUnitInfo('{st.session_state.to_unit}', 'Base conversion factor: {length_units.get(st.session_state.to_unit, 1)}')\"><i class='fas fa-info-circle'></i></span>",
#         unsafe_allow_html=True
#     )

# # Perform conversion with loading spinner
# if st.button("Convert"):
#     st.session_state.show_result = False
#     st.markdown("<div class='spinner'></div>", unsafe_allow_html=True)
#     time.sleep(1)  # Simulate processing
#     st.session_state.show_result = True

# if st.session_state.show_result and value is not None:
#     converted_value, formula = convert_value(value, st.session_state.from_unit, st.session_state.to_unit, category)
    
#     # Display result in a card
#     st.markdown(
#         f"""
#         <div class="result-card">
#             <h3>{value} {st.session_state.from_unit} = {converted_value:.2f} {st.session_state.to_unit}</h3>
#             <p><b>Formula:</b> {formula}</p>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     # Add to history
#     conversion_entry = f"{value} {st.session_state.from_unit} = {converted_value:.2f} {st.session_state.to_unit}"
#     st.session_state.history.append(conversion_entry)
#     if len(st.session_state.history) > 10:
#         st.session_state.history.pop(0)

# # Add to favorites
# if st.button("⭐ Add to Favorites"):
#     conversion_entry = f"{value} {st.session_state.from_unit} = {converted_value:.2f} {st.session_state.to_unit}"
#     if conversion_entry not in st.session_state.favorites:
#         st.session_state.favorites.append(conversion_entry)
#         st.success("Added to Favorites!")

# # Sidebar: History and Favorites with collapsible sections
# with st.sidebar.expander("Conversion History"):
#     for entry in reversed(st.session_state.history):
#         st.write(entry)
#     if st.button("Clear History"):
#         st.session_state.history = []
#         st.rerun()

# # Export history as CSV
# if st.session_state.history:
#     history_df = pd.DataFrame(st.session_state.history, columns=["Conversion"])
#     csv = history_df.to_csv(index=False)
#     st.sidebar.download_button(
#         label="📥 Download History as CSV",
#         data=csv,
#         file_name="conversion_history.csv",
#         mime="text/csv"
#     )

# with st.sidebar.expander("Favorites"):
#     for fav in st.session_state.favorites:
#         st.write(fav)
#     if st.button("Clear Favorites"):
#         st.session_state.favorites = []
#         st.rerun()  