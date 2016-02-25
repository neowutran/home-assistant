import pyqrcode
import pyotp
import time

class TOTP:
    def __init__(self):
        self.generate_secret()

    def generate_secret(self):
        self.secret = 'JEKWNRN2DKRB6VSF'
        #self.secret = pyotp.random_base32()
        #print(self.secret)
        self.totp = pyotp.TOTP(self.secret)
        self.url = pyqrcode.create(self.totp.provisioning_uri("neowutran@gmail.com"))

    def generate_QR_code(self):
        print(self.url.terminal('black', 'white'))

    def print_code(self):
        while True:
            print(self.totp.now())
            time.sleep(5)

    def verify(self, password):
        return self.totp.verify(password)

def main():
    totp = TOTP()
    totp.generate_QR_code()
    password = input('code: ')
    print(totp.verify(password))
    totp.print_code()

if __name__ == "__main__":
    main()
