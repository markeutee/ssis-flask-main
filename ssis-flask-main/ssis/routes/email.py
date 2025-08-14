from flask import Blueprint, request, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

email_bp = Blueprint('email', __name__)
@email_bp.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()

        to_email = data.get('to')
        subject = data.get('subject')
        content = data.get('content')

        # ✅ Log the values to check what you're actually sending
        print(f"📨 Email TO: {to_email}")
        print(f"📨 Subject: {subject}")
        print(f"📨 Content: {content}")

        # ✅ Check for missing fields
        if not to_email or not subject or not content:
            return jsonify({'error': 'Missing required email fields'}), 400

        # ✅ Construct message with correct field
        message = Mail(
            from_email='johnmarkmontilla15@gmail.com',
            to_emails=to_email,
            subject=subject,
            html_content=content  # or plain_text_content=content if it's not HTML
        )

        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)

        return jsonify({'message': 'Email sent!', 'status_code': response.status_code}), 200

    except Exception as e:
        import traceback
        print("📛 ERROR SENDING EMAIL:")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
