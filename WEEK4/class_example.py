"""
An example of a Python Class, which allows implementation of OOP concepts
"""

class Dog():
    """
    The Dog class allows instantiation of multiple types of dog
    """
    cute = True
    sound = "woof!"
    energy = 100

    def __init__(self, height, weight, food):
        """Set attributes for your dog"""
        self.height = height
        self.weight = weight
        self.food = food

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

    def eat(self, amount_g=25):
        """Watch dog eat"""
        if self.food == "dry":
            energy_gained = 1 * amount
        elif self.food == "wet":
            energy_gained == 2 * amount
        else:
            print("Dog can't eat that, it threw up")
            energy_gained = -1 * amount

        self.energy += energy_gained

    @classmethod
    def bark(cls):
        print(cls.sound)


if __name__ == "__main__":
    spot = Dog(height=5, weight=20, food="dry")
    spot.run(distance=5)
    spot.eat(amount=10)
    spot.play()
    spot.bark()

    breakpoint()

    print(spot.energy)
        
        
