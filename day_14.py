import re
import copy

input = """
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
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
        self.build_distance_lookup()

    def build_distance_lookup(self):
        self.distance = {'ORE': 0}

        while len(self.distance) < len(self.reactions):
            for reaction in self.reactions:
                material = reaction.products[0]['element']
                if material in self.distance:
                    continue
                if not all([i in self.distance for i in list(map(lambda x: x['element'], reaction.reactants))]):
                    continue
                all_reactant_elements = list(map(lambda x: x['element'], reaction.reactants))
                self.distance[material] = max([self.distance[i] for i in all_reactant_elements]) + 1

    def build_reaction_library(self):
        search_results = re.findall("(.*)\n", self.reaction_map)
        reaction_strings = list(filter(lambda x: x.__ne__(''), search_results))
        for reaction_string in reaction_strings:
            self.reactions.append(Reaction(reaction_string))

    def calculate_max_fuel(self, ore_target):
        one_unit = self.calculate_input_ore(1)
        target = ore_target // one_unit
        used_ore = self.calculate_input_ore(target)
        while True:
            target += (ore_target - used_ore) // one_unit + 1
            used_ore = self.calculate_input_ore(target)
            if used_ore > ore_target:
                break
        return target - 1

    def calculate_input_ore(self, amount_of_fuel):
        fuel_producing_reaction = next(reaction for reaction in self.reactions if reaction.products[0]['element'] == 'FUEL')
        times_to_run_fuel_reaction = self.times_to_run_reaction(fuel_producing_reaction, amount_of_fuel)
        self.ore_sourced_reactions = [reaction for reaction in self.reactions if reaction.reactants[0]['element'] == 'ORE']
        self.ore_sourced_elements = list(map(lambda x: x.products[0]['element'], self.ore_sourced_reactions))

        # initialize the constituents, these will be refined down into respective reactants
        scaled_fuel_producing_constituents = list(map(lambda x: {'element': x['element'], 'amount': x['amount'] * times_to_run_fuel_reaction}, copy.deepcopy(fuel_producing_reaction.reactants)))
        self.constituents = scaled_fuel_producing_constituents

        # Refine until finding all constituents that are directly sourced from fuel
        while True:
            new_constituents = []

            constituent_elements = list(map(lambda x: x['element'], self.constituents))
            constituent_element_to_extract = max(constituent_elements, key=lambda x: self.distance[x])
            constituent_to_extract = next(constituent for constituent in self.constituents if constituent['element'] == constituent_element_to_extract)
            del self.constituents[self.constituents.index(constituent_to_extract)]
            self.constituents += self.constituents_of(constituent_to_extract)
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

        reaction_producing_element = self.reaction_producting_element(element)

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

    def reaction_producting_element(self, element):
        reaction = copy.deepcopy(
            next(reaction for reaction in self.reactions if reaction.products[0]['element'] == element)
        )
        return reaction

reactor = Reactor(input)
reactor
print(reactor.calculate_input_ore(1))
print(reactor.calculate_max_fuel(1000000000000))