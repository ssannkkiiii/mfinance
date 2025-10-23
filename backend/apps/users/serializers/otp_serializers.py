from rest_framework import serializers

class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    action = serializers.ChoiceField(
        choices=['register', 'reset', 'change'],
        required=True
    )

    def validate_email(self, value):
        value = value.strip().lower()
        if not value or len(value) > 254:
            raise serializers.ValidationError("Invalid email format")
        return value

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    action = serializers.ChoiceField(
        choices=['register', 'reset', 'change'],
        required=True
    )
    otp = serializers.CharField(max_length=6, min_length=6)

    def validate_email(self, value):
        value = value.strip().lower()
        if not value or len(value) > 254:
            raise serializers.ValidationError("Invalid email format")
        return value

    def validate_otp(self, value):
        value = value.strip()
        if not value.isdigit():
            raise serializers.ValidationError("OTP must contain only digits")
        if len(value) != 6:
            raise serializers.ValidationError("OTP must be exactly 6 digits")
        return value