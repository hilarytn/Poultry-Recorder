import random
import string
from flask import current_app
from flask_mail import Message
from extensions import mail, redis_client



def generate_otp():
    # Generate a random 6-digit OTP
    otp = ''.join(random.choices(string.digits, k=6))
    return otp

def send_otp_email(email, otp):
    msg = Message("Your OTP Code", recipients=[email])
    msg.body = f"Your OTP code is: {otp}"
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

def generate_and_store_otp(user_id):
    otp = random.randint(100000, 999999)  # Generate 6-digit OTP

    redis_key = f"otp:{user_id}"
    expiration_time = current_app.config['OTP_EXPIRATION_TIME']  # Use expiration time from config

    # Store OTP in Redis with expiration time
    redis_client.setex(redis_key, expiration_time, otp)

    return otp

def verify_otp(user_id, otp_input):
    redis_key = f"otp:{user_id}"

    # Retrieve OTP from Redis
    stored_otp = redis_client.get(redis_key)

    if not stored_otp or stored_otp != otp_input:
        return False  # Invalid or expired OTP

    # OTP is valid, delete it from Redis
    redis_client.delete(redis_key)

    return True