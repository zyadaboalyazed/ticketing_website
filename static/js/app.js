// API Base URL - will be configured based on environment
const API_URL = 'http://localhost:5000/api';

// State management
let currentEvents = [];
let currentBookings = [];
let selectedEvent = null;

// DOM Elements
const eventsListEl = document.getElementById('events-list');
const bookingsListEl = document.getElementById('bookings-list');
const bookingFormSection = document.getElementById('booking-form-section');
const bookingForm = document.getElementById('booking-form');
const notificationEl = document.getElementById('notification');

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    loadEvents();
    loadBookings();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Booking form submission
    bookingForm.addEventListener('submit', handleBookingSubmit);

    // Cancel booking form
    document.getElementById('cancel-booking').addEventListener('click', () => {
        bookingFormSection.classList.add('hidden');
        selectedEvent = null;
    });

    // Update total price when number of tickets changes
    document.getElementById('num-tickets').addEventListener('input', updateTotalPrice);

    // Smooth scroll for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// Load events from API
async function loadEvents() {
    try {
        const response = await fetch(`${API_URL}/events`);
        if (!response.ok) throw new Error('Failed to load events');
        
        currentEvents = await response.json();
        displayEvents(currentEvents);
    } catch (error) {
        console.error('Error loading events:', error);
        // Display sample events if API is not available
        displaySampleEvents();
    }
}

// Display sample events (for when backend is not running)
function displaySampleEvents() {
    const sampleEvents = [
        {
            id: 1,
            name: 'Rock Concert 2025',
            date: '2025-11-15',
            venue: 'Madison Square Garden',
            price: 75.00,
            available_tickets: 500
        },
        {
            id: 2,
            name: 'Jazz Night',
            date: '2025-11-20',
            venue: 'Blue Note',
            price: 45.00,
            available_tickets: 150
        },
        {
            id: 3,
            name: 'Theater Play - Hamlet',
            date: '2025-11-25',
            venue: 'Broadway Theater',
            price: 60.00,
            available_tickets: 300
        },
        {
            id: 4,
            name: 'Sports Game - Finals',
            date: '2025-12-01',
            venue: 'Stadium Arena',
            price: 120.00,
            available_tickets: 1000
        }
    ];
    
    currentEvents = sampleEvents;
    displayEvents(sampleEvents);
}

// Display events in the UI
function displayEvents(events) {
    if (!events || events.length === 0) {
        eventsListEl.innerHTML = '<p class="text-center">No events available at the moment.</p>';
        return;
    }

    eventsListEl.innerHTML = events.map(event => `
        <div class="event-card" data-event-id="${event.id}">
            <div class="event-card-header">
                <h3>${event.name}</h3>
            </div>
            <div class="event-card-body">
                <div class="event-info">
                    <p><strong>📅 Date:</strong> ${formatDate(event.date)}</p>
                    <p><strong>📍 Venue:</strong> ${event.venue}</p>
                    <p><strong>💰 Price:</strong> $${event.price.toFixed(2)}</p>
                    <p><strong>🎫 Available:</strong> ${event.available_tickets} tickets</p>
                </div>
            </div>
            <div class="event-card-footer">
                <button class="btn btn-primary btn-full" onclick="openBookingForm(${event.id})">
                    Book Tickets
                </button>
            </div>
        </div>
    `).join('');
}

// Open booking form for selected event
function openBookingForm(eventId) {
    selectedEvent = currentEvents.find(e => e.id === eventId);
    if (!selectedEvent) {
        showNotification('Event not found', 'error');
        return;
    }

    // Populate form
    document.getElementById('event-name').value = selectedEvent.name;
    document.getElementById('num-tickets').value = 1;
    updateTotalPrice();

    // Show form and scroll to it
    bookingFormSection.classList.remove('hidden');
    bookingFormSection.scrollIntoView({ behavior: 'smooth' });
}

// Update total price based on number of tickets
function updateTotalPrice() {
    if (!selectedEvent) return;
    
    const numTickets = parseInt(document.getElementById('num-tickets').value) || 1;
    const total = (selectedEvent.price * numTickets).toFixed(2);
    document.getElementById('total-price').value = `$${total}`;
}

// Handle booking form submission
async function handleBookingSubmit(e) {
    e.preventDefault();

    if (!selectedEvent) {
        showNotification('Please select an event', 'error');
        return;
    }

    const booking = {
        event_id: selectedEvent.id,
        event_name: selectedEvent.name,
        customer_name: document.getElementById('customer-name').value,
        customer_email: document.getElementById('customer-email').value,
        num_tickets: parseInt(document.getElementById('num-tickets').value),
        total_price: selectedEvent.price * parseInt(document.getElementById('num-tickets').value)
    };

    try {
        const response = await fetch(`${API_URL}/bookings`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(booking)
        });

        if (!response.ok) throw new Error('Failed to create booking');

        const result = await response.json();
        showNotification('Booking created successfully!', 'success');
        
        // Reset form
        bookingForm.reset();
        bookingFormSection.classList.add('hidden');
        selectedEvent = null;

        // Reload data
        loadEvents();
        loadBookings();

        // Scroll to bookings section
        document.getElementById('bookings').scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error('Error creating booking:', error);
        showNotification('Failed to create booking. Please try again.', 'error');
    }
}

// Load bookings from API
async function loadBookings() {
    try {
        const response = await fetch(`${API_URL}/bookings`);
        if (!response.ok) throw new Error('Failed to load bookings');
        
        currentBookings = await response.json();
        displayBookings(currentBookings);
    } catch (error) {
        console.error('Error loading bookings:', error);
        bookingsListEl.innerHTML = '<p class="text-center">Unable to load bookings. Please make sure the backend is running.</p>';
    }
}

// Display bookings in the UI
function displayBookings(bookings) {
    if (!bookings || bookings.length === 0) {
        bookingsListEl.innerHTML = '<p class="text-center">No bookings yet. Book your first event!</p>';
        return;
    }

    bookingsListEl.innerHTML = bookings.map(booking => `
        <div class="booking-card" data-booking-id="${booking.id}">
            <h3>${booking.event_name}</h3>
            <div class="booking-info">
                <p><strong>Customer:</strong> ${booking.customer_name}</p>
                <p><strong>Email:</strong> ${booking.customer_email}</p>
                <p><strong>Tickets:</strong> ${booking.num_tickets}</p>
                <p><strong>Total:</strong> $${booking.total_price.toFixed(2)}</p>
                <p><strong>Booked on:</strong> ${formatDate(booking.booking_date)}</p>
            </div>
            <div class="booking-actions">
                <button class="btn btn-danger" onclick="cancelBooking(${booking.id})">
                    Cancel Booking
                </button>
            </div>
        </div>
    `).join('');
}

// Cancel a booking
async function cancelBooking(bookingId) {
    if (!confirm('Are you sure you want to cancel this booking?')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/bookings/${bookingId}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to cancel booking');

        showNotification('Booking cancelled successfully', 'success');
        
        // Reload data
        loadEvents();
        loadBookings();
    } catch (error) {
        console.error('Error cancelling booking:', error);
        showNotification('Failed to cancel booking. Please try again.', 'error');
    }
}

// Show notification
function showNotification(message, type = 'info') {
    notificationEl.textContent = message;
    notificationEl.className = `notification ${type}`;
    notificationEl.classList.remove('hidden');

    setTimeout(() => {
        notificationEl.classList.add('hidden');
    }, 3000);
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}
