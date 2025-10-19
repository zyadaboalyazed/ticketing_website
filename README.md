# Ticketing Website 🎫

A modern, full-stack ticketing system for booking event tickets. Built with a responsive HTML/CSS/JavaScript frontend and a Python Flask backend.

## Features

- 🎨 Modern, responsive frontend design
- 🎫 Browse available events
- 📝 Book tickets for events
- 👤 Manage your bookings
- 🔄 Real-time ticket availability updates
- 📱 Mobile-friendly interface

## Tech Stack

### Frontend
- HTML5
- CSS3 (with modern Grid and Flexbox)
- Vanilla JavaScript (ES6+)
- Responsive design

### Backend
- Python 3.x
- Flask web framework
- Flask-CORS for cross-origin requests
- RESTful API design

## Project Structure

```
ticketing_website/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── index.html            # Main HTML file (served by Flask)
├── static/
│   ├── css/
│   │   └── style.css     # Styles
│   └── js/
│       └── app.js        # Frontend JavaScript
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/zyadaboalyazed/ticketing_website.git
   cd ticketing_website
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Flask backend**
   ```bash
   python app.py
   ```

2. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`
   - The frontend will be served automatically by Flask

## API Endpoints

### Events
- `GET /api/events` - Get all events
- `GET /api/events/<id>` - Get a specific event
- `POST /api/events` - Create a new event (admin)
- `PUT /api/events/<id>` - Update an event (admin)
- `DELETE /api/events/<id>` - Delete an event (admin)

### Bookings
- `GET /api/bookings` - Get all bookings
- `GET /api/bookings/<id>` - Get a specific booking
- `POST /api/bookings` - Create a new booking
- `DELETE /api/bookings/<id>` - Cancel a booking

### Health Check
- `GET /api/health` - Check API status

## Usage

### Booking a Ticket

1. Browse available events on the home page
2. Click "Book Tickets" on your desired event
3. Fill in your details:
   - Your name
   - Email address
   - Number of tickets
4. Review the total price
5. Click "Book Now" to confirm

### Managing Bookings

- View all your bookings in the "My Bookings" section
- Cancel any booking by clicking the "Cancel Booking" button

## Development

### Frontend Development
- Frontend files are located in the root and `static/` directory
- The JavaScript uses modern ES6+ features
- CSS uses Grid and Flexbox for responsive layouts

### Backend Development
- The Flask app uses in-memory storage for simplicity
- To use a real database, integrate SQLAlchemy or another ORM
- CORS is enabled for development purposes

## Future Enhancements

- [ ] User authentication and authorization
- [ ] Payment integration
- [ ] Email notifications
- [ ] Database integration (PostgreSQL/MySQL)
- [ ] Admin dashboard
- [ ] Ticket QR codes
- [ ] Event search and filtering
- [ ] User profiles

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please open an issue on GitHub.