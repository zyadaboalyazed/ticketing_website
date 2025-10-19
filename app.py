from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# In-memory data storage (in production, use a real database)
events = [
    {
        'id': 1,
        'name': 'Rock Concert 2025',
        'date': '2025-11-15',
        'venue': 'Madison Square Garden',
        'price': 75.00,
        'available_tickets': 500
    },
    {
        'id': 2,
        'name': 'Jazz Night',
        'date': '2025-11-20',
        'venue': 'Blue Note',
        'price': 45.00,
        'available_tickets': 150
    },
    {
        'id': 3,
        'name': 'Theater Play - Hamlet',
        'date': '2025-11-25',
        'venue': 'Broadway Theater',
        'price': 60.00,
        'available_tickets': 300
    },
    {
        'id': 4,
        'name': 'Sports Game - Finals',
        'date': '2025-12-01',
        'venue': 'Stadium Arena',
        'price': 120.00,
        'available_tickets': 1000
    }
]

bookings = []
booking_id_counter = 1

# Serve the main page
@app.route('/')
def index():
    return render_template('index.html')

# API Routes

# Get all events
@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(events), 200

# Get a specific event
@app.route('/api/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = next((e for e in events if e['id'] == event_id), None)
    if event:
        return jsonify(event), 200
    return jsonify({'error': 'Event not found'}), 404

# Create a new event (admin functionality)
@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.get_json()
    
    required_fields = ['name', 'date', 'venue', 'price', 'available_tickets']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_event = {
        'id': max([e['id'] for e in events], default=0) + 1,
        'name': data['name'],
        'date': data['date'],
        'venue': data['venue'],
        'price': float(data['price']),
        'available_tickets': int(data['available_tickets'])
    }
    
    events.append(new_event)
    return jsonify(new_event), 201

# Update an event
@app.route('/api/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event = next((e for e in events if e['id'] == event_id), None)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        event['name'] = data['name']
    if 'date' in data:
        event['date'] = data['date']
    if 'venue' in data:
        event['venue'] = data['venue']
    if 'price' in data:
        event['price'] = float(data['price'])
    if 'available_tickets' in data:
        event['available_tickets'] = int(data['available_tickets'])
    
    return jsonify(event), 200

# Delete an event
@app.route('/api/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    global events
    event = next((e for e in events if e['id'] == event_id), None)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    events = [e for e in events if e['id'] != event_id]
    return jsonify({'message': 'Event deleted successfully'}), 200

# Get all bookings
@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    return jsonify(bookings), 200

# Get a specific booking
@app.route('/api/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    booking = next((b for b in bookings if b['id'] == booking_id), None)
    if booking:
        return jsonify(booking), 200
    return jsonify({'error': 'Booking not found'}), 404

# Create a new booking
@app.route('/api/bookings', methods=['POST'])
def create_booking():
    global booking_id_counter
    data = request.get_json()
    
    required_fields = ['event_id', 'event_name', 'customer_name', 'customer_email', 'num_tickets', 'total_price']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate event exists and has enough tickets
    event = next((e for e in events if e['id'] == data['event_id']), None)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    if event['available_tickets'] < data['num_tickets']:
        return jsonify({'error': 'Not enough tickets available'}), 400
    
    # Create booking
    new_booking = {
        'id': booking_id_counter,
        'event_id': data['event_id'],
        'event_name': data['event_name'],
        'customer_name': data['customer_name'],
        'customer_email': data['customer_email'],
        'num_tickets': int(data['num_tickets']),
        'total_price': float(data['total_price']),
        'booking_date': datetime.now().isoformat()
    }
    
    bookings.append(new_booking)
    booking_id_counter += 1
    
    # Update available tickets
    event['available_tickets'] -= data['num_tickets']
    
    return jsonify(new_booking), 201

# Cancel a booking (delete)
@app.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    global bookings
    booking = next((b for b in bookings if b['id'] == booking_id), None)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    # Return tickets to the event
    event = next((e for e in events if e['id'] == booking['event_id']), None)
    if event:
        event['available_tickets'] += booking['num_tickets']
    
    bookings = [b for b in bookings if b['id'] != booking_id]
    return jsonify({'message': 'Booking cancelled successfully'}), 200

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'API is running'}), 200

if __name__ == '__main__':
    # Note: Set debug=False in production
    # Use environment variable to control debug mode
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
