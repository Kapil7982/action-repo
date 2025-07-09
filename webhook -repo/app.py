from flask import Flask, request, jsonify, render_template
from config import Config
from models import WebhookModel
from webhook_processor import WebhookProcessor
import json

app = Flask(__name__)
app.config.from_object(Config)

# Initialize MongoDB model
webhook_model = WebhookModel(app.config['MONGODB_URI'], app.config['DB_NAME'])
processor = WebhookProcessor()

@app.route('/')
def index():
    """Render the main UI page"""
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle GitHub webhook events"""
    try:
        # Get the event type from headers
        event_type = request.headers.get('X-GitHub-Event')
        payload = request.get_json()
        
        if not payload:
            return jsonify({'error': 'No payload received'}), 400
        
        processed_data = None
        
        if event_type == 'push':
            processed_data = processor.process_push_event(payload)
        elif event_type == 'pull_request':
            processed_data = processor.process_pull_request_event(payload)
        
        if processed_data:
            # Store in MongoDB
            webhook_model.insert_webhook(processed_data)
            return jsonify({'message': 'Webhook processed successfully'}), 200
        else:
            return jsonify({'message': 'Event not processed'}), 200
            
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/events')
def get_events():
    """API endpoint to get latest webhook events"""
    try:
        events = webhook_model.get_latest_webhooks(50)
        # Convert ObjectId to string for JSON serialization
        for event in events:
            event['_id'] = str(event['_id'])
            # Convert datetime to string
            if 'timestamp' in event:
                event['timestamp'] = event['timestamp'].isoformat()
        
        return jsonify(events)
    except Exception as e:
        print(f"Error fetching events: {e}")
        return jsonify({'error': 'Failed to fetch events'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)