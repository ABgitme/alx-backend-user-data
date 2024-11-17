#!/usr/bin/env python3
"""handle login via session-based authentication"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth_login():
    """ POST /api/v1/auth_session/login
    Handles user login with session authentication.
    """
    # Retrieve email and password from form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email is provided
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Check if password is provided
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve the user based on email
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]

    # Verify if the password is correct
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Import auth and create a session ID
    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    # Create a JSON response for the user
    user_data = user.to_json()
    response = make_response(jsonify(user_data))

    # Set the session ID in the response cookie
    session_name = os.getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)

    return response
