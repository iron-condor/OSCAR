"""Module that contains a class for storing contacts and contact data"""
from datetime import datetime

class Contact:
    """Manages contacts for use in texting, emailing, and general forms of contacting people"""

    def __init__(self, first_name=None, last_name=None, phone_numbers=[], emails=[], addresses=[], contact_groups=[],
     nicknames=[], notes="", birthday=None, languages=[], organizations=[], photo=None, website=None, vcf_dict=None):
        """Constructor for the Contact object

        Arguments
        ---------
        first_name : String (optional)
            The contact's first name
        last_name : String (optional)
            The contact's last name
        phone_numbers : list[string] (optional)
            A list of phone numbers associated with the contact
        emails : list[string] (optional)
            A list of emails associated with the contact
        addresses : list[string] (optional)
            A list of addresses associated with the contact
        contact_groups : list[string] (optional)
            A list of contact groups associated with the contact
            Ex: Friends, Family, ICE
        nicknames : list[string] (optional)
            A list of nicknames that are associated with the contact
            Ex: Nate, Mike
        notes : String (optional)
            A string containing any notes that the user has stored for the contact
        birthday : datetime (optional)
            A datetime object representing the contact's birthday
        languages : list[string] (optional)
            A list of languages understood/spoken by the contact
        organizations : list[string] (optional)
            A list of organizations with which the contact is affiliated
        photo : * (optional)
            A photo associated with the contact. Data type undecided as of this update
        website : * (optional)
            A URL to a website associated with the contact. Data type undecided as of this update
        vcf_dict : dictionary[string] (optional)
            A dictionary from a VCF file containing info about the contact.
            Usually received from the add_contact.py file
        """
        if vcf_dict is None:
            self.first_name = first_name
            self.last_name = last_name
            self.phone_numbers = phone_numbers
            self.emails = emails
            self.addresses = addresses
            self.contact_groups = contact_groups
            self.notes = notes
            self.birthday = birthday
            self.languages = []
            self.organizations = []
            self.photo = photo
            self.website = website
        else:
            self.first_name = None
            self.last_name = None
            self.phone_numbers = []
            self.emails = []
            self.addresses = []
            self.contact_groups = []
            self.notes = ""
            self.birthday = None
            self.languages = []
            self.organizations = []
            self.photo = None
            self.website = None

            for key in vcf_dict:
                if key == "fn":
                    self.first_name = vcf_dict["fn"].split(" ")[0]
                    if len(vcf_dict["fn"].split(" ")) > 1:
                        self.last_name = vcf_dict["fn"].split(" ")[-1]
                elif key == "tel":
                    self.phone_numbers.append(vcf_dict["tel"])
                elif key == "adr":
                    if ">" not in vcf_dict["adr"]:
                        self.addresses.append(vcf_dict["adr"])
                    else:
                        address_list = vcf_dict["adr"].split(">")
                        address_list = [addr.replace(", <ADR{}", "") for addr in address_list]
                        self.addresses = address_list
                elif key == "email":
                    if "," not in vcf_dict["email"]:
                        self.emails.append(vcf_dict["email"])
                    else:
                        self.emails = self.split_and_trim(key, vcf_dict["email"])
                elif key == "note":
                    self.note = vcf_dict["note"]
                elif key == "bday":
                    self.birthday = datetime.strptime(vcf_dict["bday"], "%Y-%m-%d")
                elif key == "org":
                    if "title" in vcf_dict:
                        self.organizations.append([vcf_dict["org"].replace("['", "").replace("']", ""), vcf_dict["title"]])
                    else:
                        self.organizations.append([vcf_dict["org"].replace("['", "").replace("']", "")])
                elif key == "url":
                    self.website = vcf_dict["url"]

    def split_and_trim(self, key, string) -> list:
        """Method that trims formatting from VCF dicts and returns delimited data as a list

        Arguments
        ---------
        key : String
            The key from the dictionary that is associated with the string to be parsed
        string : String
            The string from the dictionary that is to be split and trimmed

        Returns
        -------
        list[string]
            A list containing the data in the string
        """
        return string.replace("<" + key.upper() + "{}", "").replace(">", "").split(", ")
