from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
import random
import pywhatkit as pwk
#import phonenumbers

Window.size = (500, 700)


prime_numbers = [6117333583, 2190898013, 6897674977, 4985733887, 8054236823,
                 7558758989, 7466408399, 5013907721, 6619635811, 8494065067,
                 9316795897, 8337278011, 8457027277, 9914912323, 8062610177,
                 1812291707, 2036929003, 6643077613, 9995519693, 3459453953,
                 4059985243, 1637963231, 4913252803, 6851601007, 6558038021,
                 2668948237, 5142269467, 5028748369, 8240489833, 9969200993,
                 5530575937, 4924139177, 9001696661, 6597135697, 2997473753,
                 4415743219, 9532993867, 7179026719, 2248981061, 2162899169,
                 9420499409, 2718865469, 7460148127, 5974631237, 2193027553,
                 1363416169, 4381383911, 2732716513, 1275656803, 2365756607,
                 2053300133, 4645424387, 6822645407, 7188311483, 7780603723,
                 2257456501, 3332415637, 8602407467, 2326738207, 6960483217]



def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi


def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True


def generate_key_pair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    n = p * q

    phi = (p-1) * (q-1)

    e = random.randrange(1, phi)

    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = multiplicative_inverse(e, phi)

    return ((e, n), (d, n))


def encrypt(pk, plaintext):
    key, n = pk
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher


def decrypt(pk, ciphertext):
    key, n = pk
    aux = [str(pow(char, key, n)) for char in ciphertext]
    plain = [chr(int(char2)) for char2 in aux]
    return ''.join(plain)


class StartWindow(Screen):
    def start(self):
        phone_number = self.ids.phone_number.text
        while True:
            p = prime_numbers[random.randint(0, 59)]
            q = prime_numbers[random.randint(0, 59)]
            if p != q:
                break
        public, private = generate_key_pair(p, q)
        self.ids.gen_key = public, private
        pwk.sendwhatmsg_instantly(phone_number, str(public))


class MainWindow(Screen):
    pass


class EncryptionWindow(Screen):
    def encryption(self):
        plaintext = self.ids.input.text

        if plaintext:
            public = self.ids.public_key.text

            if public:
                first, second = public.split(',')
                if first[0] == '(':
                    first_pk = int(first[1:])
                else:
                    first_pk = int(first)
                if second[-1] == ')':
                    second_pk = int(second[:-1])
                else:
                    second_pk = int(second)
                public_key = (first_pk, second_pk)
                encrypted_msg = encrypt(public_key, plaintext)
                self.ids.output.text = f'{encrypted_msg}'
            else:
                self.ids.public_key.text = ""
                self.ids.output.text = ""
        else:
            self.ids.output.text = "Please enter your message to encrypt!"


class DecryptionWindow(Screen):
    def decryption(self):
        private_key = self.manager.ids.start_win.ids.gen_key[1]
        if private_key:
            encrypted_msg = self.ids.input_ci.text
            encrypted_msg = encrypted_msg.split(",")
            encrypted_msg = list(map(int, encrypted_msg))
            plain_text = decrypt(private_key, encrypted_msg)
            self.ids.output.text = f'{plain_text}'
        else:
            self.ids.output.text = "Haven't generated keys"

    def clear_dec(self):
        self.ids.input_ci.text = ""
        self.ids.output.text = ""


class SendingWindow(Screen):
    def sending_via_whatsapp(self):
        cipher_text = self.manager.ids.enc_win.ids.output.text
        cipher_text = cipher_text[1:-1]
        phone_number = self.manager.ids.start_win.ids.phone_number.text
        pwk.sendwhatmsg_instantly(phone_number, cipher_text)
    def clear_enc(self):
        self.manager.ids.enc_win.ids.input.text = ""
        self.manager.ids.enc_win.ids.output.text = ""


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('mes_02.kv')


class MessengerApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MessengerApp().run()
