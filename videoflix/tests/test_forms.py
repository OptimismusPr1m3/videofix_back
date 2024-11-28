import pytest
from django import forms
from videoflix.forms import SignupForm, LoginForm, PasswordResetForm, PasswordResetVerifiedForm, EmailChangeForm, UsersMeChangeForm


@pytest.mark.django_db
def test_signup_form_valid_data():
    form_data = {
        'email': 'test@example.com',
        'password': 'SecurePassword123',
        'password2': 'SecurePassword123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    form = SignupForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_signup_form_password_mismatch():
    form_data = {
        'email': 'test@example.com',
        'password': 'SecurePassword123',
        'password2': 'DifferentPassword123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    form = SignupForm(data=form_data)
    assert not form.is_valid()
    assert "Confirmation password doesn't match." in form.errors['password2']


@pytest.mark.django_db
def test_login_form_valid_data():
    form_data = {
        'email': 'test@example.com',
        'password': 'SecurePassword123'
    }
    form = LoginForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_password_reset_form_valid_data():
    form_data = {
        'email': 'test@example.com',
    }
    form = PasswordResetForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_password_reset_verified_form_valid_data():
    form_data = {
        'password': 'NewPassword123',
        'password2': 'NewPassword123'
    }
    form = PasswordResetVerifiedForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_password_reset_verified_form_password_mismatch():
    form_data = {
        'password': 'NewPassword123',
        'password2': 'DifferentPassword123'
    }
    form = PasswordResetVerifiedForm(data=form_data)
    assert not form.is_valid()
    assert 'Passwörter stimmen nicht überein' in form.errors['password2']


@pytest.mark.django_db
def test_users_me_change_form_valid_data():
    form_data = {
        'first_name': 'Updated',
        'last_name': 'User',
        'date_of_birth': '1990-01-01'
    }
    form = UsersMeChangeForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_users_me_change_form_missing_data():
    form_data = {
        'first_name': 'Updated',
        'last_name': 'User',
    }
    form = UsersMeChangeForm(data=form_data)
    assert form.is_valid()  # Optional fields should not break form validation
