# Live Dining Status

A Flask web application that scrapes and displays live dining hall menu information from Smith College.

## Features

- Real-time dining hall menu scraping
- Time-based meal display (breakfast, lunch, dinner)
- Interactive dropdown selection for different dining halls
- Responsive web interface

## Local Development

### Prerequisites

- Python 3.9+
- pip

### Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set environment variables (optional for development):
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```
4. Run the application:
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`.

## Deployment on Render

### Method 1: Using render.yaml (Recommended)

1. Fork this repository to your GitHub account
2. Connect your GitHub repository to Render
3. Render will automatically detect the `render.yaml` file and use it for deployment
4. The app will be deployed with the following configuration:
   - Python 3.9.16
   - Gunicorn WSGI server
   - Automatic SSL certificate
   - Auto-generated secure SECRET_KEY

### Method 2: Manual Setup

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the following settings:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Python Version**: 3.9.16

4. Set the following environment variables:
   - `SECRET_KEY`: Generate a secure random string
   - `FLASK_ENV`: `production`

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Flask session secret key | Yes (production) | `dev-key-change-in-production` |
| `FLASK_ENV` | Flask environment mode | No | `development` |
| `PORT` | Application port | No | `5000` |

## Project Structure

```
live-dining-status/
├── app.py              # Main Flask application
├── scraper.py          # Web scraping logic for dining hall menus
├── requirements.txt    # Python dependencies
├── render.yaml        # Render deployment configuration
├── Procfile           # Alternative deployment configuration
├── .env.example       # Environment variable template
├── README.md          # This file
└── templates/         # HTML templates
    ├── index.html     # Main page with dining hall selection
    └── dining.html    # Menu display page
```

## How It Works

1. **Web Scraping**: The `scraper.py` module fetches live menu data from Smith College's dining services website
2. **Data Processing**: Menu items are parsed and organized by dining hall and meal time
3. **Time-Based Display**: The application automatically shows the appropriate meal (breakfast/lunch/dinner) based on the current time
4. **Session Management**: User selections are stored in Flask sessions for a seamless experience

## Time-Based Meal Logic

- **Breakfast**: 7:00 AM - 12:00 PM
- **Lunch**: 12:00 PM - 5:00 PM  
- **Dinner**: 5:00 PM - 8:00 PM

## Error Handling

The application includes graceful error handling:
- If the dining services website is unavailable, fallback data is provided
- Invalid dining hall selections redirect to the main page
- Missing menu data is handled with appropriate user feedback

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## License

This project is for educational purposes. Please respect Smith College's terms of service when using their dining services data.