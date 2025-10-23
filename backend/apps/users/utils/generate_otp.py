from django.core.cache import cache
import secrets
import logging

logger = logging.getLogger(__name__)

def generate_otp():
    return secrets.randbelow(900000) + 100000

def store_otp(email, purpose, otp, ttl=300):
    try:
        cache.set(f"otp:{purpose}:{email}", otp, ttl)
        logger.info(f"OTP stored for {email} with purpose {purpose}")
        return True
    except Exception as e:
        logger.error(f"Failed to store OTP for {email}: {str(e)}")
        return False

def verify_otp(email, purpose, otp):
    try:
        stored = cache.get(f"otp:{purpose}:{email}")
        is_valid = stored and str(stored) == str(otp)
        
        if is_valid:
            cache.delete(f"otp:{purpose}:{email}")
            cache.set(f"verified:{purpose}:{email}", True, 600)
            logger.info(f"OTP verified successfully for {email}")
        else:
            logger.warning(f"Invalid OTP for {email}")
            
        return is_valid
    except Exception as e:
        logger.error(f"Failed to verify OTP for {email}: {str(e)}")
        return False

def is_verified(email, purpose):
    try:
        return cache.get(f"verified:{purpose}:{email}", False)
    except Exception as e:
        logger.error(f"Failed to check verification for {email}: {str(e)}")
        return False

def clear_verification(email, purpose):
    try:
        cache.delete(f"verified:{purpose}:{email}")
        logger.info(f"Verification cleared for {email} with purpose {purpose}")
        return True
    except Exception as e:
        logger.error(f"Failed to clear verification for {email}: {str(e)}")
        return False