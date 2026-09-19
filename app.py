import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from google import genai
from google.genai import types
from datetime import datetime
from quiz_data import QUIZ_BANK

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sanskriti Verse: Digital Heritage Explorer",
    page_icon="🪔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CUSTOM CSS — Pure Black Dark Theme
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Playfair+Display:wght@600;700&display=swap');

    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    
    html, body, [class*="css"], p, span, div, h1, h2, h3, h4, h5, h6, label { 
        font-family: 'Poppins', sans-serif;
        color: #E0E0E0 !important;
    }

    .main-header {
        background: linear-gradient(90deg, #FF9933 0%, #222222 50%, #138808 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(255,255,255,0.1);
    }
    .main-header h1 {
        font-family: 'Playfair Display', serif !important;
        color: #FFFFFF !important;
        font-size: 2.6rem;
        margin-bottom: 0.2rem;
    }
    .main-header p { color: #CCCCCC !important; font-size: 1.1rem; }

    .info-card {
        background: #111111;
        border-left: 5px solid #FF9933;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(255,255,255,0.05);
    }
    .culture-card {
        background: #1A1A1A;
        border-radius: 14px;
        padding: 1.3rem;
        box-shadow: 0 3px 10px rgba(255,255,255,0.1);
        border-top: 4px solid #138808;
        transition: transform 0.2s;
        height: 100%;
    }
    .culture-card:hover { transform: translateY(-5px); }

    .stat-box {
        background: linear-gradient(135deg, #1A1A2E, #16213E);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid #333;
    }
    .stat-box h2 { color: #FFD700 !important; margin: 0; font-size: 2rem; }
    .stat-box p { margin: 0; font-size: 0.9rem; opacity: 0.9; }

    .footer {
        text-align: center;
        color: #888888 !important;
        padding: 1.5rem;
        margin-top: 2rem;
        border-top: 1px solid #333333;
    }
    
    .quiz-question {
        background: #151515;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 3px solid #138808;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>🪔 Sanskriti Verse: Digital Heritage Explorer</h1>
    <p>Preserving & Promoting India's Rich Cultural Heritage and Traditions </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# PANDAS DATA SETUP (All States + Key UTs)
# ---------------------------------------------------------
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

heritage_raw_data = [
    {
        "State": "Andhra Pradesh",
        "Emoji": "🌶️",
        "Art": "Kalamkari",
        "Festival": "Ugadi",
        "Dance": "Kuchipudi",
        "Food": "Pulihora",
        "Monument": "Tirupati Balaji Temple",
        "UNESCO Sites": 0,
        "Desc": "Known for its rich cultural heritage, ancient temples, and spicy cuisine.",
        "Heritage_Spots": [
            {
                "Name": "Tirumala Venkateswara Temple",
                "Info": "One of the holiest and wealthiest Hindu shrines nestled in the Seshachalam hills.",
                "Detail": "Dedicated to Lord Venkateswara, this massive architectural landmark witnesses tens of thousands of pilgrims daily. It showcases stunning Dravidian architecture, ornate mandapas, and deep spiritual significance.",
                "Era": "Ancient/Medieval",
                "Significance": "Religious pilgrimage epicentre"
            },
            {
                "Name": "Lepakshi Temple",
                "Info": "A 16th-century architectural marvel known for its famous hanging pillar.",
                "Detail": "Built during the Vijayanagara Empire, Lepakshi features magnificent stone carvings, vibrant ceiling frescoes depicting Hindu epics, and a massive monolithic Nandi bull carved out of a single granite block.",
                "Era": "16th Century (Vijayanagara Empire)",
                "Significance": "Masterpiece of Vijayanagara art and engineering"
            },
            {
                "Name": "Undavalli Caves",
                "Info": "Monolithic rock-cut cave temples carved out of a sandstone hill on the Krishna River bank.",
                "Detail": "Dating back to the 4th-5th century AD, these multi-story caves feature a massive reclining statue of Lord Vishnu carved from a single block of granite, alongside fine Buddhist and Hindu art reliefs.",
                "Era": "4th-5th Century AD",
                "Significance": "Early rock-cut architecture transition"
            }
        ]
    },
    {
        "State": "Arunachal Pradesh",
        "Emoji": "⛰️",
        "Art": "Thangka Painting",
        "Festival": "Losar",
        "Dance": "Lion and Peacock Dance",
        "Food": "Thukpa",
        "Monument": "Tawang Monastery",
        "UNESCO Sites": 0,
        "Desc": "The Land of Dawn-Lit Mountains, rich in tribal culture and pristine eastern Himalayan beauty.",
        "Heritage_Spots": [
            {
                "Name": "Tawang Monastery",
                "Info": "The largest monastery in India and second largest in the world at 10,000 feet.",
                "Detail": "Built in the 17th century, this 3-storey monastic complex belongs to the Gelugpa sect of Mahayana Buddhism, preserving priceless ancient manuscripts, scriptures, and sacred thangkas.",
                "Era": "17th Century",
                "Significance": "Spiritual heart of Himalayan Buddhism"
            },
            {
                "Name": "Ita Fort",
                "Info": "A historic 14th-century brick fortification located in the capital city of Itanagar.",
                "Detail": "Meaning 'Fort of Bricks', it features unique irregular brick blocks across multiple entry gates, serving as a vital archaeological milestone of medieval indigenous rule.",
                "Era": "14th-15th Century",
                "Significance": "Ancient indigenous administrative fort"
            },
            {
                "Name": "Malinithan Temple Ruins",
                "Info": "An archaeological temple site showcasing exquisite 14th-century granite sculptures.",
                "Detail": "Located at the foot of the Siang hills, Malinithan is famous for its classical Nagara-style temple ruins dedicated to Goddess Durga, alongside fine sculptures linked with local Mahabharata folklore.",
                "Era": "14th Century",
                "Significance": "Fusion of regional tribal culture and classical Hindu traditions"
            }
        ]
    },
    {
        "State": "Assam",
        "Emoji": "🦏",
        "Art": "Bamboo Craft",
        "Festival": "Bihu",
        "Dance": "Sattriya",
        "Food": "Masor Tenga",
        "Monument": "Kamakhya Temple",
        "UNESCO Sites": 2,
        "Desc": "Famous for its sprawling tea gardens, one-horned rhinoceros, and vibrant Bihu festivities.",
        "Heritage_Spots": [
            {
                "Name": "Kamakhya Temple",
                "Info": "One of the oldest and most revered Shakti Peethas situated on Nilachal Hill.",
                "Detail": "Dedicated to Goddess Kamakhya, this temple is a central hub of Tantric-shakti worship. It features unique beehive-shaped domes and attracts millions of devotees during the annual Ambubachi Mela.",
                "Era": "Ancient / Rebuilt 16th Century",
                "Significance": "Premier Shakti Peetha of India"
            },
            {
                "Name": "Kaziranga National Park",
                "Info": "A UNESCO World Heritage Site hosting two-thirds of the world's great one-horned rhinoceroses.",
                "Detail": "Set against the backdrop of the Brahmaputra River, this sanctuary boasts incredible biodiversity, thriving elephant populations, tigers, and rich wetlands vital for ecological heritage.",
                "Era": "Established 1905",
                "Significance": "Global conservation landmark"
            },
            {
                "Name": "Rang Ghar",
                "Info": "An 18th-century two-story royal sports pavilion built by the Ahom kings.",
                "Detail": "Considered the oldest amphitheatre in Asia, Ahom royalty used it to watch traditional games like buffalo fights and bulbuli bird fights during festival seasons.",
                "Era": "18th Century (Ahom Kingdom)",
                "Significance": "Royal architectural heritage of Northeast India"
            }
        ]
    },
    {
        "State": "Bihar",
        "Emoji": "🪷",
        "Art": "Madhubani Painting",
        "Festival": "Chhath Puja",
        "Dance": "Bidesiya",
        "Food": "Litti Chokha",
        "Monument": "Mahabodhi Temple",
        "UNESCO Sites": 2,
        "Desc": "Ancient land of knowledge, birthplace of Buddhism and Jainism.",
        "Heritage_Spots": [
            {
                "Name": "Mahabodhi Temple Complex",
                "Info": "A UNESCO World Heritage Site marking the spot where Gautama Buddha attained enlightenment.",
                "Detail": "The central temple features a towering pyramidal structure housing a colossal gilded statue of Buddha sitting in earth-touching mudra beside the sacred descendant of the Bodhi Tree.",
                "Era": "3rd Century BC onwards",
                "Significance": "Holiest sanctuary of Buddhism globally"
            },
            {
                "Name": "Nalanda University Ruins",
                "Info": "The archaeological remains of one of the world's first great residential universities.",
                "Detail": "Flourishing from the 5th to 12th century AD, Nalanda was a global center of learning hosting over 10,000 students and 2,000 teachers studying medicine, astronomy, and philosophy.",
                "Era": "5th to 12th Century AD",
                "Significance": "Ancient center of global higher education"
            },
            {
                "Name": "Vishnupad Temple (Gaya)",
                "Info": "A sacred temple situated along the Phalgu river bearing the footprint of Lord Vishnu.",
                "Detail": "Built of black basalt blocks, it is a primary destination for Hindu ancestral rites (Pind Daan), featuring striking architecture and deep theological roots.",
                "Era": "Rebuilt 18th Century by Devi Ahilya Bai Holkar",
                "Significance": "Sacred Hindu shraddh ritual site"
            }
        ]
    },
    {
        "State": "Chhattisgarh",
        "Emoji": "🌳",
        "Art": "Dhokra Bell Metal Art",
        "Festival": "Bastar Dussehra",
        "Dance": "Panthi",
        "Food": "Chila",
        "Monument": "Sirpur Group of Monuments",
        "UNESCO Sites": 0,
        "Desc": "A deeply forested state known for its spectacular tribal traditions and waterfalls.",
        "Heritage_Spots": [
            {
                "Name": "Sirpur Heritage Village",
                "Info": "An ancient city of temples and monasteries dating back to the 5th-12th centuries.",
                "Detail": "Sirpur was a major Buddhist, Hindu, and Jain learning center. It features the famous Lakshmana Brick Temple, noted for its fine terracotta carvings and ancient brick architecture.",
                "Era": "5th-12th Century AD",
                "Significance": "Multireligious ancient monastic capital"
            },
            {
                "Name": "Bhoramdeo Temple Complex",
                "Info": "Often called the 'Khajuraho of Chhattisgarh', featuring classic Nagara architecture.",
                "Detail": "Surrounded by the Maikal hills, this 11th-century temple complex is dedicated to Lord Shiva and adorned with intricate stone sculptures and erotic carvings.",
                "Era": "11th Century AD",
                "Significance": "Exquisite mediaeval temple art"
            },
            {
                "Name": "Chitrakote Waterfalls",
                "Info": "Often called the 'Niagara Falls of India', located on the Indravati River.",
                "Detail": "A breathtaking horse-shoe-shaped waterfall plunging from a height of nearly 100 feet, surrounded by dense forests and deep tribal heritage locations.",
                "Era": "Natural Heritage Landmark",
                "Significance": "Geographical and cultural tourism hub"
            }
        ]
    },
    {
        "State": "Delhi (UT)",
        "Emoji": "🏛️",
        "Art": "Zardozi Embroidery",
        "Festival": "Diwali",
        "Dance": "Kathak",
        "Food": "Chole Bhature",
        "Monument": "Red Fort",
        "UNESCO Sites": 3,
        "Desc": "The capital territory, holding a millennium of history and diverse cultural assimilation.",
        "Heritage_Spots": [
            {
                "Name": "Qutub Minar Complex",
                "Info": "A towering 73-meter brick minaret built in the early 13th century.",
                "Detail": "A UNESCO World Heritage Site featuring complex Arabic inscriptions, the ancient iron pillar that has resisted rust for over 1,600 years, and early Indo-Islamic structural foundations.",
                "Era": "12th-13th Century",
                "Significance": "Early milestone of Indo-Islamic architecture"
            },
            {
                "Name": "Humayun's Tomb",
                "Info": "The grand garden-tomb of Mughal Emperor Humayun, inspiring the Taj Mahal.",
                "Detail": "Built in red sandstone and white marble, this majestic structure set inside a Persian-style Charbagh garden is a masterclass in early Mughal symmetry and architectural layout.",
                "Era": "16th Century (Mughal Empire)",
                "Significance": "Pioneering prototype of Mughal garden tombs"
            },
            {
                "Name": "Red Fort (Lal Qila)",
                "Info": "The historic fortification from which Mughal emperors ruled India.",
                "Detail": "Featuring massive red sandstone walls, Diwan-i-Aam, and Rang Mahal, it serves as the backdrop for India's national independence day flag hoisting ceremony.",
                "Era": "17th Century (Shah Jahan)",
                "Significance": "Seat of imperial power and national symbol"
            }
        ]
    },
    {
        "State": "Goa",
        "Emoji": "🏖️",
        "Art": "Azulejos Hand-painted Tiles",
        "Festival": "Goa Carnival",
        "Dance": "Fugdi",
        "Food": "Goan Fish Curry",
        "Monument": "Basilica of Bom Jesus",
        "UNESCO Sites": 1,
        "Desc": "Famous for its stunning beaches, Portuguese heritage, and vibrant nightlife.",
        "Heritage_Spots": [
            {
                "Name": "Basilica of Bom Jesus",
                "Info": "A UNESCO-listed 16th-century church holding the mortal remains of St. Francis Xavier.",
                "Detail": "Renowned for its exemplary Baroque architecture, undecorated rustic facade, and inlaid marble flooring, it stands as a pillar of Christian heritage in Asia.",
                "Era": "16th Century (Portuguese Era)",
                "Significance": "Global Catholic pilgrimage landmark"
            },
            {
                "Name": "Aguada Fort",
                "Info": "A 17th-century Portuguese fort and lighthouse overlooking the Arabian Sea.",
                "Detail": "Built to defend against Dutch and Maratha attacks, this expansive fortification features a massive historic freshwater spring that historically supplied drinking water to passing galleons.",
                "Era": "17th Century",
                "Significance": "Strategic maritime defense bastion"
            },
            {
                "Name": "Se Cathedral",
                "Info": "One of the largest churches in Asia, dedicated to Catherine of Alexandria.",
                "Detail": "Famous for its Portuguese-Manueline architecture and the massive 'Golden Bell' housed in its towering belfry, known for its rich tone.",
                "Era": "16th-17th Century",
                "Significance": "Grandeur of colonial religious art"
            }
        ]
    },
    {
        "State": "Gujarat",
        "Emoji": "🦁",
        "Art": "Bandhani",
        "Festival": "Navratri",
        "Dance": "Garba",
        "Food": "Dhokla",
        "Monument": "Rani Ki Vav",
        "UNESCO Sites": 4,
        "Desc": "The jewel of Western India, known for Asiatic lions, Rann of Kutch, and colorful festivals.",
        "Heritage_Spots": [
            {
                "Name": "Rani Ki Vav (The Queen's Stepwell)",
                "Info": "An intricately constructed subterranean stepwell in Patan.",
                "Detail": "Designed as an inverted temple highlighting the sanctity of water, its carved walls feature over 500 major sculptures of deities, avatars, and mythological motifs.",
                "Era": "11th Century (Solanki Dynasty)",
                "Significance": "Pinnacle of stepwell architectural design"
            },
            {
                "Name": "Champaner-Pavagadh Archaeological Park",
                "Info": "A UNESCO World Heritage site featuring unexcavated chalcolithic sites and a 16th-century capital.",
                "Detail": "Blending Hindu and Islamic architectural styles, it includes ancient hill fortresses, palaces, mosques, and stepwells dating from the pre-Mughal Islamic era.",
                "Era": "8th to 16th Century",
                "Significance": "Cross-cultural medieval architectural synthesis"
            },
            {
                "Name": "Sun Temple (Modhera)",
                "Info": "An architectural masterpiece dedicated to the solar deity Surya, built on the Tropic of Cancer.",
                "Detail": "Features a magnificent pillared Surya Mandir hall, an expansive stepped water tank (Kunda) lined with 108 miniature shrines, and precise solar equinox alignment.",
                "Era": "11th Century",
                "Significance": "Masterwork of Solanki temple architecture"
            }
        ]
    },
    {
        "State": "Haryana",
        "Emoji": "🚜",
        "Art": "Phulkari",
        "Festival": "Surajkund Crafts Mela",
        "Dance": "Jhumar",
        "Food": "Bajre Ki Roti",
        "Monument": "Sheikh Chilli's Tomb",
        "UNESCO Sites": 0,
        "Desc": "Historically rich state known for agriculture, ancient Vedic sites, and traditional arts.",
        "Heritage_Spots": [
            {
                "Name": "Kurukshetra Brahma Sarovar",
                "Info": "A massive sacred water tank associated with the legendary Mahabharata epic.",
                "Detail": "Revered as the holy ground where Lord Krishna delivered the Bhagavad Gita, this massive tank attracts pilgrims from across India for ritual baths during solar eclipses.",
                "Era": "Ancient Vedic Period",
                "Significance": "Epic Mahabharata spiritual ground"
            },
            {
                "Name": "Sheikh Chilli's Tomb",
                "Info": "A striking Mughal-era mausoleum complex located in Thanesar.",
                "Detail": "Dedicated to the Sufi saint Abd-ur-Rahim, popularly known as Sheikh Chilli, it features brilliant white marble construction, symmetric gardens, and Persian styles.",
                "Era": "17th Century (Mughal Era)",
                "Significance": "Fine example of provincial Sufi architecture"
            },
            {
                "Name": "Jyotisar Birthplace of Gita",
                "Info": "The historic site marked by a sacred banyan tree where the Bhagavad Gita was spoken.",
                "Detail": "A peaceful memorial site where travelers and scholars reflect on the philosophical dialogue between Krishna and Arjuna before the Kurukshetra war.",
                "Era": "Ancient Tradition",
                "Significance": "Birthplace of universal philosophical scripture"
            }
        ]
    },
    {
        "State": "Himachal Pradesh",
        "Emoji": "🏔️",
        "Art": "Kangra Painting",
        "Festival": "Kullu Dussehra",
        "Dance": "Nati",
        "Food": "Dham",
        "Monument": "Hadimba Temple",
        "UNESCO Sites": 2,
        "Desc": "The Abode of Snow, dotted with hill stations, monasteries, and immense natural beauty.",
        "Heritage_Spots": [
            {
                "Name": "Hadimba Temple (Manali)",
                "Info": "A unique wooden pagoda-style shrine nestled inside a thick Dhungri cedar forest.",
                "Detail": "Built in 1553, this temple is dedicated to Hidimba Devi, wife of Bhima from the Mahabharata, famous for its multi-tiered wooden roofs and intricate woodcarvings.",
                "Era": "16th Century (1553 AD)",
                "Significance": "Unique Himalayan wooden pagoda architecture"
            },
            {
                "Name": "Kangra Fort",
                "Info": "One of the oldest dated forts in India, built by the ancient Katoch dynasty.",
                "Detail": "Perched on a steep cliff overlooking the Banganga and Manjhi rivers, this historic fort has witnessed centuries of royal reigns, imperial attacks, and architectural expansions.",
                "Era": "Ancient to Medieval Period",
                "Significance": "Seat of the ancient Katoch rulers"
            },
            {
                "Name": "Key Monastery (Spiti Valley)",
                "Info": "A famous Tibetan Buddhist monastery perched on a hilltop at 13,668 feet.",
                "Detail": "A fortress-like religious training center housing hundreds of monks, rare murals, wind instruments, and ancient weapons belonging to the Gelugpa sect.",
                "Era": "11th Century AD",
                "Significance": "High-altitude monastic learning hub"
            }
        ]
    },
    {
        "State": "Jammu & Kashmir (UT)",
        "Emoji": "❄️",
        "Art": "Pashmina & Papier-Mache",
        "Festival": "Tulip Festival",
        "Dance": "Rouf",
        "Food": "Rogan Josh",
        "Monument": "Shalimar Bagh",
        "UNESCO Sites": 0,
        "Desc": "Paradise on earth, known for its scenic valleys, lakes, and rich Sufi heritage.",
        "Heritage_Spots": [
            {
                "Name": "Shalimar Bagh (Srinagar)",
                "Info": "A magnificent Mughal garden built by Emperor Jahangir on the banks of Dal Lake.",
                "Detail": "Known as the 'Crown of Srinagar', it features cascading water channels, polished stone pavilions, and blooming chinar trees set against snowy mountain backdrops.",
                "Era": "17th Century (Mughal Empire)",
                "Significance": "Masterpiece of Mughal landscape architecture"
            },
            {
                "Name": "Martand Sun Temple",
                "Info": "A breathtaking 8th-century ruined temple dedicated to the Sun God Surya.",
                "Detail": "Built by King Lalitaditya Muktapida, this stone temple exhibits classic Kashmiri-Classical architecture with colonnaded courtyards overlooking the entire Kashmir valley.",
                "Era": "8th Century AD",
                "Significance": "Pinnacle of ancient Kashmiri stone architecture"
            },
            {
                "Name": "Pari Mahal (Srinagar)",
                "Info": "A historic seven-terraced garden overlooking the Dal Lake and Srinagar city.",
                "Detail": "Originally a Buddhist monastery later converted into an observatory and garden by Dara Shikoh, patron of arts and eldest son of Emperor Shah Jahan.",
                "Era": "17th Century",
                "Significance": "Mughal terrace gardening and astronomy history"
            }
        ]
    },
    {
        "State": "Jharkhand",
        "Emoji": "🌿",
        "Art": "Paitkar Painting",
        "Festival": "Sarhul",
        "Dance": "Chhau",
        "Food": "Dhuska",
        "Monument": "Baidyanath Temple",
        "UNESCO Sites": 0,
        "Desc": "The Land of Forests, rich in minerals and deep-rooted indigenous tribal heritage.",
        "Heritage_Spots": [
            {
                "Name": "Baidyanath Temple (Deoghar)",
                "Info": "One of the twelve sacred Jyotirlingas of Lord Shiva.",
                "Detail": "A major pilgrimage center where devotees gather during the Shravan Mela, carrying holy Ganges water over long distances on foot to offer to the deity.",
                "Era": "Ancient / Medieval Shrine",
                "Significance": "Premier Shaivite pilgrimage shrine"
            },
            {
                "Name": "Maliti & Rajrappa Temple Complex",
                "Info": "A scenic confluence shrine dedicated to Goddess Chhinnamasta.",
                    "Detail": "Located where the Damodar and Bhairavi rivers meet, this site combines unique tantric iconography with a roaring waterfall and deep forest terrain.",
                "Era": "Mediaeval Tradition",
                "Significance": "Tantric Shakti pilgrimage point"
            },
            {
                "Name": "McCluskieganj",
                "Info": "A unique historic Anglo-Indian township established during the British Raj.",
                "Detail": "Dotted with decaying colonial-style bungalows, quiet woods, and orchards, it offers a glimpse into a multicultural settlement experiment from the early 20th century.",
                "Era": "1930s (British Era)",
                "Significance": "Unique socio-cultural colonial settlement"
            }
        ]
    },
    {
        "State": "Karnataka",
        "Emoji": "🐘",
        "Art": "Mysore Silk Weaving",
        "Festival": "Mysuru Dasara",
        "Dance": "Yakshagana",
        "Food": "Bisi Bele Bath",
        "Monument": "Hampi Ruins",
        "UNESCO Sites": 3,
        "Desc": "A blend of modernity and antiquity, home to sprawling empires and classical music.",
        "Heritage_Spots": [
            {
                "Name": "Hampi Ruins",
                "Info": "The magnificent medieval capital of the Vijayanagara Empire.",
                "Detail": "A sprawling UNESCO World Heritage landscape filled with boulder-strewn hills, stone chariots, musical pillars, and grand temple complexes like Virupaksha and Vittala.",
                "Era": "14th-16th Century (Vijayanagara)",
                "Significance": "Global archaeological empire capital"
            },
            {
                "Name": "Mysore Palace",
                "Info": "The majestic royal residence of the Wadiyar dynasty.",
                "Detail": "A glowing spectacle of Indo-Saracenic architecture, featuring sprawling courtyards, stained glass, golden domes, and illuminated during the grand Dasara festival.",
                "Era": "20th Century Rebuild (Wadiyar Dynasty)",
                "Significance": "Masterpiece of royal Indo-Saracenic design"
            },
            {
                "Name": "Badami Cave Temples",
                "Info": "A complex of four rock-cut Hindu and Jain cave temples carved out of red sandstone cliffs.",
                "Detail": "Dating back to the Chalukya dynasty of the 6th century, these caves feature rich relief carvings of deities like Nataraja, Vishnu, and Mahavira overlooking a scenic lake.",
                "Era": "6th Century AD (Chalukya Empire)",
                "Significance": "Early Chalukya rock-cut temple heritage"
            }
        ]
    },
    {
        "State": "Kerala",
        "Emoji": "🌴",
        "Art": "Mural Painting",
        "Festival": "Onam",
        "Dance": "Kathakali",
        "Food": "Sadya",
        "Monument": "Padmanabhaswamy Temple",
        "UNESCO Sites": 1,
        "Desc": "God's Own Country — famous for backwaters, Ayurveda, and classical dance dramas.",
        "Heritage_Spots": [
            {
                "Name": "Sree Padmanabhaswamy Temple",
                "Info": "An ancient temple in Thiruvananthapuram dedicated to Lord Vishnu.",
                "Detail": "Renowned for its striking blend of Kerala and Dravidian architecture, grand corridor pillars featuring thousands of carved figures, and immense historical temple treasures.",
                "Era": "Ancient / Rebuilt 18th Century",
                "Significance": "Architectural and spiritual landmark"
            },
            {
                "Name": "Fort Kochi & Chinese Fishing Nets",
                "Info": "A historic coastal enclave featuring colonial history and backwater views.",
                "Detail": "A melting pot of Portuguese, Dutch, and British colonial influences, highlighted by iconic cantilevered Chinese fishing nets along the coastline and historic churches.",
                "Era": "15th Century onwards",
                "Significance": "Early European trading port heritage"
            },
            {
                "Name": "Mattancherry Palace (Dutch Palace)",
                "Info": "A mediaeval palace featuring exquisite Kerala mural paintings.",
                "Detail": "Gifted by the Portuguese to the Raja of Cochin, it contains stunning ceiling murals illustrating Hindu epics like the Ramayana alongside traditional royal furniture.",
                "Era": "16th Century",
                "Significance": "Pinnacle of traditional Kerala mural art"
            }
        ]
    },
    {
        "State": "Madhya Pradesh",
        "Emoji": "🐅",
        "Art": "Gond Art",
        "Festival": "Lokrang Festival",
        "Dance": "Matki",
        "Food": "Poha Jalebi",
        "Monument": "Khajuraho Monuments",
        "UNESCO Sites": 3,
        "Desc": "The Heart of India, known for its tiger reserves, ancient temples, and stupas.",
        "Heritage_Spots": [
            {
                "Name": "Khajuraho Group of Monuments",
                "Info": "A UNESCO World Heritage site famed for its exquisite Nagara-style architecture.",
                "Detail": "Built by the Chandela dynasty between 950 and 1050 AD, these temples feature breathtaking fine sandstone sculptures reflecting life, love, music, and spirituality.",
                "Era": "10th-11th Century (Chandela Dynasty)",
                "Significance": "World-renowned mediaeval temple sculpture"
            },
            {
                "Name": "Sanchi Stupa",
                "Info": "The oldest stone Buddhist monument in India, commissioned by Emperor Ashoka.",
                "Detail": "A serene hilltop complex housing sacred relics of the Buddha, surrounded by intricately carved stone toranas (gateways) depicting stories from Jataka tales.",
                "Era": "3rd Century BC to 1st Century AD",
                "Significance": "Foundational Buddhist architectural site"
            },
            {
                "Name": "Gwalior Fort",
                "Info": "A massive hill fort described by Mughal emperor Babur as 'the pearl among fortresses in Hind'.",
                "Detail": "Enclosing historic palaces like the Man Mandir Palace with blue ceramic tile work, Jain rock-cut statues, and ancient water tanks carved out of rock.",
                "Era": "8th Century onwards",
                "Significance": "Impregnable central Indian hill fortress"
            }
        ]
    },
    {
        "State": "Maharashtra",
        "Emoji": "🏰",
        "Art": "Warli Painting",
        "Festival": "Ganesh Chaturthi",
        "Dance": "Lavani",
        "Food": "Vada Pav",
        "Monument": "Gateway of India",
        "UNESCO Sites": 6,
        "Desc": "India's financial powerhouse with deep-rooted Maratha history, caves, and coastline.",
        "Heritage_Spots": [
            {
                "Name": "Ajanta and Ellora Caves",
                "Info": "UNESCO World Heritage rock-cut cave monuments carved out of basaltic cliffs.",
                "Detail": "Ellora features the magnificent monolithic Kailash Temple (Cave 16) carved entirely top-down from a single rock, while Ajanta preserves world-famous ancient Buddhist murals.",
                "Era": "2nd Century BC to 10th Century AD",
                "Significance": "Masterpiece of Indian rock-cut cave art"
            },
            {
                "Name": "Chhatrapati Shivaji Maharaj Terminus",
                "Info": "A historic railway station and UNESCO World Heritage Site in Mumbai.",
                "Detail": "An architectural masterpiece blending Victorian Gothic Revival architecture with traditional Indian palace stone domes, turrets, and ironwork grilles.",
                "Era": "19th Century (British Era / F.W. Stevens)",
                "Significance": "Pinnacle of Victorian-Gothic railway architecture"
            },
            {
                "Name": "Raigad Fort",
                "Info": "The historic hill fortress and capital of Chhatrapati Shivaji Maharaj.",
                "Detail": "Perched 2,700 feet high in the Sahyadri mountains, this fort witnessed the coronation of the great Maratha king and serves as a symbol of Maratha pride and swaraj.",
                "Era": "17th Century (Maratha Empire)",
                "Significance": "Historic capital seat of the Maratha Empire"
            }
        ]
    },
    {
        "State": "Manipur",
        "Emoji": "🦌",
        "Art": "Kauna Reed Craft",
        "Festival": "Yaoshang",
        "Dance": "Manipuri",
        "Food": "Eromba",
        "Monument": "Kangla Fort",
        "UNESCO Sites": 0,
        "Desc": "The Jewel of India, famous for its floating national park, classical dance, and sports.",
        "Heritage_Spots": [
            {
                "Name": "Kangla Fort",
                "Info": "The historic capital seat of the ancient rulers of Manipur.",
                "Detail": "Surrounded by a moat, this ancient site holds immense spiritual and political importance, housing sacred temples, archaeological ruins, and historical royal coronation grounds.",
                "Era": "Ancient to 19th Century",
                "Significance": "Ancient political and spiritual capital of Meitei kings"
            },
            {
                "Name": "Loktak Lake & Sendra Island",
                "Info": "The largest freshwater lake in Northeast India, famous for floating 'phumdis'.",
                "Detail": "Home to Keibul Lamjao National Park—the world's only floating national park and last natural refuge of the endangered Sangai brow-antlered deer.",
                "Era": "Geological Heritage",
                "Significance": "Unique floating wetland ecosystem"
            },
            {
                "Name": "Ibudhou Thangjing Temple (Moirang)",
                "Info": "An ancient sacred shrine dedicated to the pre-Hindu deity Lord Thangjing.",
                "Detail": "A crucial centre for traditional folklore, ritual music, and the origin site of the classical Khamba-Thoibi dance drama embedded deeply in Manipuri culture.",
                "Era": "Ancient Tradition",
                "Significance": "Epic center of classical Meitei mythology"
            }
        ]
    },
    {
        "State": "Meghalaya",
        "Emoji": "🌧️",
        "Art": "Cane and Bamboo Craft",
        "Festival": "Wangala",
        "Dance": "Nongkrem",
        "Food": "Jadoh",
        "Monument": "Living Root Bridges",
        "UNESCO Sites": 0,
        "Desc": "Abode of Clouds, showcasing matrilineal society and unparalleled monsoon landscapes.",
        "Heritage_Spots": [
            {
                "Name": "Living Root Bridges (Nongriat)",
                "Info": "Bridges grown organically out of aerial roots of rubber fig trees.",
                "Detail": "A stunning example of bio-engineering practiced by the Khasi people over centuries, growing stronger over time across rushing jungle streams and deep valleys.",
                "Era": "Centuries-old indigenous practice",
                "Significance": "Pioneering sustainable natural bio-architecture"
            },
            {
                "Name": "Mawlynnong Village",
                "Info": "Acclaimed as 'God's Own Garden' and cleanest village in Asia.",
                "Detail": "Renowned for community-driven waste management, bamboo dustbins, blooming flower-lined paths, and a unique 85-foot high living root observation tower.",
                "Era": "Traditional Khasi Settlement",
                "Significance": "Global model for community cleanliness and eco-tourism"
            },
            {
                "Name": "Nartiang Monoliths",
                "Info": "A collection of ancient megaliths scattered across Jaintia hills.",
                "Detail": "Believed to be the densest collection of megalithic stones in the world, erected by the local tribal chieftains in the 16th century to commemorate historical figures.",
                "Era": "16th Century AD",
                "Significance": "Largest megalithic collection in the region"
            }
        ]
    },
    {
        "State": "Mizoram",
        "Emoji": "🎋",
        "Art": "Bamboo Weaving",
        "Festival": "Chapchar Kut",
        "Dance": "Cheraw (Bamboo Dance)",
        "Food": "Bai",
        "Monument": "Solomon's Temple",
        "UNESCO Sites": 0,
        "Desc": "Land of the Hill People, draped in rolling hills, valleys, and vibrant bamboo culture.",
        "Heritage_Spots": [
            {
                "Name": "Solomon's Temple (Aizawl)",
                "Info": "A grand white marble church standing as a modern architectural landmark.",
                "Detail": "Built over several years by a local socio-religious group, its sprawling white marble premises and tranquil surroundings draw thousands of visitors and worshippers.",
                "Era": "Modern Era (Completed 2017)",
                "Significance": "Major modern architectural and spiritual landmark"
            },
            {
                "Name": "Reiek Heritage Village",
                "Info": "A cultural hub showcasing traditional Mizo hill life and huts.",
                "Detail": "Perched on the Reiek peak, it provides panoramic views of rolling green valleys and hosts traditional tribal festival celebrations and indigenous folk displays.",
                "Era": "Traditional Mizo Settlement",
                "Significance": "Preservation of indigenous Mizo architecture"
            },
            {
                "Name": "Vantawng Waterfalls & Cultural Groves",
                "Info": "The highest waterfall in Mizoram surrounded by lush undisturbed forests.",
                "Detail": "Plunging from over 750 feet amidst bamboo jungles, it holds rich folklore ties to local tribal legends and natural sacred groves.",
                "Era": "Natural Heritage",
                "Significance": "Highest uninterrupted cascade in the state"
            }
        ]
    },
    {
        "State": "Nagaland",
        "Emoji": "🦅",
        "Art": "Naga Shawls",
        "Festival": "Hornbill Festival",
        "Dance": "Chang Lo",
        "Food": "Smoked Pork",
        "Monument": "Kachari Ruins",
        "UNESCO Sites": 0,
        "Desc": "Famous for its diverse indigenous tribes, warrior traditions, and the Hornbill Festival.",
        "Heritage_Spots": [
            {
                "Name": "Kisama Heritage Village",
                "Info": "The permanent venue for the world-renowned annual Hornbill Festival.",
                "Detail": "Designed like a traditional Naga village, it features morungs (dormitories) representing each major tribe, displaying tribal arts, crafts, war gear, and dances.",
                "Era": "Modern Cultural Village",
                "Significance": "Unified cultural showcase of all Naga tribes"
            },
            {
                "Name": "Dimapur Kachari Ruins",
                "Info": "Mysterious medieval mushroom-domed monoliths built by the Dimasa Kachari kingdom.",
                "Detail": "Dating back to the 10th century, these curious cylindrical stone pillars carved with intricate patterns stand as relics of an ancient kingdom's architecture.",
                "Era": "10th-13th Century AD",
                "Significance": "Relics of the mediaeval Dimasa Kachari kingdom"
            },
            {
                "Name": "Khonoma Green Village",
                "Info": "Asia's first green village known for its historic Angami warrior resistance.",
                "Detail": "Famous for community conservation of forests, terrace farming, and historic stone fortification walls that once resisted British colonial forces.",
                "Era": "19th Century Historical Site",
                "Significance": "Pioneering eco-conservation and tribal valor"
            }
        ]
    },
    {
        "State": "Odisha",
        "Emoji": "☸️",
        "Art": "Pattachitra",
        "Festival": "Rath Yatra",
        "Dance": "Odissi",
        "Food": "Dalma",
        "Monument": "Konark Sun Temple",
        "UNESCO Sites": 1,
        "Desc": "Known for architectural grandeur, ancient Kalinga history, and coastal beauty.",
        "Heritage_Spots": [
            {
                "Name": "Konark Sun Temple",
                "Info": "A 13th-century UNESCO World Heritage architectural marvel shaped like a colossal chariot.",
                "Detail": "Built by King Narasimhadeva I, it features 24 giant carved stone wheels serving as working sundials alongside delicate stone horses and mythological motifs.",
                "Era": "13th Century AD (Eastern Ganga Dynasty)",
                "Significance": "Masterpiece of Kalinga stone architecture"
            },
            {
                "Name": "Jagannath Temple (Puri)",
                "Info": "One of the Char Dham holy Hindu pilgrimage sites.",
                "Detail": "Famous for its towering Kalinga architecture and the grand annual Rath Yatra (Chariot Festival), where massive wooden chariots pull deities through the streets.",
                "Era": "12th Century AD",
                "Significance": "Global center of Jagannath worship and rath rituals"
            },
            {
                "Name": "Lingaraj Temple (Bhubaneswar)",
                "Info": "A majestic 11th-century temple dedicated to Lord Shiva, epitome of Kalinga design.",
                "Detail": "Standing 180 feet tall, its expansive stone courtyard contains over 50 smaller shrines showcasing the pinnacle of Somavamshi temple construction.",
                "Era": "11th Century AD",
                "Significance": "Architectural prototype of Bhubaneswar temple city"
            }
        ]
    },
    {
        "State": "Punjab",
        "Emoji": "🌾",
        "Art": "Phulkari",
        "Festival": "Baisakhi",
        "Dance": "Bhangra",
        "Food": "Makki di Roti",
        "Monument": "Golden Temple",
        "UNESCO Sites": 0,
        "Desc": "Land of five rivers, vibrant with energetic folk dances and Sikh heritage.",
        "Heritage_Spots": [
            {
                "Name": "The Golden Temple (Sri Harmandir Sahib)",
                "Info": "The spiritual and cultural center of Sikhism located in Amritsar.",
                "Detail": "Surrounded by the holy pool of Amrit Sarovar, the shrine's upper floors are covered in pure gold leaf, welcoming millions of visitors daily to its community kitchen (langar).",
                "Era": "16th-19th Century",
                "Significance": "Holies sanctuary of Sikhism worldwide"
            },
            {
                "Name": "Jallianwala Bagh",
                "Info": "A historic public garden and national memorial to a tragic colonial massacre.",
                "Detail": "Preserves bullet marks on ancient walls and the martyrs' well, serving as a solemn reminder of India's freedom struggle under British colonial rule.",
                "Era": "1919 (British Era Massacre Site)",
                "Significance": "Turning point in India's freedom movement"
            },
            {
                "Name": "Qila Mubarak (Patiala)",
                "Info": "A grand mediaeval fortress complex at the heart of Patiala city.",
                "Detail": "Built by Baba Ala Singh, founder of the Patiala state, featuring Sikh-Mughal architectural synthesis, royal guest houses, and subterranean treasury halls.",
                "Era": "18th Century",
                "Significance": "Historic royal seat of the Phulkian rulers"
            }
        ]
    },
    {
        "State": "Rajasthan",
        "Emoji": "🏰",
        "Art": "Miniature Painting",
        "Festival": "Pushkar Camel Fair",
        "Dance": "Ghoomar",
        "Food": "Dal Baati Churma",
        "Monument": "Amber Fort",
        "UNESCO Sites": 9,
        "Desc": "Known for its majestic forts, vibrant Rajputana culture, and desert festivals.",
        "Heritage_Spots": [
            {
                "Name": "Amber Fort & Palace (Jaipur)",
                "Info": "A majestic hilltop fortress built with red sandstone and white marble.",
                "Detail": "Overlooking Maota Lake, it features sprawling mirror-inlaid halls (Sheesh Mahal), grand courtyards, and deep Rajput-Mughal architectural synthesis.",
                "Era": "16th Century (Kachwaha Rajputs)",
                "Significance": "Grand example of Rajput hill fort architecture"
            },
            {
                "Name": "Mehrangarh Fort (Jodhpur)",
                "Info": "One of the largest forts in India, towering 400 feet above the blue city.",
                "Detail": "Enclosing grand palaces with intricate lattice windows and courtyards, housing historical armories, palanquins, and fine miniature paintings.",
                "Era": "15th Century onwards (Rathore Clan)",
                "Significance": "Formidable desert citadel of Marwar"
            },
            {
                "Name": "Chittorgarh Fort",
                "Info": "The largest fort in India, symbolizing Rajput valor, sacrifice, and romance.",
                "Detail": "Sprawling across a 700-acre hill, it features massive victory towers (Kirti Stambh and Vijay Stambh), royal water reservoirs, and historic palaces.",
                "Era": "7th to 16th Century",
                "Significance": "Symbol of legendary Rajput courage and history"
            }
        ]
    },
    {
        "State": "Sikkim",
        "Emoji": "🏔️",
        "Art": "Thangka Painting",
        "Festival": "Losoong",
        "Dance": "Singhi Chham",
        "Food": "Momo",
        "Monument": "Rumtek Monastery",
        "UNESCO Sites": 1,
        "Desc": "India's first fully organic state, known for its snow-capped peaks and Buddhist culture.",
        "Heritage_Spots": [
            {
                "Name": "Rumtek Monastery",
                "Info": "The largest and most spiritually significant monastery in Sikkim.",
                "Detail": "Serving as the seat-in-exile of the Karmapa Lama, it houses sacred Buddhist relics, golden stupas, and vibrant traditional Tibetan wall paintings.",
                "Era": "16th Century / Rebuilt 20th Century",
                "Significance": "Primary seat of the Karma Kagyu lineage"
            },
            {
                "Name": "Pemayangtse Monastery",
                "Info": "One of the oldest and premier monasteries of the Nyingma order in Sikkim.",
                "Detail": "Perched on a ridge facing snowy Himalayan ranges, it houses a famous seven-tiered wooden sculpture depicting Guru Rinpoche's celestial palace (Zangdokpalri).",
                "Era": "1705 AD",
                "Significance": "Ancient Nyingma monastic heritage"
            },
            {
                "Name": "Rabdentse Ruins",
                "Info": "The archaeological remains of the second capital of the Kingdom of Sikkim.",
                "Detail": "Overlooking the scenic valley and Khangchendzonga peak, these stone ruins offer a glimpse into the royal dynasty's historic seat before its relocation.",
                "Era": "17th to 18th Century",
                "Significance": "Ancient royal capital archaeological site"
            }
        ]
    },
    {
        "State": "Tamil Nadu",
        "Emoji": "🛕",
        "Art": "Tanjore Painting",
        "Festival": "Pongal",
        "Dance": "Bharatanatyam",
        "Food": "Sambar & Dosa",
        "Monument": "Meenakshi Temple",
        "UNESCO Sites": 6,
        "Desc": "Home to Dravidian temple architecture and one of the oldest classical dance forms.",
        "Heritage_Spots": [
            {
                "Name": "Meenakshi Amman Temple (Madurai)",
                "Info": "A historic Hindu temple complex featuring towering multicolored gopurams.",
                "Detail": "Adorned with thousands of brightly painted mythological stone sculptures, hall columns, and sacred water tanks dedicated to Goddess Meenakshi.",
                "Era": "Ancient / Rebuilt 17th Century (Nayak Dynasty)",
                "Significance": "Masterpiece of Dravidian temple town planning"
            },
            {
                "Name": "Brihadeeswarar Temple (Thanjavur)",
                "Info": "A UNESCO World Heritage Chola temple built over 1,000 years ago.",
                "Detail": "Masterminded by King Rajaraja I, its massive granite vimana tower stands tall without mortar, capped by a single stone cupola weighing over 80 tons.",
                "Era": "11th Century AD (Chola Empire)",
                "Significance": "Pinnacle of Great Living Chola Temples"
            },
            {
                "Name": "Shore Temple (Mahabalipuram)",
                "Info": "A UNESCO World Heritage 8th-century structural temple overlooking the Bay of Bengal.",
                "Detail": "Built by the Pallava dynasty using blocks of granite, it stands resilient against ocean winds, showcasing early Dravidian rock-cut and structural mastery.",
                "Era": "8th Century AD (Pallava Dynasty)",
                "Significance": "Ancient coastal monolithic architecture"
            }
        ]
    },
    {
        "State": "Telangana",
        "Emoji": "🕌",
        "Art": "Cheriyal Scroll Painting",
        "Festival": "Bathukamma",
        "Dance": "Perini Shivatandavam",
        "Food": "Hyderabadi Biryani",
        "Monument": "Charminar",
        "UNESCO Sites": 1,
        "Desc": "Known for its fusion of Persian and Indian heritage, historic forts, and distinct cuisine.",
        "Heritage_Spots": [
            {
                "Name": "Charminar (Hyderabad)",
                "Info": "An iconic 16th-century monument and mosque featuring four grand minarets.",
                "Detail": "Built by Muhammad Quli Qutb Shah at the heart of the old city, it overlooks bustling bazaars, pearl markets, and rich Qutb Shahi architecture.",
                "Era": "16th Century (Qutb Shahi Dynasty)",
                "Significance": "Global architectural symbol of Hyderabad"
            },
            {
                "Name": "Golconda Fort",
                "Info": "A massive medieval fortress renowned for its acoustic design and diamond history.",
                "Detail": "Famous for its clapping-portico acoustics where a hand-clap at the entrance can be heard at the hill summit, and for once housing world-famous gems like the Koh-i-Noor.",
                "Era": "13th to 17th Century",
                "Significance": "Historic diamond trade hub and military fort"
            },
            {
                "Name": "Kakatiya Rudreshwara (Ramappa) Temple",
                "Info": "A UNESCO World Heritage temple renowned for its floating lightweight bricks.",
                "Detail": "Built in the 13th century during the Kakatiya rule, its intricately carved black basalt pillars and sandbox foundation technology have withstood major earthquakes.",
                "Era": "13th Century AD (Kakatiya Dynasty)",
                "Significance": "UNESCO-listed marvel of Kakatiya engineering"
            }
        ]
    },
    {
        "State": "Tripura",
        "Emoji": "🍍",
        "Art": "Bamboo Handicrafts",
        "Festival": "Kharchi Puja",
        "Dance": "Hojagiri",
        "Food": "Mui Borok",
        "Monument": "Ujjayanta Palace",
        "UNESCO Sites": 0,
        "Desc": "A princely state of the past, featuring grand palaces, rock carvings, and tribal rhythms.",
        "Heritage_Spots": [
            {
                "Name": "Ujjayanta Palace (Agartala)",
                "Info": "A royal palace featuring Mughal-style gardens and neoclassical architecture.",
                "Detail": "Built by Maharaja Radha Kishore Manikya in the early 20th century, it now serves as the State Museum showcasing royal artifacts and tribal heritage.",
                "Era": "Early 20th Century (1901 AD)",
                "Significance": "Royal palace and premier state museum"
            },
            {
                "Name": "Unakoti Rock Carvings",
                "Info": "An ancient Shaivite pilgrimage site featuring giant rock-cut relief sculptures.",
                "Detail": "Hidden in a forested hill range, Unakoti houses hundreds of massive stone and rock-cut figures of Hindu deities dating back to the 7th–9th centuries.",
                "Era": "7th to 9th Century AD",
                "Significance": "Mysterious ancient forest rock sculpture site"
            },
            {
                "Name": "Neermahal (Water Palace)",
                "Info": "A royal palace built in the middle of the Rudrasagar Lake.",
                "Detail": "Constructed as a summer resort for Maharaja Bir Bikram Kishore Manikya, it blends Hindu and Islamic architectural styles across a picturesque lake setting.",
                "Era": "1930s (Manikya Dynasty)",
                "Significance": "Unique royal water palace architecture"
            }
        ]
    },
    {
        "State": "Uttar Pradesh",
        "Emoji": "🕌",
        "Art": "Chikankari",
        "Festival": "Kumbh Mela",
        "Dance": "Kathak",
        "Food": "Awadhi Cuisine",
        "Monument": "Taj Mahal",
        "UNESCO Sites": 3,
        "Desc": "Cradle of ancient civilisation with Mughal architecture and spiritual pilgrimage sites.",
        "Heritage_Spots": [
            {
                "Name": "Taj Mahal (Agra)",
                "Info": "A UNESCO World Heritage white marble mausoleum and symbol of eternal love.",
                "Detail": "Built by Emperor Shah Jahan for his wife Mumtaz Mahal, it features complex pietra dura gemstone inlay work and symmetrical reflection gardens.",
                "Era": "17th Century (Mughal Empire)",
                "Significance": "Global wonder of architectural symmetry and romance"
            },
            {
                "Name": "Varanasi Ghats & Kashi Vishwanath",
                "Info": "One of the oldest continuously inhabited living cities in the world.",
                "Detail": "Sprawling along the crescent banks of the holy Ganges River, famous for its spiritual rituals, morning boat rides, and the grand evening Ganga Aarti.",
                "Era": "Ancient Living City",
                "Significance": "Spiritual heartland of ancient Indian civilization"
            },
            {
                "Name": "Fatehpur Sikri",
                "Info": "A UNESCO World Heritage fortified ghost city built by Mughal Emperor Akbar.",
                "Detail": "Featuring red sandstone palaces, Buland Darwaza, and the marble tomb of Sufi saint Salim Chishti, it was briefly the grand capital of the Mughal Empire.",
                "Era": "16th Century (Akbar's Reign)",
                "Significance": "Masterpiece of Mughal imperial town planning"
            }
        ]
    },
    {
        "State": "Uttarakhand",
        "Emoji": "🏞️",
        "Art": "Aipan Art",
        "Festival": "Maha Kumbh Mela",
        "Dance": "Langvir Nritya",
        "Food": "Kafuli",
        "Monument": "Kedarnath Temple",
        "UNESCO Sites": 1,
        "Desc": "The Land of Gods (Devbhoomi), famous for Himalayan treks and sacred pilgrimage sites.",
        "Heritage_Spots": [
            {
                "Name": "Kedarnath Temple",
                "Info": "A sacred 8th-century stone shrine dedicated to Lord Shiva in the high Himalayas.",
                "Detail": "Part of the holy Chota Char Dham pilgrimage circuit, surrounded by snow peaks and glacial valleys near the Mandakini river source.",
                "Era": "8th Century AD (Adi Shankaracharya origin)",
                "Significance": "High-altitude holy Jyotirlinga shrine"
            },
            {
                "Name": "Valley of Flowers National Park",
                "Info": "A UNESCO World Heritage Site known for endemic alpine flowers and meadows.",
                "Detail": "A vibrant valley opening up after the monsoon, filled with colorful rare flora, rich Himalayan wildlife, and picturesque mountain trails.",
                "Era": "Natural Ecological Reserve",
                "Significance": "Global biodiversity and floral hotspot"
            },
            {
                "Name": "Tungnath Temple",
                "Info": "The highest Shiva temple in the world, located at 12,073 feet.",
                "Detail": "The highest of the Panch Kedar temples, offering panoramic views of major Himalayan peaks like Nanda Devi and Chaukhamba.",
                "Era": "Mediaeval Himalayan Heritage",
                "Significance": "Highest altitude Shaivite temple structure"
            }
        ]
    },
    {
        "State": "West Bengal",
        "Emoji": "🎭",
        "Art": "Patachitra",
        "Festival": "Durga Puja",
        "Dance": "Chhau",
        "Food": "Rosogolla",
        "Monument": "Victoria Memorial",
        "UNESCO Sites": 3,
        "Desc": "Rich literary and artistic legacy, celebrated for Durga Puja and Rabindra Sangeet.",
        "Heritage_Spots": [
            {
                "Name": "Victoria Memorial (Kolkata)",
                "Info": "A grand British-era white marble monument and museum in Kolkata.",
                "Detail": "Blending British and Mughal architecture, it stands amid manicured gardens housing royal galleries, historical paintings, and statues.",
                "Era": "Early 20th Century (British Raj)",
                "Significance": "Grand colonial landmark and historical museum"
            },
            {
                "Name": "Sundarbans National Park",
                "Info": "A UNESCO World Heritage mangrove forest reserve shared with Bangladesh.",
                "Detail": "Home to the largest delta on earth, famous for the majestic Royal Bengal tigers, estuarine crocodiles, and winding network of tidal waterways.",
                "Era": "Natural Biosphere Reserve",
                "Significance": "Largest coastal mangrove tiger reserve globally"
            },
            {
                "Name": "Terracotta Temples of Bishnupur",
                "Info": "A cluster of unique 17th-century terracotta brick temples built by the Malla kings.",
                "Detail": "Adorned with intricate terracotta tile carvings depicting scenes from Hindu epics on curved chala-style Bengali roofs.",
                "Era": "17th-18th Century (Malla Dynasty)",
                "Significance": "Unique regional terracotta temple architecture"
            }
        ]
    }
]

df_heritage = pd.DataFrame(heritage_raw_data)
# Sort alphabetically to keep the dropdown clean
df_heritage = df_heritage.sort_values(by="State").reset_index(drop=True)

# 30 Questions representing all 28 states + 2 UTs

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.markdown("## 🇮🇳 Digital Heritage")
st.sidebar.title("🧭 Navigate")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Explore States","Heritage Explorer", "AI Cultural Guide", "Cultural Quiz", "Contribute", "About Project"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Project Goal")
st.sidebar.info("Digitally document, promote, and gamify India's cultural heritage so youth engage with tradition through technology.")
st.sidebar.markdown("### 👨‍💻 Built by")
st.sidebar.write("II Year CSE Students — SIH Prototype")

# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------
if page == "Home":
    col1, col2, col3, col4 = st.columns(4)
    stats = [("28+", "States & UTs"), ("40+", "UNESCO Sites"), ("100+", "Dance Forms"), ("1000+", "Festivals")]
    for col, (num, label) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f'<div class="stat-box"><h2>{num}</h2><p>{label}</p></div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("""
    <div class="info-card">
    <h3>🌏 Why This Matters</h3>
    India's traditions passed through generations remain scattered or undocumented. <b>Digital Heritage Explorer</b> brings this heritage online—interactive, searchable, and fun to learn.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("✨ Featured Heritage Snapshot")
    # Show 3 random states to make the homepage dynamic
    sampled_states = df_heritage.sample(3).reset_index(drop=True)
    cols = st.columns(3)
    for i, row in sampled_states.iterrows():
        with cols[i]:
            st.markdown(f"""
            <div class="culture-card">
                <h3>{row['Emoji']} {row['State']}</h3>
                <p>{row['Desc']}</p>
                <p>🏛️ <b>{row['Monument']}</b></p>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------
# EXPLORE STATES PAGE
# ---------------------------------------------------------
# ---------------------------------------------------------
# EXPLORE STATES PAGE
# ---------------------------------------------------------
elif page == "Explore States":
  st.header("🗺️ Explore Indian States & Their Heritage")

  state_list = df_heritage['State'].tolist()
  selected_state = st.selectbox('Choose a state to explore:', state_list)

  state_info = df_heritage[df_heritage['State'] == selected_state].iloc[0]

  st.markdown(f'## {state_info["Emoji"]} {selected_state}')
  st.write(state_info['Desc'])

  c1, c2, c3 = st.columns(3)
  c1.markdown(f"**🎨 Art Form**\n\n{state_info['Art']}")
  c2.markdown(f"**🎉 Famous Festival**\n\n{state_info['Festival']}")
  c3.markdown(f"**💃 Dance Form**\n\n{state_info['Dance']}")

  c4, c5 = st.columns(2)
  c4.markdown(f"**🍛 Signature Food**\n\n{state_info['Food']}")
  c5.markdown(f"**🏛️ Iconic Monument**\n\n{state_info['Monument']}")

  # --- NEW: Heritage Places to Visit Section ---
  st.markdown('---')
  st.subheader('🏛️ Famous Heritage Places to Visit')

  # Check if the selected state has detailed heritage spots in its dictionary
  if (
      'Heritage_Spots' in state_info
      and isinstance(state_info['Heritage_Spots'], list)
      and len(state_info['Heritage_Spots']) > 0
  ):
    for spot in state_info['Heritage_Spots']:
      st.markdown(f'#### 📍 {spot["Name"]}')
      st.write(spot['Info'])

      # Read More Button using Streamlit Expander
      with st.expander(f'📖 Read More about {spot["Name"]}'):
        st.write(spot['Detail'])
      st.markdown('')
  else:
    st.info(
        f'Detailed heritage location logs for {selected_state} are currently'
        ' being updated!'
    )
  # ---------------------------------------------

  st.markdown('---')
  st.subheader('🔍 Compare States')
  compare = st.multiselect(
      'Select states to compare', state_list, default=[selected_state]
  )
  if compare:
    df_comparison = df_heritage[df_heritage['State'].isin(compare)].drop(
        columns=['Emoji', 'Desc', 'Heritage_Spots'], errors='ignore'
    )
    st.table(df_comparison.set_index('State'))

# ---------------------------------------------------------
# DASHBOARD PAGE
# ---------------------------------------------------------
elif page == "Heritage Explorer":
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
                            height: 300px;
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
        st.markdown(f'<img src="{data["img"]}" referrerpolicy="no-referrer" style="width: 100%; height: 100%; border-radius:10px; margin: 0; padding: 0">', unsafe_allow_html=True)

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
# ---------------------------------------------------------
# CONTRIBUTE PAGE
# ---------------------------------------------------------
elif page == "Contribute":
    st.header("📝 Contribute a Tradition")
    st.write("Help us grow this heritage archive! Share a tradition, festival, or art form from your region.")

    with st.form("contribute_form", clear_on_submit=True):
        name = st.text_input("Your Name")
        state = st.selectbox("State / Region", df_heritage['State'].tolist() + ["Other"])
        category = st.selectbox("Category", ["Art", "Dance", "Festival", "Food", "Monument", "Folklore", "Other"])
        description = st.text_area("Describe the tradition")
        submitted = st.form_submit_button("Submit Contribution 🚀")

        if submitted:
            if name and state and description:
                st.success(f"🙏 Thank you {name}! Your entry on **{category}** from **{state}** has been recorded.")
                st.info(f"Submitted on: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
            else:
                st.error("Please fill in all required fields before submitting.")

# ---------------------------------------------------------
# ABOUT PAGE
# ---------------------------------------------------------
elif page == "About Project":
    st.header("ℹ️ About This SIH Prototype")
    st.markdown("""
    <div class="info-card">
    <h4>Problem Statement</h4>
    <p>Student Innovation — Ideas that showcase the rich cultural heritage and traditions of India.</p>

    <h4>Tech Stack Updates</h4>
    <ul>
        <li>App Framework: <b>Streamlit (Python)</b></li>
        <li>Data Handling: <b>Pandas DataFrames</b></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("""
<div class="footer">
    🇮🇳 Made with ❤️ for Smart India Hackathon | Sanskriti Verse: Digital Heritage Explorer Prototype
</div>
""", unsafe_allow_html=True)         