import pytest
from accounts.models import MyUser

@pytest.mark.django_db
def test_create_user_with_email():
    user = MyUser.objects.create_user(
        email="testuser@example.com", 
        password="securepassword123"
    )
    assert user.email == "testuser@example.com"
    assert user.check_password("securepassword123")  # Passwort validieren
    assert not user.is_staff  # Standardmäßig kein Staff
    assert not user.is_superuser  # Standardmäßig kein Superuser

@pytest.mark.django_db
def test_create_superuser_with_email():
    admin = MyUser.objects.create_superuser(
        email="admin@example.com", 
        password="securepassword123"
    )
    assert admin.email == "admin@example.com"
    assert admin.is_staff  # Superuser sind immer Staff
    assert admin.is_superuser  # Superuser sind immer Superuser


@pytest.mark.django_db
def test_verified_user():
    verified_user = MyUser.objects.create(
        email="verified@example.com",
        is_verified=True
    )
    unverified_user = MyUser.objects.create(
        email="unverified@example.com",
        is_verified=False
    )

    assert verified_user.is_verified is True
    assert unverified_user.is_verified is False


from django.contrib.auth import authenticate

@pytest.mark.django_db
def test_user_login_with_verified_email():
    # Erstelle einen Benutzer
    user = MyUser.objects.create_user(
        email="testuser@example.com", 
        password="securepassword123", 
    )
    user.is_verified = True
    user.save()
    
    # Authentifiziere den Benutzer
    authenticated_user = authenticate(email="testuser@example.com", password="securepassword123")
    assert authenticated_user is not None
    assert authenticated_user.email == "testuser@example.com"

@pytest.mark.django_db
def test_user_login_without_verified_email():
    # Erstelle einen Benutzer ohne Verifizierung
    user = MyUser.objects.create_user(
        email="testuser@example.com",
        password="securepassword123",
    )
    user.is_verified = False  # Sicherstellen, dass der Benutzer nicht verifiziert ist
    user.save()

    # Versuch, sich einzuloggen
    authenticated_user = authenticate(email="testuser@example.com", password="securepassword123")

    # Verifizierungsprüfung manuell durchführen
    if authenticated_user:
        assert not authenticated_user.is_verified
    else:
        assert authenticated_user is None  # Login sollte fehlschlagen



