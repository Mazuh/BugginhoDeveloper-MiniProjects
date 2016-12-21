# pylint: disable=C0103
# pylint: disable=C0325

""" Main script to simulate some kind of ATM (Automatic Teller Machine). """

from persistence import Persistence
from user import User

data = Persistence()

# main user
user = User('agency', 'account', 'pass')
user.hash_password()
print(user.password)

# other users
friend1 = User('agency', 'account1', 'pass1')
friend1.hash_password()

friend2 = User('agency', 'account2', 'pass2')
friend2.hash_password()

# assembling all users for this test
data.users.append(user)
data.users.append(friend1)
data.users.append(friend2)
