from datetime import datetime
import json

class WebhookProcessor:
    @staticmethod
    def process_push_event(payload):
        """Process push webhook event"""
        try:
            author = payload.get('pusher', {}).get('name', 'Unknown')
            ref = payload.get('ref', '')
            to_branch = ref.split('/')[-1] if ref else 'Unknown'
            timestamp = datetime.utcnow()
            
            return {
                'id': payload.get('after', ''),
                'author': author,
                'action': 'push',
                'to_branch': to_branch,
                'from_branch': None,
                'timestamp': timestamp,
                'message': f'"{author}" pushed to "{to_branch}" on {timestamp.strftime("%d %B %Y - %I:%M %p UTC")}'
            }
        except Exception as e:
            print(f"Error processing push event: {e}")
            return None
    
    @staticmethod
    def process_pull_request_event(payload):
        """Process pull request webhook event"""
        try:
            pr_data = payload.get('pull_request', {})
            author = pr_data.get('user', {}).get('login', 'Unknown')
            from_branch = pr_data.get('head', {}).get('ref', 'Unknown')
            to_branch = pr_data.get('base', {}).get('ref', 'Unknown')
            timestamp = datetime.utcnow()
            action = payload.get('action', '')
            
            # Only process 'opened' and 'closed' actions
            if action == 'opened':
                message = f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp.strftime("%d %B %Y - %I:%M %p UTC")}'
                return {
                    'id': str(pr_data.get('id', '')),
                    'author': author,
                    'action': 'pull_request',
                    'to_branch': to_branch,
                    'from_branch': from_branch,
                    'timestamp': timestamp,
                    'message': message
                }
            elif action == 'closed' and pr_data.get('merged', False):
                # This is a merge action
                message = f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp.strftime("%d %B %Y - %I:%M %p UTC")}'
                return {
                    'id': str(pr_data.get('id', '')),
                    'author': author,
                    'action': 'merge',
                    'to_branch': to_branch,
                    'from_branch': from_branch,
                    'timestamp': timestamp,
                    'message': message
                }
            
            return None
        except Exception as e:
            print(f"Error processing pull request event: {e}")
            return None