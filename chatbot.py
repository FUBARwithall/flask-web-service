from flask import Blueprint, request, jsonify
import os
import logging
import numpy as np
import re
import pickle
from threading import Lock
from sentence_transformers import SentenceTransformer
from huggingface_hub import hf_hub_download, InferenceClient

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

# ============================================
# GLOBAL VARIABLES + THREAD SAFETY
# ============================================
embedder = None
kb = None
llm = None
models_lock = Lock()

# Konfigurasi Logging
logging.basicConfig(level=logging.INFO)

# --- KEYWORDS CONFIGURATION ---

GREETING_KEYWORDS = [
    "halo", "hi", "helo", "pagi", "siang", "sore", "malam", 
    "assalamualaikum", "permisi", "tanya dong", "p", "test", "halo bot", "glowie"
]

THANKS_KEYWORDS = [
    "terima kasih", "makasih", "thanks", "tengkyu", "nuhun", "suwun"
]

SKIN_KEYWORDS = [
    "jerawat", "komedo", "bruntusan", "eksim", "gatal", 
    "ruam", "iritasi", "alergi kulit", "panu", "kulit kering", "dermatitis",
    "biang keringat", "psoriasis", "vitiligo", "kurap", "kudis", "flek hitam",
    "bekas jerawat", "stretch mark", "ketombe", "rambut rontok", "rosacea",
    "melasma", "herpes", "kutil", "scabies", "urtikaria", "biduran",
    "wajah berminyak", "kulit berminyak", "kulit sensitif", "kulit kusam"
]

BLACKLIST_KEYWORDS = [
    "jok motor", "jok mobil", "sepatu", "tas", "sofa", "kursi", 
    "dompet", "jaket", "sarung tangan", "kulit sintetis", "kulit sapi",
    "kulit kambing", "kulit ular", "kerajinan kulit", "industri kulit",
    "karburator", "mesin", "motor", "mobil", "ban"
]

SPAM_KEYWORDS = [
    "wd", "slot", "gacor", "menang", "kemenangan", "jackpot", 
    "jp", "deposit", "saldo", "hoki", "maxwin", "betting"
]

# --- VALIDATION FUNCTIONS ---

def is_greeting(text: str) -> bool:
    text_lower = text.lower().strip()
    return any(text_lower == g for g in GREETING_KEYWORDS) or \
           any(text_lower.startswith(g) and len(text_lower) < 15 for g in GREETING_KEYWORDS)

def is_thanks(text: str) -> bool:
    text_lower = text.lower().strip()
    return any(t in text_lower for t in THANKS_KEYWORDS)

def is_skin_related(text: str) -> bool:
    if not text:
        return False
    text_lower = text.lower()
    if any(bl in text_lower for bl in BLACKLIST_KEYWORDS):
        return False
    has_skin_keyword = any(k in text_lower for k in SKIN_KEYWORDS)
    if has_skin_keyword:
        return True
    if "kulit" in text_lower:
        health_context = [
            "wajah", "muka", "pipi", "dahi", "hidung", "dagu",
            "merawat", "mengobati", "penyakit", "gejala", "dokter",
            "kesehatan", "treatment", "obat", "krim", "salep", "skincare"
        ]
        return any(ctx in text_lower for ctx in health_context)
    return False

# --- MODEL UTILITIES ---

def download_kb_from_hf():
    try:
        logging.info("📥 Downloading KB from HuggingFace...")
        kb_path = hf_hub_download(
            repo_id="Ardian122/skin-embeddings-v4",
            filename="skin_kb.pkl",
            cache_dir="./hf_cache"
        )
        return kb_path
    except Exception as e:
        logging.warning(f"⚠️ HF download failed: {str(e)}")
        return "skin_kb.pkl" if os.path.exists("skin_kb.pkl") else None

def load_models():
    global embedder, kb, llm
    with models_lock:
        if embedder and kb and llm:
            return True
        try:
            HF_TOKEN = os.getenv("HF_TOKEN")
            if not HF_TOKEN:
                logging.error("❌ HF_TOKEN not found in environment")
                return False
            
            kb_path = download_kb_from_hf()
            if not kb_path: return False
            
            with open(kb_path, "rb") as f:
                kb = pickle.load(f)
            
            embeddings = np.array(kb["embeddings"])
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            kb["embeddings"] = embeddings / (norms + 1e-10)
            
            embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            llm = InferenceClient(token=HF_TOKEN)
            logging.info("✅ All models loaded successfully")
            return True
        except Exception as e:
            logging.error(f"❌ Model loading failed: {str(e)}")
            return False

