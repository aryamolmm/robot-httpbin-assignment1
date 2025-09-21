from faker import Faker

fake = Faker()

def generate_user_data():
    """Generate random user data dictionary."""
    return {
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
        "phone": fake.phone_number()
    }
