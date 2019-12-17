import re
import copy

input = """
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
"""

class Reaction:
    def __init__(self, reaction_string):
        self.reaction_string = reaction_string
        self.build_reaction()

    def build_reaction(self):
        reactant_string, product_string = re.split("=>", self.reaction_string)
        self.reactants = self.extract_reaction_half(reactant_string)
        self.products = self.extract_reaction_half(product_string)

    def extract_reaction_half(self, reaction_half):
        constituents = []

        # split by ','
        parts = list(map(lambda x: x.strip(), re.split(',', reaction_half)))
        for part in parts:
            constituents.append(self.build_constituents(part))
        return constituents

    def build_constituents(self, constituent):
        # '10 ORE'
        element = re.findall('\d ([a-zA-Z]*)', constituent)[0]
        amount = ''.join(re.findall('(\d)', constituent))
        return { 'element': element, 'amount': int(amount) }


class Reactor:
    def __init__(self, reaction_map):
        self.reaction_map = reaction_map
        self.reactions = []
        self.build_reaction_library()

    def build_reaction_library(self):
        search_results = re.findall("(.*)\n", self.reaction_map)
        reaction_strings = list(filter(lambda x: x.__ne__(''), search_results))
        for reaction_string in reaction_strings:
            self.reactions.append(Reaction(reaction_string))

    def calculate_input_ore(self):
        fuel_producing_reaction = next(reaction for reaction in self.reactions if reaction.products[0]['element'] == 'FUEL')
        self.ore_sourced_reactions = [reaction for reaction in self.reactions if reaction.reactants[0]['element'] == 'ORE']
        self.ore_sourced_elements = list(map(lambda x: x.products[0]['element'], self.ore_sourced_reactions))

        self.constituents = fuel_producing_reaction.reactants
        # Refine until finding all constituents that are directly sourced from fuel
        while True:
            new_constituents = []
            for constituent in self.constituents:
                new_constituents += self.constituents_of(constituent)

            self.constituents = copy.deepcopy(new_constituents)
            self.combine_like_constituents()

            if self.no_non_ore_sourced_constituents():
                break

        return self.ore_to_produce_ore_based_constituents()

    def no_non_ore_sourced_constituents(self):
        non_ore_sourced_constituents = [constituent for constituent in self.constituents if
                                        constituent['element'] not in self.ore_sourced_elements]
        return non_ore_sourced_constituents.__len__() == 0

    def combine_like_constituents(self):
        # combine all constituents w/ the same element and sum amounts
        combined_constituents = []
        for constituent in self.constituents:
            # matching_constituent = next(ifilter(lambda x: , combined_constituents), None)

        print('here')

    def ore_to_produce_ore_based_constituents(self):
        # combine_like_constituents

        ore = 0
        # for constituent in self.constituents:
        #     ore += self.constituents_of(constituent)


    def constituents_of(self, constituent):
        amount = constituent['amount']
        element = constituent['element']

        if element in self.ore_sourced_elements:
            return [constituent]

        reaction_producing_element = copy.deepcopy(next(reaction for reaction in self.reactions if reaction.products[0]['element'] == element))

        times_to_run_reaction = 1
        while True:
            if reaction_producing_element.products[0]['amount'] * times_to_run_reaction >= amount:
                break
            times_to_run_reaction += 1

        constituents = []
        for reactant in reaction_producing_element.reactants:
            constituents += [dict(reactant, amount = (reactant['amount'] * times_to_run_reaction))]
        return constituents


reactor = Reactor(input)
reactor
print(reactor.calculate_input_ore())