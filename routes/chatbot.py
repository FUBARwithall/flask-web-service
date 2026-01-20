from flask import Blueprint, request, jsonify
import os
import logging
import numpy as np
import re
import pickle
from threading import Lock
import json
from models import get_db_connection
from sentence_transformers import SentenceTransformer, CrossEncoder
from flask_jwt_extended import jwt_required, get_jwt_identity
from huggingface_hub import hf_hub_download, InferenceClient
import rank_bm25

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

# ============================================
# GLOBAL VARIABLES + THREAD SAFETY
# ============================================
embedder = None
cross_encoder = None
kb = None
llm = None
bm25 = None
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
    "jerawat", "jerawat berminyak", "komedo", "bruntusan", "eksim", "gatal", 
    "ruam", "iritasi", "alergi kulit", "panu", "kulit kering", "dermatitis",
    "biang keringat", "psoriasis", "vitiligo", "kurap", "kudis", "flek hitam",
    "bekas jerawat", "stretch mark", "ketombe", "rambut rontok", "rosacea",
    "melasma", "herpes", "kutil", "scabies", "urtikaria", "biduran",
    "wajah berminyak", "kulit berminyak", "kulit sensitif", "kulit kusam",  
    "pori tersumbat", "sebum berlebih", "milia"
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

def is_product_recommendation_query(text: str) -> bool:
    """Deteksi apakah user menanyakan rekomendasi produk"""
    text_lower = text.lower()
    product_keywords = [
        "produk", "obat", "krim", "salep", "serum", "toner", 
        "moisturizer", "cleanser", "sabun", "skincare", "perawatan",
        "rekomendasi", "pakai apa", "pake apa", "apa yang bagus"
    ]
    return any(kw in text_lower for kw in product_keywords)

def download_kb_from_hf():
    """Download KB v7 langsung (format pkl)"""
    try:
        logging.info("📥 Downloading KB v7 from HuggingFace...")
        kb_path = hf_hub_download(
            repo_id="Ardian122/skin-embeddings-v7",
            filename="skin_kb.pkl",
            cache_dir="./hf_cache"
        )
        return {"path": kb_path, "format": "pkl"}
    except Exception as e:
        logging.error(f"❌ HF download failed: {str(e)}")

        if os.path.exists("skin_kb.pkl"):
            return {"path": "skin_kb.pkl", "format": "pkl"}
        return None

def load_kb_safe(kb_info):
    """Load KB dengan format detection otomatis"""
    if not kb_info:
        return None
    
    try:
        if kb_info.get("format") == "npz":
            logging.info("📂 Loading KB from NPZ format...")
            
            data = np.load(kb_info["embeddings"])
            embeddings = data["embeddings"]
            
            with open(kb_info["documents"], "r", encoding="utf-8") as f:
                documents = json.load(f)
            
            kb = {
                "embeddings": embeddings,
                "documents": documents
            }
            logging.info(f"✅ Loaded {len(documents)} documents from NPZ")
            return kb
        
        elif kb_info.get("format") == "pkl":
            logging.info("📂 Loading KB from PKL format...")
            with open(kb_info["path"], "rb") as f:
                kb = pickle.load(f)
                
                if 'metadata' in kb:
                    m = kb['metadata']
                    # Ambil jumlah penyakit dari list 'diseases'
                    num_diseases = len(m.get('diseases', []))
                    logging.info(f"📊 KB Statistics: {len(kb['documents'])} docs, {num_diseases} categories")
                
                return kb
    
    except Exception as e:
        logging.error(f"❌ KB loading failed: {str(e)}")
        return None

