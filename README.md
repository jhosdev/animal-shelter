# Animal Shelter Project

This project consists of a REST API for an animal shelter developed with Django Rest Framework and a web client built with Next.js. The system allows managing animals, volunteers, adopters, and adoption processes.

## Technologies Used

- Backend:
  - Python 3.12
  - Django Rest Framework
  - Simple JWT for authentication
- Frontend:
  - Next.js 14
  - React with TypeScript
  - Mantine UI
  - Next.js App Router
- Database:
  - PostgreSQL (configured with Docker Compose for local development)

## Project Setup

### Backend (Django Rest Framework)

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv env
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     .\env\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source env/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Configure environment variables:
   - Copy the `.env.example` file to `.env`
   - Adjust the variables in `.env` according to your local setup

6. Run migrations:
   ```
   python manage.py migrate
   ```

7. Start the development server:
   ```
   python manage.py runserver
   ```

8. To run tests:
   ```
   python manage.py test
   ```

### Frontend (Next.js)

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Configure the API URL:
   - Copy the `.env.example` file to `.env.local`
   - Adjust the `NEXT_PUBLIC_API_URL` variable in `.env.local`

4. Start the development server:
   ```
   npm run dev
   ```

## Database (PostgreSQL with Docker)

To set up the PostgreSQL database using Docker Compose:

1. Make sure you have Docker and Docker Compose installed.
2. From the project root, run:
   ```
   docker-compose up -d
   ```

## Deployment

- Frontend: Deployed on Vercel
- Backend and Database: Deployed on Render.com

## Features Achieved

1. Animal Management:
   - List, create, update, and delete animals in the shelter
   - Filter animals by type (dog or cat) and adoption status

2. Volunteer Management:
   - Volunteer registration and authentication
   - List, update, and delete volunteer profiles
   - Assign tasks and manage volunteer schedules

3. Adopter Management:
   - Adopter registration and authentication
   - List, update, and delete adopter profiles
   - Adoption application process

4. Adoption Process:
   - Create and manage adoption requests
   - Track the status of adoptions
   - Approval or rejection of requests by volunteers
   - Synchronize adoption information with adopters and animals

5. Authentication and Authorization:
   - Implementation of JWT for secure authentication
   - Different access levels for administrators, volunteers, and adopters

6. User Interface:
   - Responsive design using Mantine UI
   - Intuitive navigation with Next.js App Router
   - Forms with validation for data entry

## Additional Notes

- The project uses Django Rest Framework for the REST API.
- Authentication is handled with Simple JWT.
- The frontend is built with Next.js 14, using the App Router and Mantine UI for the user interface.
- Tests have been implemented in Django to ensure the quality of the backend code.
