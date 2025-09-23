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
        self.property_dummy = '''<property
                    uri=\"\"
                    cardinality=\"\" dataType=\"\">
                    <propertySet>
                        <simpleValue></simpleValue>
                    </propertySet>
                    <baseName>
                        <simpleValue></simpleValue>
                    </baseName>
                </property>'''

    def add_single_property(self, object_: BeautifulSoup, spec_name: str, spec_id: str, property_: Property):
        u"""Add property to object"""
        specification = object_.find(identifier=spec_id)

        requirements = specification.find("requirements")
        # create property from template and fill attributes
        new_property = BeautifulSoup(self.property_dummy, "xml")
        new_property.property["uri"] = property_.uri
        new_property.property["cardinality"] = property_.cardinality
        new_property.property["dataType"] = property_.datatype
        new_property.find("propertySet").find("simpleValue").string = spec_name
        new_property.find("baseName").find("simpleValue").string = property_.name
        requirements.append(new_property)


    def check_single_property(self, object_: BeautifulSoup, property_: Property) -> list[tuple[str, str]]:
        u"""Check if object has property

        Returns list of (name, id) tuples
        """
        specifications = object_.find_all('specification')
        modified_specifications = []

        # Loop over all specification tags
        for specification in specifications:
            name = specification['name']
            id = specification['identifier']

            obj_properties = object_.find_all('property')
            prop_uri = property_.uri

            # loop over individual properties
            found_property = False
            for property_ in obj_properties:
                if property_["uri"] == prop_uri:
                    found_property = True

            # Track lacking specifications for adding properties and user feedback
            if not found_property:
                modified_specifications.append((name, id))

        return modified_specifications

    def check_and_add_properties(self, object_: str, properties: List[Property]):
        u"""Check if all needed properties in object"""
        object_ = BeautifulSoup(object_, "xml")

        for property_ in properties:
            modified_specifications = self.check_single_property(object_, property_)
            if not len(modified_specifications) == 0:
                for spec_name, spec_id in modified_specifications:
                    print(f"Modified specification: {spec_name}@{spec_id}")
                    self.add_single_property(object_, spec_name, spec_id, property_)

        return True


if __name__ == "__main__":
    with open("/Users/felix/Arbeit/hackathon/ids-template-dummy.ids", "r") as f:
        object_ = BeautifulSoup(f.read(), "xml")

    prop_is_true = Property(
        "isTrue",
        "https://via.bund.de/bim/merkmale/details/property/9ea5f0fd-0893-4548-a0b4-4a938da6988c?type=PROPERTY",
        "required",
        "IFCLABEL"
    )
    prop_is_false = Property(
        "isFalse",
        "none",
        "required",
        "IFCLABEL"
    )
    enhancer = AiaEnhancer([prop_is_false, prop_is_true])

    assert len(enhancer.check_single_property(object_, prop_is_false)) > 0
    assert len(enhancer.check_single_property(object_, prop_is_true)) == 0

    assert enhancer.check_and_add_properties(object_, [prop_is_false, prop_is_true])
