import random
import string
import requests


def random_email_generator(size=5, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


email = random_email_generator() + '@yopmail.com'
print(email)


def random_username_generator(length=8):
    characters = string.ascii_letters + string.digits
    username = ''.join(random.choice(characters) for i in range(length))

    if username[0].isdigit():
        username = random.choice(string.ascii_letters) + username[1:]

    return username


random_username = random_username_generator(10)


def get_random_word_from_api():
    try:
        response = requests.get("https://api.datamuse.com/words?ml=meaning_like&max=20000")
        response.raise_for_status()
        words = [item["word"] for item in response.json()]
        return random.choice(words)
    except requests.RequestException as e:
        print("Datamuse API request failed:", e)
        return None


# Example
print("Random word:", get_random_word_from_api())

def random_password_generator(length=12):

    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")


    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special_characters = string.punctuation

    password = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits),
        random.choice(special_characters)
    ]

    all_characters = uppercase + lowercase + digits + special_characters
    password += [random.choice(all_characters) for i in range(length - 4)]

    random.shuffle(password)

    return ''.join(password)


random_password = random_password_generator(12)

