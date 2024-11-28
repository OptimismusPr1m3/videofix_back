This is the backend project for the frontend application Videoflix/Chill'N'Flix. It is based on Python and uses the Django framework. 
The corresponding frontend can be found here: [VideoflixFrontend](https://github.com/OptimismusPr1m3/videoflix_front)

## Project Structure

- **videofix_back/**: Contains the Django application code.
- **accounts/**: Contains model and views/serializer for account management.
- **video/**: Contains models and views/serializers for video-items which can be uploaded.
- **manage.py**: Befehlszeilenwerkzeug für die Django-Anwendung.
- **requirements.txt**: Liste der Python-Abhängigkeiten.


## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/OptimismusPr1m3/videofix_back
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Apply database migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
4. Start the server:
    ```bash
    python ma

## Contributing

Pull requests are welcome.

## Testing 

This project uses pytest for testing. To ensure the tests run correctly, you should use an SQLite3 database as it is designed for testing.

1. Prerequisites
    * Python 3.x
    * SQLite3 (usually included by default with Django)


2. Testing with pytest
   - **pip install -r requirements.txt /**
   - **pytest /**

3. Database Configuration

  **DATABASES = {**
    **'default': {**
      **'ENGINE': 'django.db.backends.sqlite3',**
        **'NAME': BASE_DIR / 'db.sqlite3',**
    **}**
**}**

4. Additional Notes 
    * PostgreSQL is not required and should not be used for testing to ensure an optimal and fast testing environment.


///////////////////////////////////////////////////// GERMAN /////////////////////////////////////////////////////

Dies ist das Backend-Projekt für die Frontend Anwendung Videoflix/Chill'N'Flix. Es basiert auf Python und verwendet das Django-Framework.
Das dazughehörige Frontend findet man hier: [VideoflixFrontend](https://github.com/OptimismusPr1m3/videoflix_front)

## Projektstruktur

- **videofix_back/**: Enthält den Django-Anwendungscode.
- **accounts/**: Enthält Modelle und Views/Serializer für die Kontoverwaltung.
- **video/**: Enthält Modelle und Views/Serializer für Videoelemente, die hochgeladen werden können.
- **manage.py**: Befehlszeilenwerkzeug für die Django-Anwendung.
- **requirements.txt**: Liste der Python-Abhängigkeiten.

## Installation

1. Repository klonen:
    ```bash
    git clone https://github.com/OptimismusPr1m3/videofix_back
    ```
2. Abhängigkeiten installieren:
    ```bash
    pip install -r requirements.txt
    ```
3. Datenbankmigrationen durchführen:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
4. Server starten:
    ```bash
    python manage.py runserver
    ```

## Mitwirken

Pull-Requests sind willkommen.

## Testing 

In diesem Projekt werden die Tests mit pytest durchgeführt. Um sicherzustellen, dass die Tests korrekt ausgeführt werden, solltest du eine SQLite3-Datenbank verwenden, da diese für die Tests konzipiert wurde.

1. Voraussetzungen
    * Python 3.x
    * SQLite3 (wird in der Regel standardmäßig mit Django verwendet)


2. Testen mit pytest
   - **pip install -r requirements.txt /**
   - **pytest /**

3. Konfiguration der Datenbank

  **DATABASES = {**
    **'default': {**
      **'ENGINE': 'django.db.backends.sqlite3',**
        **'NAME': BASE_DIR / 'db.sqlite3',**
    **}**
**}**

4. Weitere Hinweise 
    * PostgreSQL ist nicht erforderlich und sollte nicht für Tests verwendet werden, um eine optimale und schnelle Testumgebung zu gewährleisten.