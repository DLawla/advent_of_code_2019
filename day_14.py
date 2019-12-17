import re
import copy

input = """
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
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

        # initialize the constituents, these will be refined down into respective reactants
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

    def ore_to_produce_ore_based_constituents(self):
        ore = 0
        for constituent in self.constituents:
            matching_ore_reaction = next(reaction for reaction in self.ore_sourced_reactions if reaction.products[0]['element'] == constituent['element'])
            times_to_run_reaction = self.times_to_run_reaction(matching_ore_reaction, constituent['amount'])
            ore += matching_ore_reaction.reactants[0]['amount'] * times_to_run_reaction
        return ore

    def constituents_of(self, constituent):
        amount = constituent['amount']
        element = constituent['element']

        if element in self.ore_sourced_elements:
            return [constituent]

        reaction_producing_element = copy.deepcopy(next(reaction for reaction in self.reactions if reaction.products[0]['element'] == element))

        times_to_run_reaction = self.times_to_run_reaction(reaction_producing_element, amount)

        constituents = []
        for reactant in reaction_producing_element.reactants:
            constituents += [dict(reactant, amount = (reactant['amount'] * times_to_run_reaction))]
        return constituents

    def combine_like_constituents(self):
        unique_elemements = set(list(map(lambda x: x['element'], self.constituents)))
        combined_constituents = []
        for unique_elemement in unique_elemements:
            matching_constituent_amounts = [constituent['amount'] for constituent in self.constituents if
                                            constituent['element'] == unique_elemement]
            total_element_count = sum(matching_constituent_amounts)
            combined_constituents.append({'element': unique_elemement, 'amount': total_element_count})
        self.constituents = combined_constituents

    def no_non_ore_sourced_constituents(self):
        non_ore_sourced_constituents = [constituent for constituent in self.constituents if
                                        constituent['element'] not in self.ore_sourced_elements]
        return non_ore_sourced_constituents.__len__() == 0

    def times_to_run_reaction(self, reaction, desired_amount):
        times_to_run_reaction = 1
        while True:
            if reaction.products[0]['amount'] * times_to_run_reaction >= desired_amount:
                break
            times_to_run_reaction += 1
        return times_to_run_reaction


reactor = Reactor(input)
reactor
print(reactor.calculate_input_ore())