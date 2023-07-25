from enum import Enum


class AccountStatus(Enum):
    Active, Closed, Canceled, Blacklisted, NONE = range(0, 5)
