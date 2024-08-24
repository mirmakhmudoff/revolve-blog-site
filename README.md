# Revolve Blog Site

Revolve is a modern and responsive blog platform built using Django. It provides a comprehensive solution for managing blog posts, categories, and media, with a user-friendly interface and robust backend.

## Features

- **Blog Management**: Create, edit, and delete blog posts with ease.
- **Category Management**: Organize posts into categories for better navigation.
- **User Authentication**: Secure login and registration for users.
- **Media Handling**: Upload and manage images and other media files.
- **Responsive Design**: Accessible on all devices, from desktops to smartphones.
- **Search Functionality**: Quickly find posts using the integrated search feature.

## Project Structure

- **revolve/**: Contains the main Django app logic, including models, views, and URLs.
- **config/**: Configuration files for settings, URL routing, and other app configurations.
- **static/**: Static assets such as CSS, JavaScript, and images.
- **templates/**: HTML templates used by the Django app.
- **media/**: Directory for user-uploaded files.
- **manage.py**: Django's command-line utility for administrative tasks.

## Installation

### Prerequisites

- Python 3.x
- Django 3.x (as specified in `requirements.txt`)
- Virtualenv (optional but recommended)

### Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/mirmakhmudoff/revolve-blog-site.git
    cd revolve-blog-site
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations to set up the database:**

    ```bash
    python manage.py migrate
    ```

5. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

6. **Access the site:**

    Open your browser and go to `http://127.0.0.1:8000/`.

## Usage

- **Admin Panel**: Access the admin panel at `http://127.0.0.1:8000/admin/` to manage posts, users, and other resources.
- **Static and Media Files**: Place your static files in the `static/` directory and media files in the `media/` directory.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any enhancements, bug fixes, or additional features.
