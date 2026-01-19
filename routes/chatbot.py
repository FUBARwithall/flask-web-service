from flask import Blueprint, request, jsonify
import os
import logging
import numpy as np
import re
import pickle
from threading import Lock
from models import get_db_connection
from sentence_transformers import SentenceTransformer
from flask_jwt_extended import jwt_required, get_jwt_identity
from huggingface_hub import hf_hub_download, InferenceClient

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

# ============================================
# GLOBAL VARIABLES + THREAD SAFETY
# ============================================
embedder = None
kb = None
llm = None
models_lock = Lock()

# Konfigurasi Logging - Pastikan level INFO tampil di terminal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- KEYWORDS CONFIGURATION ---

GREETING_KEYWORDS = [
    "halo", "hi", "helo", "pagi", "siang", "sore", "malam", 
    "assalamualaikum", "permisi", "tanya dong", "p", "test", "halo bot", "glowie"
]

THANKS_KEYWORDS = [
    "terima kasih", "makasih", "thanks", "tengkyu", "nuhun", "suwun"
]

SKIN_KEYWORDS = [
    "jerawat", "jerawat berminyak", "komedo", "bruntusan", "eksim", "gatal", 
    "ruam", "iritasi", "alergi kulit", "panu", "kulit kering", "dermatitis",
    "biang keringat", "psoriasis", "vitiligo", "kurap", "kudis", "flek hitam",
    "bekas jerawat", "stretch mark", "ketombe", "rambut rontok", "rosacea",
    "melasma", "herpes", "kutil", "scabies", "urtikaria", "biduran",
    "wajah berminyak", "kulit berminyak", "kulit sensitif", "kulit kusam",  
    "pori tersumbat", "sebum berlebih"
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
    # Exact match for greetings
    if any(text_lower == g for g in GREETING_KEYWORDS):
        return True
    # Start with greeting + word boundary (e.g., "halo bot") and length limit
    return any(re.search(rf"^{re.escape(g)}\b", text_lower) and len(text_lower) < 15 for g in GREETING_KEYWORDS)

def is_thanks(text: str) -> bool:
    text_lower = text.lower().strip()
    return any(t in text_lower for t in THANKS_KEYWORDS)

def is_skin_related(text: str) -> bool:
    if not text:
        return False
    text_lower = text.lower()
    
    # Gunakan word boundaries untuk blacklist agar tidak salah deteksi (misal: "atasi" mengandung "tas")
    for bl in BLACKLIST_KEYWORDS:
        if re.search(rf"\b{re.escape(bl)}\b", text_lower):
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
        logger.info("📥 Downloading KB from HuggingFace...")
        kb_path = hf_hub_download(
            repo_id="Ardian122/skin-embeddings-v5",
            filename="skin_kb.pkl",
            cache_dir="./hf_cache"
        )
        return kb_path
    except Exception as e:
        logger.warning(f"⚠️ HF download failed: {str(e)}")
        return "skin_kb.pkl" if os.path.exists("skin_kb.pkl") else None

def load_models():
    global embedder, kb, llm
    with models_lock:
        if embedder and kb and llm:
            return True
        try:
            HF_TOKEN = os.getenv("HF_TOKEN")
            if not HF_TOKEN:
                logger.error("❌ HF_TOKEN not found in environment")
                return False
            
            kb_path = download_kb_from_hf()
            if not kb_path: return False
            
            # Fix for Windows: detect and resolve HF pointer files
            if os.path.exists(kb_path) and os.path.getsize(kb_path) < 500:
                try:
                    with open(kb_path, "r") as f:
                        pointer_content = f.read().strip()
                        if pointer_content.startswith("../../blobs/"):
                            # Resolve the relative path to the actual blob file
                            actual_kb_path = os.path.abspath(os.path.join(os.path.dirname(kb_path), pointer_content))
                            if os.path.exists(actual_kb_path):
                                logger.info(f"🔗 Resolved HF pointer: {actual_kb_path}")
                                kb_path = actual_kb_path
                except Exception as e:
                    logger.warning(f"⚠️ Failed to resolve pointer file: {str(e)}")

            with open(kb_path, "rb") as f:
                kb = pickle.load(f)
            
            embeddings = np.array(kb["embeddings"])
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            kb["embeddings"] = embeddings / (norms + 1e-10)
            
            embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            llm = InferenceClient(token=HF_TOKEN)
            logger.info("✅ All models loaded successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Model loading failed: {str(e)}")
            return False

# Panggil load_models() saat module di-import agar inisialisasi terlihat di log terminal
# Note: Ini akan berjalan saat Flask (app.py) melakukan import blueprint
load_models()
        

# Tambah endpoint untuk debugging MRR
@chatbot_bp.route("/debug", methods=["POST"])
def debug_chat():
    """Debug endpoint - Lihat retrieved documents"""
    try:
        data = request.get_json()
        message = data.get("message", "").strip()
        
        if not load_models():
            return jsonify({"error": "Models not loaded"}), 503
        
        docs = search_similar(message)
        context = "\n".join([f"- {d[:100]}..." for d in docs])
        
        return jsonify({
            "query": message,
            "retrieved_docs": len(docs),
            "docs_preview": docs,
            "context": context
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def search_similar(query, top_k=5, min_score=0.45):
    if not embedder or not kb: 
        logging.info(f"❌ MRR: Models/KB not loaded for query: '{query}'")
        return []
    
    try:
        logger.info(f"🔍 MRR Query: '{query}' - Starting embedding search...")
        q_emb = embedder.encode(query, normalize_embeddings=True)
        sims = np.dot(kb["embeddings"], q_emb)
        idx = np.argsort(sims)[::-1]
        
        # Ambil kandidat untuk reranking
        candidates = []
        for i in idx:
            if len(candidates) >= top_k * 2:  # 10 kandidat
                break
            score = float(sims[i])
            if score < min_score:
                continue
            
            doc_text = kb["documents"][i]['text']
            if any(spam in doc_text.lower() for spam in SPAM_KEYWORDS):
                continue
            candidates.append(doc_text)
        
        logger.info(f"📊 MRR: {len(kb['documents'])} total docs → {len(candidates)} candidates (min_score={min_score})")
        
        # MRR Simple Reranking (ringan)
        reranked_docs = simple_mrr(query, candidates, top_k)
        
        logger.info(f"✅ MRR: {len(candidates)} candidates → {len(reranked_docs)} final docs")
        logger.info(f"📄 Top docs: {reranked_docs[0][:100]}..." if reranked_docs else "❌ No docs after MRR")
        
        return reranked_docs
        
    except Exception as e:
        logger.error(f"💥 MRR Error: {str(e)}")
        return []

def simple_mrr(query, docs, top_k=3):
    """MRR sederhana - Keyword + length relevance"""
    if not docs:
        return []
    
    query_words = set(query.lower().split())
    scores = []
    
    for i, doc in enumerate(docs):
        # Keyword overlap
        doc_words = set(doc.lower().split())
        keyword_score = len(query_words.intersection(doc_words)) / max(len(query_words), 1)
        
        # Length penalty
        doc_len = len(doc.split())
        length_score = max(0, 1.0 - abs(doc_len - 80) / 80)  # Ideal ~80 kata
        
        # MRR score
        mrr_score = (keyword_score * 0.7) + (length_score * 0.3)
        scores.append((doc, mrr_score))
    
    ranked = sorted(scores, key=lambda x: x[1], reverse=True)
    logger.info(f"📈 MRR Scores: {[f'{s:.3f}' for _, s in ranked[:3]]}")
    
    return [doc for doc, _ in ranked[:top_k]]


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
@jwt_required()
def chat():
    conn = None
    cursor = None

    try:
        data = request.get_json()
        message = data.get("message", "").strip()
        conversation_id = data.get("conversation_id")

        if not conversation_id:
            return jsonify({"success": False, "reply": "Conversation ID tidak valid"}), 400

        if not message or len(message) > 500:
            return jsonify({"success": False, "reply": "❗ Pesan terlalu panjang atau kosong."}), 400

        # ================= DB CONNECT =================
        conn = get_db_connection()
        if not conn:
            return jsonify({"success": False, "reply": "DB error"}), 500
        cursor = conn.cursor(dictionary=True)

        # ================= 1. GREETING =================
        if is_greeting(message):
            reply = (
                "Halo! 😊 Aku Glowie, asisten AI kesehatan kulitmu. "
                "Ada yang bisa Glowie bantu seputar masalah kulit atau perawatan wajahmu?"
            )

        # ================= 2. THANKS =================
        elif is_thanks(message):
            reply = "Sama-sama! Senang bisa membantu. Jaga kesehatan kulitmu selalu ya, Glowers! ✨"

        # ================= 3. NON SKIN =================
        elif not is_skin_related(message):
            reply = (
                "Maaf, saat ini Glowie hanya bisa menjawab pertanyaan seputar "
                "kesehatan kulit dan perawatan wajah. Ada keluhan kulit yang ingin kamu tanyakan? 😊"
            )

        else:
            # ================= 4. LOAD MODEL =================
            if not load_models():
                return jsonify({"success": False, "reply": "⚠️ Glowie sedang maintenance sebentar."}), 503

            docs = search_similar(message)
            if not docs:
                reply = (
                    "Glowie belum menemukan info spesifik mengenai hal itu di database. "
                    "Untuk keamanan, sebaiknya konsultasikan langsung ke dokter kulit ya 🏥"
                )
            else:
                context_text = "\n".join([f"- {d}" for d in docs])
                reply = generate_response_with_llm(context_text, message)

        # ================= INSERT USER MESSAGE =================
        cursor.execute(
            """
            INSERT INTO messages (conversation_id, role, content)
            VALUES (%s, %s, %s)
            """,
            (conversation_id, "user", message)
        )

        # ================= INSERT BOT MESSAGE =================
        cursor.execute(
            """
            INSERT INTO messages (conversation_id, role, content)
            VALUES (%s, %s, %s)
            """,
            (conversation_id, "assistant", reply)
        )

        conn.commit()

        return jsonify({"success": True, "reply": reply}), 200

    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"❌ Chat error: {str(e)}")
        return jsonify({"success": False, "reply": "⚠️ Terjadi kesalahan pada server Glowie."}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@chatbot_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    user_id = get_jwt_identity()

    conn = get_db_connection()
    if not conn:
        return jsonify(status='error', message='DB error'), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, title, created_at FROM conversations WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,)
    )
    conversations = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(conversations), 200

@chatbot_bp.route('/conversations', methods=['POST'])
@jwt_required()
def create_conversation():
    user_id = get_jwt_identity()

    conn = get_db_connection()
    if not conn:
        return jsonify(status='error', message='DB error'), 500

    cursor = conn.cursor(dictionary=True)
    
    from datetime import datetime
    title = f"Chat {datetime.now().strftime('%d %b %Y %H:%M')}"
    
    cursor.execute(
        "INSERT INTO conversations (user_id, title) VALUES (%s, %s)",
        (user_id, title)
    )
    conn.commit()

    conversation_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({'conversation_id': conversation_id, 'title': title}), 201


@chatbot_bp.route('/messages/<int:conversation_id>', methods=['GET'])
@jwt_required()
def get_messages(conversation_id):
    user_id = get_jwt_identity()

    conn = get_db_connection()
    if not conn:
        return jsonify(status='error', message='DB error'), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT role, content, created_at
        FROM messages
        WHERE conversation_id = %s
        ORDER BY created_at ASC
    """, (conversation_id,))
    
    messages = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(messages), 200