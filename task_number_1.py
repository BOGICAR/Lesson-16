import argparse
import csv
from re import search


class CheckDataAirport:
    def __init__(self, iata_code=None, country=None, name=None):
        self.airport_data = self.load_airport_data()
        self.iata_code = iata_code
        self.country = country
        self.name = name

    def load_airport_data(self):
        with open('airport-codes_csv.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            airport_info = []
            for i in csv_reader:
                airport_info.append(i)
            return airport_info

    def check_iata_code(self):
        for line in self.airport_data:
            if line['iata_code'].lower() == self.iata_code.upper():
                return line
        raise AirportNotFoundError

    def check_country(self):
        airports = []
        for line in self.airport_data:
            if line['iso_country'].lower() == self.country.lower():
                airports.append(line)
                return airports
        if not airports:
            raise AirportNotFoundError

    def check_name(self):
        airports = []
        for line in self.airport_data:
            if line['name'] in self.name.lower():
                airports.append(line)
                return airports
        if not airports:
            raise AirportNotFoundError


def check_args():
    if len([row for row in vars(args).values() if row is not None]) > 1:
        raise MultipleOptionsError(message='Should be only one parameter')
    if not len([row for row in vars(args).values() if row is not None]):
        raise NoOptionsFoundError(message='Parameters not found')
    if args.iata_code:
        check_validation(args.iata_code)


def check_validation(iata_code):
    if search(r'[a-z\d]', iata_code) and iata_code != 3:
        raise IATACodeError(iata_code)
    else:
        return iata_code


class BaseAirportError(Exception):
    def __init__(self, iata_code: str, message="Airport not found"):
        self.iata_code = iata_code
        self.message = f"{self.iata_code} - {message}"
        super().__init__(self.message)


class AirportNotFoundError(BaseAirportError):
    pass


class CountryNotFoundError(BaseAirportError):
    pass


class IATACodeError(BaseAirportError):
    pass


class MultipleOptionsError(Exception):
    pass


class NoOptionsFoundError(Exception):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Checking airport information')
    parser.add_argument('--iata_code')
    parser.add_argument('--country')
    parser.add_argument('--name')
    args = parser.parse_args()
    check_args()
    fist_try = CheckDataAirport(name=args.name, country=args.country, iata_code=args.iata_code) # **vars(args)
