class Process:

    def __init__(self):
        pass

    # """ Get the data of each season """
    # def get_season(self, dictionary):

    #     seasons = list(dictionary["room_rates"].keys())
    #     dictionary_season = []

    #     for season in seasons:
    #         dictionary_season.append(dictionary["room_rates"][season])

    #     return dictionary_season
    
    # """ Turn the room rates into one dictionary that contains the room and its respective season rates """
    # def transform_season(self, data):

    #     """Data comes in high season, mid season, low season"""
    #     rates = {}
    #     for dictionary in data:
    #         rates_per_dictionary = {}
    #         if "rates_per_person_per_night" in dictionary:
    #             temp_rates = dictionary["rates_per_person_per_night"]
    #             for key in temp_rates:
    #                 num = self.room_name(key)

    #                 """ If we can't find the capacity of the room, just make num equal to 1 """
    #                 if num == "Manually Check Source":
    #                     num = 1

    #                 """ Multiply per person price by capacity """
    #                 if isinstance(temp_rates[key], int) or isinstance(temp_rates[key], float):
    #                     temp_rates[key] = temp_rates[key] * num

    #             rates_per_dictionary.update(temp_rates)
    #         if "rates_per_unit_per_night" in dictionary:
    #             rates_per_dictionary.update(dictionary["rates_per_unit_per_night"])
    #         if len(rates) == 0:
    #             for key in rates_per_dictionary:
    #                 rates[key] = [rates_per_dictionary[key]]
    #         else:
    #             for key in rates_per_dictionary:
    #                 rates[key].append(rates_per_dictionary[key])

    #     return rates
    
    # """Return the conservstion fee of our safari camp"""
    # def find_conservation_fee(self, dictionary):
    #     if 'conservation_fees' in dictionary:
            
    #         if len(dictionary['conservation_fees']) > 0:
    #             conservation_fee = dictionary['conservation_fees']
    #             if 'adult_per_person_per_night' in conservation_fee and isinstance(conservation_fee['adult_per_person_per_night'], int):
    #                 return conservation_fee['adult_per_person_per_night']
    #             else:
    #                 return "Please manually check source: Likely deals with specific seasonal fees or park fees that cannot be parsed"
    #         else:
    #             return "Manually Check the Source"
    #     else:
    #             return "Manually Check the Source"


    """ Find the capacity of a certain type of room - honeymoon, single, double, triple - so we know what 
    to multiply the price per person by. We do not care about unit prices as they do not apply in this case """
    def room_name(self, room_type: str):
        room_type = room_type.lower()
        if room_type.find('honeymoon') != -1:
            return 2
        elif room_type.find('single') != -1:
            return 1
        elif room_type.find('double') != -1:
            return 2
        elif room_type.find('triple') != -1:
            return 3
        else:
            return 1

    def find_capacity(self, room_type: str):

        for i in range(1, 10):
            if room_type.find(str(i)) != -1:
                return i
        return "Manually Check Source"
        
    