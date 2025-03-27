# Food-Stat Server

This README provides instructions on how to set up the environment, install dependencies, and run the Flask application.

## Prerequisites

- Python 3.7 or higher installed on your system.
- `pip` (Python package manager) installed.

## Installation

1. **Clone the Repository**  
    Clone this repository to your local machine:
    ```bash
    git clone <repository-url>
    cd Food-Stat/server
    ```

2. **Set Up a Virtual Environment**  
    Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On macOS/Linux
    venv\Scripts\activate      # On Windows
    ```

3. **Install Dependencies**  
    Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4. **Install `uv` and Sync It**  
    Install `uv` (if applicable) and sync it:
    ```bash
    pip install uv
    ```

## Running the Flask Application

1. **Activate the Virtual Environment**  
    Ensure the virtual environment is activated:
    ```bash
    source venv/bin/activate   # On macOS/Linux
    venv\Scripts\activate      # On Windows
    ```

2. **Run the Flask App**  
    Start the Flask development server:
    ```bash
    flask run
    ```

3. **Access the Application**  
    Open your browser and navigate to `http://127.0.0.1:5000`.

## Deactivating the Virtual Environment

When you're done, deactivate the virtual environment:
```bash
deactivate
```

## Notes

- Ensure `FLASK_APP` is set if the app doesn't run:
  ```bash
  export FLASK_APP=app.py   # On macOS/Linux
  set FLASK_APP=app.py      # On Windows
  ```
