# NEON Hiring Portal

## Overview
The **NEON Hiring Portal** is a streamlined web application designed to facilitate candidate tracking, interview management, and hiring decisions for small teams. The portal allows interviewers to store candidate responses, rate their answers, and maintain shared access to interview data.

## Features
- **Candidate Application Tracking**: Applications are retrieved automatically from application database.
- **Interview Question Management**: Store and organize behavioral and technical interview questions.
- **Candidate Response & Scoring**: Interviewers can input responses and assign scores to each answer.
- **Shared Admin Access**: Administrative users can view, edit, and track hiring progress collaboratively.
- **Gmail OAuth Authentication**: Ensures secure login for administrative users.
- **Candidate Data Visualization**: View summarized insights on candidate scores and hiring progress.

## Tech Stack
- **Frontend**: React (JavaScript)
- **Backend**: Flask (Python)
- **Database**: Google Sheets (via Google Forms integration)
- **Authentication**: Gmail OAuth
- **Hosting**: TBD

## Installation & Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/neon-hiring-portal.git
   cd neon-hiring-portal
   ```
2. Install dependencies:
   ```sh
   npm install    # For frontend dependencies
   pip install -r requirements.txt   # For backend dependencies
   ```
3. Set up Google OAuth credentials:
   - Create a new project in Google Cloud Console.
   - Enable the Gmail API and Google Sheets API.
   - Configure OAuth 2.0 credentials and obtain a client ID & secret.
   - Store these credentials in an `.env` file:
     ```sh
     GOOGLE_CLIENT_ID=your_client_id
     GOOGLE_CLIENT_SECRET=your_client_secret
     ```
4. Start the development server:
   - **Frontend:**
     ```sh
     npm run dev
     ```
   - **Backend:**
     ```sh
     flask run
     ```
5. Access the portal at `http://localhost:3000` (or your configured port).

## Usage
1. **Admin Login**: Sign in using Gmail OAuth authentication.
2. **View Candidates**: See a list of applicants retrieved from the application database.
3. **Conduct Interviews**: Input candidate responses and assign scores.
4. **Collaborate with Admins**: View shared interview insights and track hiring progress.

## Roadmap
- Enable automated scheduling for interviews
- Add role-based access control for admin levels
- Improve UI/UX with real-time updates


