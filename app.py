import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types
from quiz_data import QUIZ_BANK

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
            "model_url": "https://raw.githubusercontent.com/ArnavMehra451/Sanskritidemo/main/assets/Sanchi_Stupa.glb"
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
    "Tamil Nadu": {
        "Brihadeshwara Temple": {
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
    },
    "Uttar Pradesh": {
            "Taj Mahal,Agra": {
                "period": "Mughal Empire (Construction: 1631 to 1648; Complex completed 1653).",
                "desc": "Located in Agra, Uttar Pradesh, this white marble mausoleum was commissioned by the Mughal Emperor Shah Jahan to house the tomb of his favorite wife, Mumtaz Mahal. Renowned as a UNESCO World Heritage site and a masterpiece of Mughal architecture, it blends Persian, Islamic, and Indian design elements and is celebrated worldwide as a symbol of love.",
                "img": "https://images.unsplash.com/photo-1696887484490-715e7eb0e682?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dGFqJTIwbWFoYWx8ZW58MHx8MHx8fDA%3D",
                "model_url": "https://raw.githubusercontent.com/ArnavMehra451/Sanskritidemo/main/assets/Taj_Mahal.glb"
            }
    },
    "Maharashtra": {
            "Gateway Of India,Mumbai": {
                "period": "Colonial Era (Construction: 1911 to 1924; Unveiled December 4, 1924).",
                "desc": "Located on the waterfront in Mumbai, this Indo-Saracenic archway was built to commemorate the 1911 landing of King George V and Queen Mary in India. Historically, it served as the ceremonial entrance to India for British viceroys and governors, and notably marked the end of British rule when the last British troops marched through it in 1948.",
                "img": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Z2F0ZXdheSUyMG9mJTIwaW5kaWF8ZW58MHx8MHx8fDA%3D",
                "model_url": "https://raw.githubusercontent.com/ArnavMehra451/Sanskritidemo/main/assets/Gateway_Of_India.glb"
            }
    },
    "Gujrat": {
            "Statue Of Unity,Sandhu Bet": {
                "period": "Modern Era (Construction: 2013-2018; Inaugurated October 31, 2018).",
                "desc": "Standing at 182 meters in Gujarat, India, it is the world's tallest statue. Built as a tribute to Sardar Vallabhbhai Patel, one of India's founding fathers who played a key role in unifying 565 princely states into the modern Union of India, it symbolizes national unity and engineering prowess.",
                "img": "https://images.unsplash.com/photo-1642841819300-20ed449c02a1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8c3RhdHVlJTIwb2YlMjB1bml0eXxlbnwwfHwwfHx8MA%3D%3D",
                "model_url": "https://raw.githubusercontent.com/ArnavMehra451/Sanskritidemo/main/assets/Statue_Of_Unity.glb"
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
    
    user_query = st.text_input("Type your question here:", "")
    
    if st.button("Ask Guide"):
        if "GEMINI_API_KEY" in st.secrets:
            try:
                # Initialize Google GenAI client using Streamlit secrets
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                
                system_prompt = """
                You are SanskritiVerse, an expert AI Indian Cultural & Heritage Guide.
                Your sole domain is Indian monuments, dynasty history, art, architecture, festivals, and traditions.
                
                Strict Rules:
                1. Answer questions related to Indian culture and heritage thoroughly and concisely.
                2. If the user asks an off-topic question (e.g., coding, mathematics, sports, general technology, modern politics), politely refuse to answer.
                3. Gently redirect them back to asking about Indian culture or monuments.
                """


                with st.spinner("Asking SanskritiVerse AI Guide..."):
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=f"You are SanskritiVerse, an expert AI Indian Cultural Guide. Provide an engaging, accurate, and concise answer to: {user_query}",
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            temperature=0.3
                        )
                    )
                st.success("**AI Guide Response:**")
                st.write(response.text)
            except Exception as e:
                st.error(f"API Error: {e}")
        else:
            st.warning("⚠️ **API Key missing:** Add `GEMINI_API_KEY` to `.streamlit/secrets.toml` locally or in Streamlit Secrets Vault to enable live AI responses.")

# PAGE 3: CULTURAL QUIZ
elif page == "Cultural Quiz":
    st.title("🏛️ SanskritiVerse Heritage Quiz")
    st.subheader("Test your knowledge of Indian States & Cultural Heritage")

    # Step 1: State Selection
    state_list = list(QUIZ_BANK.keys())
    selected_state = st.selectbox(
        "Choose a State to start the quiz:", ["-- Select State --"] + state_list
    )

    if selected_state != "-- Select State --":
        questions = QUIZ_BANK[selected_state]

        # Initialize Session State Variables for current quiz run
        if (
            "current_state" not in st.session_state
            or st.session_state.current_state != selected_state
        ):
            st.session_state.current_state = selected_state
            st.session_state.submitted = False
            st.session_state.user_answers = {}

        st.markdown(f"### Quiz: **{selected_state}**")
        st.divider()

        # Step 2: Render Questions via Form
        with st.form("quiz_form"):
            for idx, q in enumerate(questions):
                st.write(f"**Q{idx + 1}: {q['question']}**")
                st.session_state.user_answers[idx] = st.radio(
                    f"Select answer for Q{idx + 1}:",
                    options=q["options"],
                    key=f"q_{selected_state}_{idx}",
                    index=None,
                )
                st.write("---")

            submit_btn = st.form_submit_button("Submit Quiz")

        # Step 3: Grade and Show Results
        if submit_btn:
            st.session_state.submitted = True

        if st.session_state.get("submitted", False):
            score = 0
            total = len(questions)

            st.markdown("## 📊 Quiz Results")

            for idx, q in enumerate(questions):
                user_ans = st.session_state.user_answers.get(idx)
                correct_ans = q["answer"]

                if user_ans == correct_ans:
                    score += 1
                    st.success(
                        f"**Q{idx + 1}:** Correct! Your answer: *{user_ans}*"
                    )
                else:
                    st.error(
                        f"**Q{idx + 1}:** Incorrect.\n\n"
                        f"* **Your Answer:** {user_ans if user_ans else 'No answer selected'}\n"
                        f"* **Correct Answer:** {correct_ans}"
                    )

            # Final Score Summary
            percentage = (score / total) * 100
            st.metric("Final Score", f"{score} / {total}", f"{percentage:.1f}%")

            if percentage == 100:
                st.balloons()

            # Reset Quiz Button
            if st.button("🔄 Retake Quiz"):
                st.session_state.submitted = False
                st.session_state.user_answers = {}
                st.rerun()                                                                     