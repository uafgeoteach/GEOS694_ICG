"""
An example of a Python Class, which allows implementation of OOP concepts
"""
from random import randint

class Dog():
    """
    The Dog class allows instantiation of multiple types of dog
    """
    cute = True
    sound = "woof!"
    energy = 100

    def __init__(self, height, weight, food, name=None):
        """Set attributes for your dog"""
        self.height = height
        self.weight = weight
        self.food = food
        if name is None:
            self.name = self.assign_name()
        else:
            self.name = name

    def __str__(self):
        """Make Dog talk"""
        str_out = f"{self.sound}, {self.name} wants to {self.get_state()}"
        return str_out

    @staticmethod 
    def assign_name():  # <- Static methods do not require reference to `self`
        """Provides a randomly assigned name to your doggo"""
        names = ["Balto", "Lassy", "Spot", "Shadow", "Clifford"]
        return names[randint(0, 4)]

    @classmethod
    def bark(cls):
        print(cls.sound)

    def is_tired(self):
        """Check if the dog is tired"""
        return self.energy < 10

    def run(self, distance=1):
        """See dog run"""
        bmi = self.weight / self.height
        energy_expended = distance * bmi

        self.energy -= energy_expended

    def play(self,):
        """See dog play"""
        if self.is_tired():
            print("dog cannot play, too tired")
            return None
        if self.weight < 50:
            self.run(distance=1)
        else:
            self.run(distance=5)

    def eat(self, amount=25):
        """Watch dog eat"""
        if self.food == "dry":
            energy_gained = 1 * amount
        elif self.food == "wet":
            energy_gained == 2 * amount
        else:
            print("Dog can't eat that, it threw up")
            energy_gained = -1 * amount

        self.energy += energy_gained

    def get_state(self):
        """Figure out what Dog wants to do"""
        if self.is_tired:
            state = "eat"
        else:
            state = "play"
        return state

if __name__ == "__main__":
    my_dog = Dog(height=5, weight=20, food="dry")
    my_dog.run(distance=5)
    my_dog.eat(amount=10)
    my_dog.play()
    print(my_dog)
