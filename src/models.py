from dataclasses import dataclass, asdict
from typing import List
from exceptions import *
import json

"""
TODO:  This should be split into two, one for IPv4 and one for IPv6.
    There should be one dataclass that contains both of these so that you can reference it as spoofing_result.ipv4.privatespoof and spoofing_result.ipv6.privatespoof
    This will make it easier to access the data
"""

@dataclass
class spoofer_result_base:
    session: int
    country: str
    timestamp: str
    asn: int
    client: str
    nat: bool
    privatespoof: str
    routedspoof: str

    def as_dict(self):
        return asdict(self)
    
@dataclass
class spoofer_ipv4_result(spoofer_result_base):
    version: str = "IPv4"

@dataclass
class spoofer_ipv6_result(spoofer_result_base):
    version: str = "IPv6"
    

@dataclass
class spoofing_result:
    """ This class is a dataclass that contains the results of the spoofing API call """
    ipv4: spoofer_ipv4_result
    ipv6: spoofer_ipv6_result


    def get_ipv4(self) -> spoofer_ipv4_result:
        return self.ipv4
    
    def get_ipv6(self) -> spoofer_ipv6_result:
        return self.ipv6
    
    def get_as_csv(self) -> str:
        """ This function returns the spoofing result as a CSV string """
        return f"{self.ipv4.version},{self.ipv4.session},{self.ipv4.country},{self.ipv4.timestamp},{self.ipv4.asn},{self.ipv4.client},{self.ipv4.nat},{self.ipv4.privatespoof},{self.ipv4.routedspoof}\n{self.ipv6.version},{self.ipv6.session},{self.ipv6.country},{self.ipv6.timestamp},{self.ipv6.asn},{self.ipv6.client},{self.ipv6.nat},{self.ipv6.privatespoof},{self.ipv6.routedspoof}\n"
    
    def get_ipv4_as_csv(self) -> str:
        """ This function returns the IPv4 spoofing result as a CSV string """
        return f"{self.ipv4.version},{self.ipv4.session},{self.ipv4.country},{self.ipv4.timestamp},{self.ipv4.asn},{self.ipv4.client},{self.ipv4.nat},{self.ipv4.privatespoof},{self.ipv4.routedspoof}\n"
    
    def get_ipv6_as_csv(self) -> str:
        """ This function returns the IPv6 spoofing result as a CSV string """
        return f"{self.ipv6.version},{self.ipv6.session},{self.ipv6.country},{self.ipv6.timestamp},{self.ipv6.asn},{self.ipv6.client},{self.ipv6.nat},{self.ipv6.privatespoof},{self.ipv6.routedspoof}\n"

    def get_as_json(self) -> str:
        """ This function returns the spoofing result as a JSON string """
        return json.dumps(asdict(self))


@dataclass
class all_spoofing_results():
    """" This class is a dataclass that contains a list of spoofing_results """
    _results: List[spoofing_result]

    @staticmethod
    def get_header_csv() -> str:
        """" This function returns the header for the CSV file """
        return "version,session,country,timestamp,asn,client,nat,privatespoof,routedspoof\n"

    def add_result(self, result: spoofing_result) -> None:
        """" This function adds a spoofing result to the list of results """
        self._results.append(result)

    def write_csv(self, filename) -> None:
        """" This function writes the results to a CSV file """
        with open(filename, "w") as file:
            file.write(self.get_header_csv())
            for result in self._results:
                file.write(result.get_as_csv())

    def write_json(self, filename) -> None:
        """" This function writes the results to a JSON file """
        with open(filename, "w") as file:
            json.dump([asdict(r) for r in self._results], file)