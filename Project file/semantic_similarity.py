from sentence_transformers import SentenceTransformer, util
import streamlit as st

# Cache the similarity model so it doesn't slow down the app
@st.cache_resource
def load_similarity_model():
    print("Loading SentenceTransformer into memory...")
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_similarity_model()

def similarity(text1, text2):
    emb1 = model.encode(text1, convert_to_tensor=True)
    emb2 = model.encode(text2, convert_to_tensor=True)
    score = util.cos_sim(emb1, emb2)
    return float(score)