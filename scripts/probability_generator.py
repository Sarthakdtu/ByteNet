import random
def get_prob():
    random_number = random.randint(0, 5)
    prob = random_number > 4
    return prob