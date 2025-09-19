
from flask import Flask, render_template, request, jsonify, flash
import json
import logging
from news_verifier import NewsVerifier
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the news verifier
news_verifier = NewsVerifier()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Render the main page with headline input form"""
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify_headline():
    """Verify the submitted news headline"""
    try:
        data = request.get_json() if request.is_json else request.form
        headline = data.get('headline', '').strip()
        
        if not headline:
            return jsonify({
                'error': 'Please provide a news headline to verify',
                'status': 'error'
            }), 400
        
        # Perform verification
        logger.info(f"Verifying headline: {headline}")
        result = news_verifier.verify_headline(headline)
        
        return jsonify({
            'status': 'success',
            'headline': headline,
            'verification_result': result
        })
        
    except Exception as e:
        logger.error(f"Error during verification: {str(e)}")
        return jsonify({
            'error': f'Verification failed: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/result')
def show_result():
    """Display verification results"""
    return render_template('result.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
