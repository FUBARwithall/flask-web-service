from flask import Blueprint, request, jsonify
from gradio_client import Client
import threading
from models import get_db_connection

classify_bp = Blueprint('classify', __name__, url_prefix='/api/classify')

try:
    hf_client = Client("JustParadis/indobert-comment")
except Exception as e:
    print(f"Warning: Failed to initialize Gradio client: {e}")
    hf_client = None

def classify_text(text):
    """Function to classify text using Gradio client"""
    if not hf_client:
        return None
    try:
        # Assuming the model returns a label directly or a dict with labels
        result = hf_client.predict(text, api_name="/predict")
        
        # If result is a list (like [{'label': 'positive', 'score': 0.99}]), get the top one
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], dict):
                if 'label' in result[0]:
                    return result[0]['label']
                # If it's a list of scores, find the max
                best = max(result, key=lambda x: x.get('score', 0))
                return best.get('label', str(best))
            return str(result[0])
        
        # If result is a dict (like {'negative': 0.99, 'positive': 0.01})
        if isinstance(result, dict):
            if 'label' in result:
                return result['label']
            # Find the key with the highest value (score)
            try:
                best_label = max(result.items(), key=lambda x: x[1])[0]
                return str(best_label)
            except:
                return str(result)
            
        return str(result)
    except Exception as e:
        print(f"Error classifying text: {e}")
        return None

def update_comment_sentiment(comment_id, sentiment):
    """Background task to update comment sentiment in database"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE product_comments SET sentiment = %s WHERE id = %s", (sentiment, comment_id))
        conn.commit()
    except Exception as e:
        print(f"Error updating sentiment in DB: {e}")
    finally:
        cursor.close()
        conn.close()

@classify_bp.route('/comment/<int:comment_id>', methods=['POST'])
def classify_comment_route(comment_id):
    """Route to manually trigger classification for an existing comment"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'Database connection error'}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT comment FROM product_comments WHERE id = %s", (comment_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return jsonify({'success': False, 'message': 'Comment not found'}), 404

        comment_text = row['comment']
        sentiment = classify_text(comment_text)

        if sentiment:
            update_comment_sentiment(comment_id, sentiment)
            return jsonify({'success': True, 'sentiment': sentiment})
        else:
            return jsonify({'success': False, 'message': 'Classification failed'}), 500

    except Exception as e:
        print(f"Error in classify_comment_route: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@classify_bp.route('/batch', methods=['POST'])
def batch_classify():
    """Route to classify all comments. Optionally force re-classification of existing ones."""
    try:
        data = request.get_json() or {}
        force = data.get('force', False)
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'Database connection error'}), 500
        
        cursor = conn.cursor(dictionary=True)
        if force:
            cursor.execute("SELECT id, comment FROM product_comments")
        else:
            cursor.execute("SELECT id, comment FROM product_comments WHERE sentiment IS NULL")
            
        comments = cursor.fetchall()
        cursor.close()
        conn.close()

        count = 0
        for row in comments:
            sentiment = classify_text(row['comment'])
            if sentiment:
                update_comment_sentiment(row['id'], sentiment)
                count += 1
        
        return jsonify({'success': True, 'processed': count, 'total': len(comments)})

    except Exception as e:
        print(f"Error in batch_classify: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
