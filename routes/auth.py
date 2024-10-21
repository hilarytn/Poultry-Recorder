from flask import Blueprint, request, jsonify, current_app, url_for
from models.user import User
from extensions import db, mail
from schemas.user_schema import UserSchema
from services.auth_service import generate_access_token, generate_verification_token
from flask_jwt_extended import create_access_token, decode_token
from utils.otp import generate_otp, send_otp_email, generate_and_store_otp, verify_otp
from flask_mail import Message
from datetime import datetime, timedelta


auth_bp = Blueprint('auth', __name__)

user_schema = UserSchema()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate the input
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Check if email or username already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already exists"}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already exists"}), 400

    # Create new user
    user = User(
        fullname=data['fullname'],
        username=data['username'],
        email=data['email']
    )

    # Hash the password
    user.set_password(data['password'])

    # Generate verification token
    verification_token = generate_verification_token(user)
    user.verification_token = verification_token 

    db.session.add(user)
    db.session.commit()

    # Send verification email
    verification_link = url_for('auth.verify_email', token=verification_token, _external=True)
    msg = Message(subject="Email Verification", 
                  sender=current_app.config['MAIL_USERNAME'], 
                  recipients=[user.email])
    msg.body = f"Please click the link to verify your email: {verification_link}"
    
    try:
        mail.send(msg)
    except Exception as e:
        return jsonify({"message": f"Failed to send email: {str(e)}"}), 500

    return jsonify({"message": f"User registered successfully. A verification link has been sent to your email {user.email} "}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate input data
    if 'email_or_username' not in data or 'password' not in data:
        return jsonify({"message": "Missing email/username or password"}), 400

    user = User.query.filter(
        (User.email == data['email_or_username']) | 
        (User.username == data['email_or_username'])
        ).first()

    if not user or not user.check_password(data['password']):
        return jsonify({"message": "Invalid credentials"}), 401

    if not user.is_verified:
        return jsonify({"message": "Please verify your email before logging in."}), 403
    
    #     # Request OTP after successful password check
    # otp_response = request_login_otp() 
    # if otp_response[1] != 200:
    #     return otp_response

    # return jsonify({"message": "Please check your email for the OTP."}), 200

    access_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=15))
    return jsonify({"access_token": access_token,
                    "id": user.id,
                    "fullname": user.fullname,
                    "username": user.username,
                    "email": user.email}), 200

@auth_bp.route('/all', methods=['GET'])
def all_users():
    users = User.query.all()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)

@auth_bp.route('/request_otp', methods=['POST'])
def request_otp():
    data = request.get_json()
    email = data.get('email')

    otp = generate_otp()

    # Send the OTP via email
    send_otp_email(email, otp)

    return {"msg": "OTP sent to your email."}, 200

@auth_bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    try:
        decoded_token = decode_token(token)
        email = decoded_token['sub']  # The identity is usually stored in 'sub'
        user = User.query.filter_by(email=email).first()

        if user is None or user.is_verified:
            return jsonify({"message": "Invalid or expired token."}), 400

        # Mark user as verified
        user.is_verified = True
        user.verification_token = None  # Clear the token after verification
        db.session.commit()

        return jsonify({"message": "Email verified successfully."}), 200

    except Exception as e:
        return jsonify({"message": "Invalid verification token."}), 400


@auth_bp.route('/resend_verification', methods=['POST'])
def resend_verification():
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    if user.is_verified:
        return jsonify({"message": f"Email {user.email} is already verified"}), 400

    # Generate a new verification token
    verification_token = generate_verification_token(user)
    user.verification_token = verification_token
    user.verification_token_expiry = datetime.utcnow() + timedelta(hours=24)

    db.session.commit()

    # Send the verification email
    verification_link = url_for('auth.verify_email', token=verification_token, _external=True)
    msg = Message(subject="Resend Email Verification",
                  sender=current_app.config['MAIL_USERNAME'], 
                  recipients=[user.email])
    msg.body = f"Please click the link to verify your email: {verification_link}\n This link expires in 24 hours"
    
    try:
        mail.send(msg)
    except Exception as e:
        return jsonify({"message": f"Failed to send email: {str(e)}"}), 500

    return jsonify({"message": f"Verification email sent again to {user.email} . Please check your inbox."}), 200

@auth_bp.route('/request-otp', methods=['POST'])
def request_login_otp():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    otp = generate_and_store_otp(user.id)
    print(otp)

    return jsonify({"message": "OTP sent"}), 200

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp_route():
    data = request.get_json()
    user_id = data.get('user_id')
    otp_input = data.get('otp')

    if verify_otp(user_id, otp_input):
        # Issue access token or perform login actions
        access_token = create_access_token(identity=user_id)
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"message": "Invalid or expired OTP"}), 401