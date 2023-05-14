import random
import string

def generate_password(length):
    """
    Generate a random password of the given length.
    """
    # Define the set of characters to choose from
    characters = string.ascii_letters + string.digits + string.punctuation
    
    # Generate a random password by choosing `length` characters from the set
    password = ''.join(random.choice(characters) for i in range(length))
    
    return password
