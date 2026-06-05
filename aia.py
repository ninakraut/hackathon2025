from dataclasses import dataclass
from typing import List
from copy import copy

from bs4 import BeautifulSoup, Tag


class AiaEnhancer:
    def __init__(self):
        self.property_dummy = BeautifulSoup('''<property
                    uri=\"\"
                    cardinality=\"required\" dataType=\"IFCLABEL\">
                    <propertySet>
                        <simpleValue></simpleValue>
                    </propertySet>
                    <baseName>
                        <simpleValue></simpleValue>
                    </baseName>
                </property>''',
                                            'xml'
                                            )

    def add_single_property(self, object_: BeautifulSoup, spec_name: str, spec_id: str, property_: Tag):
        u"""Add property to object"""
        specification = object_.find(identifier=spec_id)

        requirements = specification.find("requirements")
        # create property from template and fill attributes
        new_property = copy(self.property_dummy)
        new_property.property["uri"] = create_bim_portal_uri_from_guid(property_.find('guid').string)
        new_property.find("propertySet").simpleValue.string = spec_name
        new_property.find("baseName").simpleValue.string = property_.namesInLanguage.find('name').string
        requirements.append(new_property)


    def check_single_property(self, object_: BeautifulSoup, property_: Tag) -> list[tuple[str, str]]:
        u"""Checks if object has a given property and returns list of (name, id) tuples.

        Parameters:
            `object_`: BeautifulSoup object representing an EIR (AIA)

            `property_`: bs4.Tag object representing a BIM property

        Returns:
            `modified_specifications`: list of (name, id) tuples
        """
        specifications = object_.find_all('specification')
        modified_specifications = []

        # Loop over all specification tags
        for specification in specifications:
            name = specification['name']
            id = specification['identifier']

            obj_properties = object_.find_all('property')

            # Properties complying with ISO 23386 only have GUID
            # URI is probably BIM portal specific so this would need a case distinction for BIM portal or other data
            prop_guid = property_.find('guid').string
            # Build dummy BIM portal URI from guid
            prop_uri = create_bim_portal_uri_from_guid(prop_guid)

            # loop over individual properties
            found_property = False
            for obj_p in obj_properties:
                if obj_p["uri"] == prop_uri:
                    found_property = True

            # Track lacking specifications for adding properties and user feedback
            if not found_property:
                modified_specifications.append((name, id))

        return modified_specifications

    def check_and_add_properties(self, object_: BeautifulSoup, properties: List[Tag]):
        u"""Check if all needed properties in object and add missing properties."""

        for prop in properties:
            modified_specifications = self.check_single_property(object_, prop)
            if not len(modified_specifications) == 0:
                for spec_name, spec_id in modified_specifications:
                    print(f"Modified specification: {spec_name}@{spec_id}")
                    self.add_single_property(object_, spec_name, spec_id, prop)

        return str(object_)


def create_bim_portal_uri_from_guid(guid: str) -> str:
    u"""Create a dummy BIM portal URI from property GUID."""

    return f"https://via.bund.de/bim/merkmale/details/property/{guid}?type=PROPERTY"


if __name__ == "__main__":
    with open("/Users/felix/Arbeit/hackathon/ids-template-dummy.ids", "r") as f:
        eir = BeautifulSoup(f.read(), "xml")

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
    enhancer = AiaEnhancer()

    assert len(enhancer.check_single_property(eir, prop_is_false)) > 0
    assert len(enhancer.check_single_property(eir, prop_is_true)) == 0

    assert enhancer.check_and_add_properties(eir, [prop_is_false, prop_is_true])