def load_models():
    global embedder, cross_encoder, kb, llm, bm25
    
    with models_lock:
        if embedder and cross_encoder and kb and llm and bm25:
            return True
        
        try:
            HF_TOKEN = os.getenv("HF_TOKEN")
            if not HF_TOKEN:
                logging.error("❌ HF_TOKEN not found in environment")
                return False
            
            kb_info = download_kb_from_hf()
            if not kb_info:
                logging.error("❌ KB download failed")
                return False
            
            kb = load_kb_safe(kb_info)
            if not kb:
                logging.error("❌ KB loading failed")
                return False
            
            embeddings = np.array(kb["embeddings"])
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            kb["embeddings"] = embeddings / (norms + 1e-10)
            
            from sentence_transformers import SentenceTransformer, CrossEncoder
            
            embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
            
            import rank_bm25
            corpus = [doc['text'] for doc in kb["documents"]]
            tokenized_corpus = [doc.lower().split() for doc in corpus]
            bm25 = rank_bm25.BM25Okapi(tokenized_corpus)
            
            from huggingface_hub import InferenceClient
            llm = InferenceClient(token=HF_TOKEN)
            
            logging.info("✅ All models loaded successfully")
            return True
            
        except Exception as e:
            logging.error(f"❌ Model loading failed: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())
            return False


def extract_main_keywords(query: str) -> set:
    """
    🆕 Extract topik agar sesuai dengan kategori v7
    """
    keyword_mapping = {
        "jerawat": ["jerawat", "acne", "komedo", "bruntusan", "pustula", "papula"],
        "eksim": ["eksim", "eczema", "dermatitis"],
        "psoriasis": ["psoriasis", "plak", "bersisik"],
        "vitiligo": ["vitiligo", "belang", "bercak putih"],
        "kurap_dan_jamur": ["kurap", "panu", "kadas", "jamur kulit", "ringworm", "tinea"],
        "herpes": ["herpes", "zoster", "cacar ular", "dompo"],
        "biang_keringat": ["biang keringat", "miliaria", "keringat buntet"],
        "milia_dan_bisul": ["milia", "bisul", "furunkel", "bintik putih keras", "bernanah"],
        "scabies_dan_kutu": ["scabies", "skabies", "kudis", "gudik", "tungau", "kutu"],
        "kulit_berminyak": ["berminyak", "oily", "sebum"],
        "kulit_kering": ["kering", "dry", "xerosis", "mengelupas"],
        "kulit_sensitif": ["sensitif", "perih", "mudah iritasi", "reaktif"]
    }
    
    query_lower = query.lower()
    detected_topics = set()
    for topic, keywords in keyword_mapping.items():
        if any(kw in query_lower for kw in keywords):
            detected_topics.add(topic)
    return detected_topics

def calculate_topic_relevance(doc_text: str, query_topics: set) -> float:
    """
    🆕 Hitung skor relevansi terhadap 12 kategori medis v7
    """
    if not query_topics:
        return 1.0 
    
    doc_lower = doc_text.lower()
    
    topic_must_have = {
        "jerawat": ["jerawat", "acne", "komedo"],
        "eksim": ["eksim", "eczema", "dermatitis"],
        "psoriasis": ["psoriasis"],
        "vitiligo": ["vitiligo", "belang"],
        "kurap_dan_jamur": ["kurap", "panu", "jamur", "tinea"],
        "herpes": ["herpes", "zoster"],
        "biang_keringat": ["biang keringat", "miliaria"],
        "milia_dan_bisul": ["milia", "bisul"],
        "scabies_dan_kutu": ["scabies", "kudis", "tungau"],
        "kulit_berminyak": ["berminyak", "oily", "sebum"],
        "kulit_kering": ["kering", "dry", "xerosis"],
        "kulit_sensitif": ["sensitif", "iritasi"]
    }
    
    disqualify_keywords = {
        "scabies_dan_kutu": ["jerawat", "bisul"],
        "kurap_dan_jamur": ["jerawat", "eksim"],
        "jerawat": ["bisul", "milia"]
    }
    
    matched_score = 0
    for topic in query_topics:
        if topic in topic_must_have:
            if any(kw in doc_lower for kw in topic_must_have[topic]):
                matched_score += 1
            if topic in disqualify_keywords:
                if any(kw in doc_lower for kw in disqualify_keywords[topic]):
                    matched_score -= 0.4
    
    return max(0.0, matched_score / len(query_topics))


def rerank_documents(query, docs, top_k=3):
    """
    ✅ IMPROVED CROSS-ENCODER RERANKER dengan Topic Filtering
    """
    global cross_encoder
    if not cross_encoder or not docs:
        return docs[:top_k] if docs else []
    
    try:
        # 1. Extract topik dari query
        query_topics = extract_main_keywords(query)
        logging.info(f"🎯 Detected topics: {query_topics}")
        
        # 2. Cross-Encoder scoring
        pairs = [[query, doc] for doc in docs]
        ce_scores = cross_encoder.predict(pairs)
        
        # 3. Calculate topic relevance untuk setiap dokumen
        topic_scores = [calculate_topic_relevance(doc, query_topics) for doc in docs]
        
        # 4. HYBRID SCORING: Cross-Encoder (70%) + Topic Relevance (30%)
        final_scores = [
            0.7 * ce_score + 0.3 * topic_score 
            for ce_score, topic_score in zip(ce_scores, topic_scores)
        ]
        
        # 5. Filter dokumen dengan topic_relevance < 0.3 (threshold)
        MIN_TOPIC_RELEVANCE = 0.3
        filtered_results = [
            (score, doc, topic_score) 
            for score, doc, topic_score in zip(final_scores, docs, topic_scores)
            if topic_score >= MIN_TOPIC_RELEVANCE
        ]
        
        if not filtered_results:
            logging.warning("⚠️ All docs filtered out by topic relevance, using fallback")
            filtered_results = [(s, d, t) for s, d, t in zip(final_scores, docs, topic_scores)]
        
        # 6. Sort by final score
        ranked = sorted(filtered_results, key=lambda x: x[0], reverse=True)
        
        # 7. Logging untuk debugging
        logging.info(f"📈 Rerank Results:")
        for i, (score, doc, topic_score) in enumerate(ranked[:3], 1):
            # Cari judul dari awal dokumen
            doc_preview = doc[:200].replace('\n', ' ').strip()

            first_sentence = doc_preview.split('. ')[0] if '. ' in doc_preview else doc_preview[:100]
            logging.info(f"  #{i} | Final: {score:.3f} | Topic: {topic_score:.2f} | {first_sentence}...")
        
        return [doc for _, doc, _ in ranked[:top_k]]
        
    except Exception as e:
        logging.error(f"❌ Rerank error: {str(e)}")
        return docs[:top_k] if docs else []


def search_similar(query, top_k=5, min_score=0.35):
    """✅ MRR Search v7: Hybrid + Semantic + BM25 + Reranker"""
    global embedder, kb, bm25
    if not embedder or not kb or not bm25:
        return []
    
    try:
        # 1. Semantic Search
        q_emb = embedder.encode(query, normalize_embeddings=True)
        semantic_sims = np.dot(kb["embeddings"], q_emb)
        semantic_idx = np.argsort(semantic_sims)[::-1]
        
        # 2. BM25
        tokenized_query = query.lower().split()
        bm25_scores = bm25.get_scores(tokenized_query)
        bm25_idx = np.argsort(bm25_scores)[::-1]
        
        # 3. Hybrid RRF
        candidates = {}
        for rank, i in enumerate(semantic_idx[:20], 1): # Ambil top 20
            if semantic_sims[i] >= min_score:
                candidates[i] = 1/(60 + rank)
        for rank, i in enumerate(bm25_idx[:20], 1):
            candidates[i] = candidates.get(i, 0) + 1/(60 + rank)
            
        sorted_candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
        candidate_docs = [kb["documents"][i]['text'] for i, _ in sorted_candidates[:15]]
        
        # 4. Reranking & Filtering
        return rerank_documents(query, candidate_docs, top_k)
    except Exception as e:
        logging.error(f"Search error: {e}")
        return []


# --- DEBUG ENDPOINT ---
@chatbot_bp.route("/debug", methods=["POST"])
def debug_chat():
    """Debug endpoint - Lihat retrieved documents + scores"""
    try:
        data = request.get_json()
        message = data.get("message", "").strip()
        
        if not load_models():
            return jsonify({"error": "Models not loaded"}), 503
        
        docs = search_similar(message, top_k=5)
        context = "\n".join([f"- {d[:100]}..." for d in docs])
        
        return jsonify({
            "query": message,
            "retrieved_docs": len(docs),
            "docs_preview": [d[:150] + "..." for d in docs],
            "context": context,
            "success": True
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
    global llm
    try:
        # Deteksi apakah ini query produk
        is_product_query = is_product_recommendation_query(question)
        
        if is_product_query:
            system_prompt = (
                "Anda adalah Glowie, asisten ahli kesehatan kulit. "
                "TUGAS: Berikan rekomendasi perawatan yang akurat berdasarkan konteks medis.\n"
                "ATURAN PENTING:\n"
                "1. JANGAN sebutkan nama brand/produk spesifik (seperti Wardah, Emina, dll).\n"
                "2. Jelaskan BAHAN AKTIF atau JENIS PRODUK yang sesuai (contoh: 'salicylic acid 2%', 'benzoyl peroxide', 'niacinamide').\n"
                "3. Berikan 2-3 jenis perawatan yang efektif.\n"
                "4. Maksimal 4 kalimat.\n"
                "5. Akhiri dengan saran konsultasi ke dokter/apoteker untuk rekomendasi produk spesifik.\n"
                "6. Gunakan bahasa santai dan ramah."
            )
        else:
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

        conn = get_db_connection()
        if not conn:
            return jsonify({"success": False, "reply": "DB error"}), 500
        cursor = conn.cursor(dictionary=True)

        if is_greeting(message):
            reply = (
                "Halo! 😊 Aku Glowie, asisten AI kesehatan kulitmu. "
                "Ada yang bisa Glowie bantu seputar masalah kulit atau perawatan wajahmu?"
            )
        elif is_thanks(message):
            reply = "Sama-sama! Senang bisa membantu. Jaga kesehatan kulitmu selalu ya, Glowers! ✨"
        elif not is_skin_related(message):
            reply = (
                "Maaf, saat ini Glowie hanya bisa menjawab pertanyaan seputar "
                "kesehatan kulit dan perawatan wajah. Ada keluhan kulit yang ingin kamu tanyakan? 😊"
            )
        else:
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

        cursor.execute(
            "INSERT INTO messages (conversation_id, role, content) VALUES (%s, %s, %s)",
            (conversation_id, "user", message)
        )
        cursor.execute(
            "INSERT INTO messages (conversation_id, role, content) VALUES (%s, %s, %s)",
            (conversation_id, "assistant", reply)
        )
        conn.commit()

        return jsonify({"success": True, "reply": reply}), 200

    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"❌ Chat error: {str(e)}")
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