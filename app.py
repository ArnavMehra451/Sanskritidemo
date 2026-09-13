import streamlit as st
import streamlit.components.v1 as components
from google import genai

# Page Configuration
st.set_page_config(page_title="SanskritiVerse", page_icon="🏛️", layout="wide")

# Sidebar Navigation
st.sidebar.title("🏛️ SanskritiVerse")
st.sidebar.subheader("Cultural Heritage Portal")
page = st.sidebar.radio("Navigate", ["Heritage Explorer", "AI Cultural Guide", "Cultural Quiz"])

# DATA: Sample Heritage Data (Includes Multi-Monument Support for MP)
heritage_data = {
    "Madhya Pradesh": {
        "Sanchi Stupa": {
            "period": "3rd Century BCE (Mauryan Empire)",
            "desc": "One of India's oldest stone structures commissioned by Emperor Ashoka, famous for its majestic dome and carved Toranas (gateways).",
            "img": "https://images.unsplash.com/photo-1699988194923-50f944f92d9a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8c2FuY2hpJTIwc3R1cGF8ZW58MHx8MHx8fDA%3D",
            "model_url": "https://modelviewer.dev/shared-assets/models/Astronaut.glb"
        },
        "Gwalior Fort": {
            "period": "8th Century CE onwards",
            "desc": "Described by Babur as 'the pearl among fortresses of Hind', featuring Man Mandir Palace and iconic turquoise tilework.",
            "img": "https://images.unsplash.com/photo-1691515310304-08816f9391d4?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Z3dhbGlvciUyMGZvcnR8ZW58MHx8MHx8fDA%3D",
            "model_url": "https://modelviewer.dev/shared-assets/models/Astronaut.glb"
        },
        "Khajuraho Group of Monuments": {
            "period": "950 - 1050 CE (Chandela Dynasty)",
            "desc": "UNESCO World Heritage site celebrated for its Nagara-style temple architecture and intricate stone sculptures.",
            "img": "https://images.unsplash.com/photo-1672215055915-e6143dc70e6a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8a2hhanVyYWhvJTIwZ3JvdXAlMjBvZiUyMHRlbXBsZXN8ZW58MHx8MHx8fDA%3D",
            "model_url": "https://modelviewer.dev/shared-assets/models/Astronaut.glb",
        }
    },
    "Maharashtra": {
        "Ajanta & Ellora Caves": {
            "period": "2nd Century BCE - 10th Century CE",
            "desc": "Ancient rock-cut caves showcasing masterpiece Buddhist, Hindu, and Jain sculptures and mural paintings.",
            "img": "https://images.unsplash.com/photo-1559318246-114068fc532e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjB8fGFqYW50YSUyMCUyNiUyMGVsbG9yYSUyMGNhdmVzfGVufDB8fDB8fHww",
            "model_url": "https://modelviewer.dev/shared-assets/models/Astronaut.glb"
        }
    },
    "Tamil Nadu": {
        "Brihadeeswarar Temple": {
            "period": "1010 CE (Chola Dynasty)",
            "desc": "A UNESCO World Heritage site built by Rajaraja Chola I, famous for its massive granite vimana tower.",
            "img": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?q=80&w=800",
            "model_url": "https://modelviewer.dev/shared-assets/models/Astronaut.glb"
        }
    },
    "Rajasthan": {
        "Amer Fort, Jaipur": {
            "period": "1592 CE",
            "desc": "Known for its artistic Hindu style elements, built with red sandstone and marble overlooking Maota Lake.",
            "img": "https://images.unsplash.com/photo-1599661046289-e31897846e41?q=80&w=800",
            "model_url": "https://modelviewer.dev/shared-assets/models/Astronaut.glb"
        }
    }
}

# PAGE 1: HERITAGE EXPLORER
if page == "Heritage Explorer":
    st.title("🗺️ Interactive Heritage Explorer")
    st.write("Select a state to explore its key monuments, history, and virtual artifacts.")
    
    selected_state = st.selectbox("Choose a State / Region:", list(heritage_data.keys()))
    
    # If the state has multiple monuments, let the user pick one; otherwise pick the single monument
    monuments = heritage_data[selected_state]
    if len(monuments) > 1:
        selected_monument = st.selectbox("Select Monument:", list(monuments.keys()))
    else:
        selected_monument = list(monuments.keys())[0]
        
    data = monuments[selected_monument]
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header(selected_monument)
        st.caption(f"**Historical Era:** {data['period']}")
        st.write(data["desc"])
        
        st.markdown("---")
        st.subheader("3D Artifact Viewer")
        # 1. Dynamically pull the model URL for the active monument
    active_model = data.get("model_url", "")
    
    # 2. Render button
    if st.button(f"Launch 3D View for {selected_monument}"):
        if active_model:
            # 3. Inject the active_model variable inside the WebGL string
            webgl_viewer_code = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js"></script>
                <style>
                    body {{ margin: 0; background-color: transparent; }}
                    model-viewer {{
                        width: 100%;
                        height: 350px;
                        background-color: #1e1e1e;
                        border-radius: 12px;
                    }}
                </style>
            </head>
            <body>
                <model-viewer 
                    src="{active_model}" 
                    alt="{selected_monument} 3D Asset" 
                    auto-rotate 
                    camera-controls 
                    shadow-intensity="1">
                </model-viewer>
            </body>
            </html>
            """
            components.html(webgl_viewer_code, height=370)
        else:
            st.warning("3D asset link not available for this monument.")
    else:
        st.info("💡 *Click above to render the 3D WebGL interactive model.*")

    with col2:
        st.markdown(f'<img src="{data["img"]}" referrerpolicy="no-referrer" style="width:100%; border-radius:10px;">', unsafe_allow_html=True)
        st.caption(selected_monument)

# PAGE 2: AI CULTURAL GUIDE
elif page == "AI Cultural Guide":
    st.title("💬 AI Cultural Tour Guide")
    st.write("Ask any questions about Indian monuments, dynasty history, or traditions.")
    
    user_query = st.text_input("Type your question here:", "Tell me an interesting fact about Rajaraja Chola.")
    
    if st.button("Ask Guide"):
        st.success("**AI Guide Response:**")
        st.write("Rajaraja Chola I built the Brihadeeswarar Temple in Thanjavur. The shadow of the main tower (Vimana) is designed in a way that it never touches the ground at noon during certain seasons, demonstrating extraordinary 11th-century engineering capabilities!")

# PAGE 3: CULTURAL QUIZ
elif page == "Cultural Quiz":
    st.title("🏆 Gamified Heritage Quiz")
    st.write("Test your knowledge and earn cultural discovery badges.")
    
    q1 = st.radio("1. Which dynasty built the Brihadeeswarar Temple?", ["Mughal Dynasty", "Chola Dynasty", "Gupta Dynasty"])
    q2 = st.radio("2. Where are the Ajanta & Ellora Caves located?", ["Madhya Pradesh", "Karnataka", "Maharashtra"])
    
    if st.button("Submit Quiz"):
        score = 0
        if q1 == "Chola Dynasty": score += 1
        if q2 == "Maharashtra": score += 1
        st.balloons()
        st.success(f"You scored {score}/2! You earned the **'Heritage Scholar'** Badge 🎉")