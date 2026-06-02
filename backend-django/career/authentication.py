import json
import urllib.request

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions


class FirebaseAuthentication(authentication.BaseAuthentication):
    """
    Firebase bearer-token authentication.
    """

    def authenticate(self, request):
        header = authentication.get_authorization_header(request).decode("utf-8")
        if not header.startswith("Bearer "):
            return None

        token = header.replace("Bearer ", "", 1).strip()
        try:
            import firebase_admin
            from firebase_admin import auth, credentials
        except ImportError as exc:
            raise exceptions.AuthenticationFailed("Firebase Admin SDK is not installed.") from exc

        if not firebase_admin._apps and settings.FIREBASE_CREDENTIALS_PATH:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)

        if firebase_admin._apps:
            try:
                decoded_token = auth.verify_id_token(token)
            except Exception as exc:
                raise exceptions.AuthenticationFailed("Invalid Firebase token.") from exc
        else:
            decoded_token = verify_firebase_token_with_public_certs(token)

        email = decoded_token.get("email")
        uid = decoded_token.get("uid") or decoded_token.get("user_id") or decoded_token.get("sub")
        if not email or not uid:
            raise exceptions.AuthenticationFailed("Firebase token missing email or uid.")

        user, _ = User.objects.get_or_create(
            username=email,
            defaults={"email": email, "first_name": decoded_token.get("name", "")},
        )
        return user, None


def verify_firebase_token_with_public_certs(token):
    """
    Verify Firebase ID tokens without a service-account file.
    Use this for local MVP testing. Production can use FIREBASE_CREDENTIALS_PATH.
    """
    if not settings.FIREBASE_PROJECT_ID:
        raise exceptions.AuthenticationFailed("Firebase project id is missing.")

    try:
        import jwt
        from cryptography import x509
    except ImportError as exc:
        raise exceptions.AuthenticationFailed("Firebase token verification dependencies are not installed.") from exc

    try:
        header = jwt.get_unverified_header(token)
        key_id = header.get("kid")
        with urllib.request.urlopen(
            "https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com",
            timeout=10,
        ) as response:
            certs = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise exceptions.AuthenticationFailed("Could not load Firebase public certificates.") from exc

    cert = certs.get(key_id)
    if not cert:
        raise exceptions.AuthenticationFailed("Firebase token key id is not recognized.")

    issuer = f"https://securetoken.google.com/{settings.FIREBASE_PROJECT_ID}"
    try:
        public_key = x509.load_pem_x509_certificate(cert.encode("utf-8")).public_key()
        return jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=settings.FIREBASE_PROJECT_ID,
            issuer=issuer,
            leeway=300,
        )
    except Exception as exc:
        raise exceptions.AuthenticationFailed("Invalid Firebase token.") from exc
