from address import Address


class Person:
    def __init__(self, name, address: Address, email, phone):
        self.name = name
        self.address = address
        self.email = email
        self.phone = phone
