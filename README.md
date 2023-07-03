# Book Author api

This api allows you to manage books and their pages through a simple RESTful API by django rest-framework.

## Prerequisites


- Python 3.6 or higher
- pip (Python package installer)

## Getting Started

1. **Clone the repository:**

   ```
   git clone https://github.com/MarioMedWilson/docsperts-bookauthorapi-backend.git
   ```

2. **Change into the project directory:**

   ```
   cd docsperts-bookauthorapi-backend
   ```

3. **Create a virtual environment (optional but recommended):**

   - Create a new virtual environment:

     ```
     python -m venv .venv
     ```

   - Activate the virtual environment:

       ```
       source .venv/Scripts/activate
       ```


4. **Install project dependencies:**

   ```
   pip install -r requirements.txt
   ```

5. **Apply database migrations:**

   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start the development server:**

   ```
   python manage.py runserver
   ```

7. **Access the Book App:**

   - Open your web browser and visit `http://localhost:8000/` to access the BookAuthorAPI.
   - You could find all the urls in [link](https://github.com/MarioMedWilson/docsperts-bookauthorapi-backend/blob/master/bookauthorapi/urls.py).
