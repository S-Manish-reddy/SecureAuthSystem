import pyotp
import qrcode


def generate_2fa_secret():

    return pyotp.random_base32()


def generate_otp_uri(
    email: str,
    secret: str
):

    return pyotp.totp.TOTP(secret).provisioning_uri(
        name=email,
        issuer_name="SecureAuthSystem"
    )


def verify_otp(
    secret: str,
    otp: str
):

    totp = pyotp.TOTP(secret)

    return totp.verify(otp)


def generate_qr_code(
    uri: str,
    file_path: str
):

    qr = qrcode.make(uri)

    qr.save(file_path)