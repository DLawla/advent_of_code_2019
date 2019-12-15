import copy

class System:
    def __init__(self):
        self.moons = [
            Moon([-13, 14, -7]),
            Moon([-18, 9, 0]),
            Moon([0, -3, -3]),
            Moon([-15, 3, -13])
        ]
        self.initial_state = self.get_state()

    def step(self):
        self.apply_gravity()
        self.apply_velocity()

    def get_state(self):
        return [moon.coordinates.__str__() + moon.velocity.__str__() for moon in self.moons]

    def apply_gravity(self):
        for i, moon in enumerate(self.moons):
            for j, other_moon in enumerate(self.moons):
                if i == j:
                    continue
                for position_index, position in enumerate(moon.coordinates):
                    if other_moon.coordinates[position_index] > moon.coordinates[position_index]:
                        moon.velocity[position_index] += 1
                    elif other_moon.coordinates[position_index] < moon.coordinates[position_index]:
                        moon.velocity[position_index] -= 1

    def apply_velocity(self):
        for moon in self.moons:
            moon.coordinates = [sum(x) for x in zip(moon.coordinates, moon.velocity)]

    def energy(self):
        total_energy = 0

        for moon in self.moons:
            potential_energy = sum([abs(x) for x in moon.coordinates])
            kinetic_energy = sum([abs(x) for x in moon.velocity])
            total_energy += (potential_energy * kinetic_energy)

        return total_energy

class Moon:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.velocity = [0, 0, 0]

class OptimizedSystem:
    def __init__(self):
        self.x = [[-13, -18, 0, -15], [0, 0, 0, 0]]
        self.y = [[14, 9, -3, 3], [0, 0, 0, 0]]
        self.z = [[-7, 0, -3, -13], [0, 0, 0, 0]]
        self.x_i = copy.deepcopy(self.x)
        self.y_i = copy.deepcopy(self.y)
        self.z_i = copy.deepcopy(self.z)
        self.repeat_x = None
        self.repeat_y = None
        self.repeat_z = None
        self.step_count = 0

    def step(self):
        if not self.repeat_x:
            self.apply_gravity(self.x)
        if not self.repeat_y:
            self.apply_gravity(self.y)
        if not self.repeat_z:
            self.apply_gravity(self.z)
        if not self.repeat_x:
            self.apply_velocity(self.x)
        if not self.repeat_y:
            self.apply_velocity(self.y)
        if not self.repeat_z:
            self.apply_velocity(self.z)

        self.step_count += 1
        self.check_for_repeats()

    def apply_gravity(self, axis_coordinates):
        coordinates = axis_coordinates[0]
        velocities = axis_coordinates[1]

        for i, coordinate in enumerate(coordinates):
            for j, other_coordinate in enumerate(coordinates):
                if i == j:
                    continue

                if other_coordinate > coordinate:
                    velocities[i] += 1
                elif other_coordinate < coordinate:
                    velocities[i] -= 1

    def apply_velocity(self, axis_coordinates):
        coordinates = axis_coordinates[0]
        velocities = axis_coordinates[1]

        axis_coordinates[0] = [sum(x) for x in zip(coordinates, velocities)]

    def check_for_repeats(self):
        if self.x == self.x_i and not self.repeat_x:
            self.repeat_x = self.step_count
        if self.y == self.y_i and not self.repeat_y:
            self.repeat_y = self.step_count
        if self.z == self.z_i and not self.repeat_z:
            self.repeat_z = self.step_count

# Challenge 1
# system = OptimizedSystem()
# for i in range(1000):
#     system.step()
# print(system.energy())
# answer: 7138

# Challenge 2
system = OptimizedSystem()
i = 0
while True:
    system.step()
    if system.repeat_x:
        print(f'x: {system.repeat_x}')
    if system.repeat_y:
        print(f'y: {system.repeat_y}')
    if system.repeat_z:
        print(f'z: {system.repeat_z}')
    if system.repeat_x and system.repeat_y and system.repeat_z:
        lowest = system.repeat_x * system.repeat_y * system.repeat_z
        print(lowest)
        break
    if i % 100_000 == 0:
        print(i)
    i += 1

from math import gcd

a = [system.repeat_x, system.repeat_y, system.repeat_z]
lcm = a[0]
for i in a[1:]:
  lcm = int(lcm*i/gcd(lcm, i))
print(lcm)