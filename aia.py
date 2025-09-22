from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup

@dataclass
class Property:
    name: str
    uri: str
    cardinality: str
    datatype: str


class AiaEnhancer:
    def __init__(self, properties: List[Property]):
        pass

    def add_property(self, object_: BeautifulSoup, spec_name: str, property: Property):
        u"""Add property to object"""
        pass

    def check_single_property(self, object_: BeautifulSoup, property: Property):
        u"""Check if object has property"""
        specifications = object_.find_all('specification')
        modified_specifications = []

        # Loop over all specification tags
        for specification in specifications:
            name = specification['name']
            id = specification['identifier']

            obj_properties = object_.find_all('property')
            prop_uri = property.uri

            # loop over individual properties
            found_property = False
            for property in obj_properties:
                if property["uri"] == prop_uri:
                    found_property = True

            # Track lacking specifications for adding properties and user feedback
            if not found_property:
                modified_specifications.append(name)

        return modified_specifications

    def check_properties(self, object_: BeautifulSoup, properties: List[Property]):
        u"""Check if all needed properties in object"""
        for property in properties:
            if not self.check_single_property(object_, property):
                self.add_property(object_, property)


if __name__ == "__main__":
    with open("/Users/felix/Arbeit/hackathon/ids-template-dach.ids", "r") as f:
        _object = BeautifulSoup(f.read(), "xml")

    prop_is_true = Property(
        "isTrue",
        "https://via.bund.de/bim/merkmale/details/property/9ea5f0fd-0893-4548-a0b4-4a938da6988c?type=PROPERTY",
        "required",
        "IFCLABEL"
    )
    prob_is_false = Property(
        "isFalse",
        "none",
        "required",
        "IFCLABEL"
    )
    enhancer = AiaEnhancer([prob_is_false, prop_is_true])

    assert enhancer.check_property(_object, prob_is_false) == False
    assert enhancer.check_property(_object, prop_is_true) == True