def search_similar(query, top_k=3, min_score=0.35):
    if not embedder or not kb: return []
    try:
        q_emb = embedder.encode(query, normalize_embeddings=True)
        sims = np.dot(kb["embeddings"], q_emb)
        idx = np.argsort(sims)[::-1]
        
        results = []
        for i in idx:
            if len(results) >= top_k: break
            score = float(sims[i])
            if score < min_score: continue
            
            doc_text = kb["documents"][i]['text']
            if any(spam in doc_text.lower() for spam in SPAM_KEYWORDS):
                continue
            results.append(doc_text)
        return results
    except Exception as e:
        logging.error(f"Search error: {str(e)}")
        return []

def clean_llm_output(text: str) -> str:
    replacements = {
        "suntik air": "bilas dengan air",
        "majalah": "makeup",
        "secubagian": "setiap",
        "kadar kemasan": "kadar minyak",
    }
    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)
    for spam in SPAM_KEYWORDS:
        text = re.sub(f"(?i){spam}", "", text)
    return re.sub(r'\s+', ' ', text).strip()

def generate_response_with_llm(context: str, question: str) -> str:
    try:
        # System prompt diperketat agar tidak repetitif
        system_prompt = (
            "Anda adalah Glowie, asisten ahli kesehatan kulit. "
            "TUGAS: Berikan jawaban medis yang akurat, ramah, dan ringkas berdasarkan konteks.\n"
            "ATURAN PENTING:\n"
            "1. JANGAN memperkenalkan diri lagi (seperti 'Halo, saya Glowie' atau 'Glowie di sini').\n"
            "2. LANGSUNG jawab intisari pertanyaan user.\n"
            "3. Gunakan gaya bahasa santai/friendly (gunakan kata 'ya', 'kamu', atau 'yuk').\n"
            "4. Maksimal 3-4 kalimat saja.\n"
            "5. Berikan 1 tips praktis di akhir jawaban.\n"
            "6. Jika perlu, sarankan konsultasi ke dokter kulit 🏥."
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Konteks Medis:\n{context}\n\nPertanyaan: {question}"}
        ]
        
        response = llm.chat_completion(
            messages=messages,
            model="meta-llama/Llama-3.1-8B-Instruct",
            max_tokens=300,
            temperature=0.4
        )
        
        reply = response.choices[0].message.content.strip()
        
        # Filter tambahan jika AI masih membandel (opsional)
        intro_patterns = [
            r"^(Halo|Hai)[!,\s]+(Saya|Aku|Glowie di sini).+?\.", 
            r"^Glowie adalah.+?\."
        ]
        for pattern in intro_patterns:
            reply = re.sub(pattern, "", reply, flags=re.IGNORECASE).strip()
            
        return clean_llm_output(reply)
    except Exception:
        return "Untuk kondisi itu, pastikan kulit tetap bersih dan jangan dipencet ya. Kalau belum membaik, yuk konsultasi ke dokter kulit! 🏥"

# --- MAIN ROUTE ---

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()
        
        if not message or len(message) > 500:
            return jsonify({"success": False, "reply": "❗ Pesan terlalu panjang atau kosong."}), 400
        
        # 1. Cek Sapaan
        if is_greeting(message):
            return jsonify({
                "success": True, 
                "reply": "Halo! 😊 Aku Glowie, asisten AI kesehatan kulitmu. Ada yang bisa Glowie bantu seputar masalah kulit atau perawatan wajahmu?"
            })
            
        # 2. Cek Ucapan Terima Kasih
        if is_thanks(message):
            return jsonify({
                "success": True, 
                "reply": "Sama-sama! Senang bisa membantu. Jaga kesehatan kulitmu selalu ya, Glowers! ✨"
            })

        # 3. Cek Relevansi Topik Kulit
        if not is_skin_related(message):
            return jsonify({
                "success": True, 
                "reply": "Maaf, saat ini Glowie hanya bisa menjawab pertanyaan seputar kesehatan kulit dan perawatan wajah. Ada keluhan kulit yang ingin kamu tanyakan ke Glowie? 😊"
            })
        
        # 4. Load Models & Search
        if not load_models():
            return jsonify({"success": False, "reply": "⚠️ Glowie sedang maintenance sebentar, tunggu ya."}), 503
        
        docs = search_similar(message)
        if not docs:
            return jsonify({
                "success": True, 
                "reply": "Glowie belum menemukan info spesifik mengenai hal itu di database. Untuk keamanan, sebaiknya konsultasikan langsung ke dokter kulit ya 🏥"
            })
        
        # 5. Generate Response
        context_text = "\n".join([f"- {d}" for d in docs])
        reply = generate_response_with_llm(context_text, message)
        
        return jsonify({"success": True, "reply": reply})

    except Exception as e:
        logging.error(f"Server Error: {str(e)}")
        return jsonify({"success": False, "reply": "⚠️ Terjadi kesalahan pada server Glowie."}), 500