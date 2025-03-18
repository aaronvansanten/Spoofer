import os
from dataclasses import asdict
from datetime import date

from models import *
from APIHandler import *


class Spoofer:
    """ This class is an implementation of the spoofer API. It contains functions to make API calls to the spoofer API. """

    def __init__(self):
        self.__API_handler = SpooferAPIHandler()
        self._base_dir = "../Data/"

    def _parse_api_response(self, response: dict) -> spoofing_result:
        """
        This function parses the response from the API call and returns a spoofing_result object.

        :param response: The response from the API call
        :return: The spoofing_result object
        """

        ipv4_result: spoofer_ipv4_result = spoofer_ipv4_result(
            session=response.get("session"),
            country=response.get("country"),
            timestamp=response.get("timestamp"),
            asn=response.get("asn4"),
            client=response.get("client4"),
            nat=response.get("nat4"),
            privatespoof=response.get("privatespoof"),
            routedspoof=response.get("routedspoof")
        )

        ipv6_result: spoofer_ipv6_result = spoofer_ipv6_result(
            session=response.get("session"),
            country=response.get("country"),
            timestamp=response.get("timestamp"),
            asn=response.get("asn6"),
            client=response.get("client6"),
            nat=response.get("nat6"),
            privatespoof=response.get("privatespoof6"),
            routedspoof=response.get("routedspoof6")
        )

        return spoofing_result(ipv4=ipv4_result, ipv6=ipv6_result)

    def write_collection_API_Call(self, file_name: str, write_as_csv: bool = False, items_per_page: str = 5, asn: str = "", date_before: str = "", date_after: str = date.today(), date_strict_before: str = "", date_strict_after: str = "") -> None:
        """
        This function makes the collection API call to the spoofer API and writes the results to a file. It takes the arguments and constructs the URL to make the call.
        The base directory of this file is the directory of the file form which the spoofer object is initialized.
        By default, the results are written to a JSON file. If you want to write the results to a CSV file, set the write_as_csv parameter to True.

        :param file_name: The name of the file to write the results to. Extension is added automatically based on the file type
        :param write_as_csv: A boolean value to determine if the results should be written to a CSV file
        :param items_per_page: The number of items to return per page
        :param asn: The ASN to filter the results by
        :param date_before: The date to filter the results before
        :param date_after: The date to filter the results after. Default value is today to only get recent results
        :param date_strict_before: The date to filter the results before strictly
        :param date_strict_after: The date to filter the results after strictly
        """
        response = self.__API_handler.fetch_Collection(
            items_per_page, asn, date_before, date_after, date_strict_before, date_strict_after)

        parsed_response = response.get("hydra:member")
        all_results = all_spoofing_results([])
        for result in parsed_response:
            all_results.add_result(self._parse_api_response(result))

        if write_as_csv:
            all_results.write_csv(os.path.join(
                self._base_dir, f"{file_name}.csv"))
        else:
            all_results.write_json(os.path.join(
                self._base_dir, f"{file_name}.json"))

    def obtain_spoofed_possibilities(self, id: str, version: int = 0) -> dict:
        """
        This function returns the spoofed possibilities for the address in the session.

        :param id: The ID of the session you want to query
        :param version: The IP version of the address you want to query. If left empty, it will return both IPv4 and IPv6 addresses
        :return: The spoofed possibilities for the address in the specified session
        """
        response = self._parse_api_response(self.__API_handler.fetch_session(id))
        if version == 4:
            return response.ipv4.as_dict()
        elif version == 6:
            return response.ipv6.as_dict()
        else:
            return asdict(response)

    def obtain_spoofed_possibilites_ipv4(self, id: str) -> dict:
        """
        This function returns the spoofed possibilities for the IPv4 address in the session from the spoofer API.

        :param id: The ID of the session you want to query
        :return: The spoofed possibilities for the IPv4 address in the specified session
        """
        return self.obtain_spoofed_possibilities(id, 4)

    def obtain_spoofed_possibilites_ipv6(self, id: str) -> dict:
        """
        This function returns the spoofed possibilities for the IPv6 address in the session from the spoofer API.

        :param id: The ID of the session you want to query
        :return: The spoofed possibilities for the IPv6 address in the specified session
        """
        return self.obtain_spoofed_possibilities(id, 6)
