import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

from exceptions import *


class SpooferAPIHandler:
    def __init__(self):
        self.base_url = 'https://api.spoofer.caida.org/sessions'

    def __construct_optional_params(self, asn, time_before, time_strict_before, time_after, time_strict_after) -> dict:
        """
        This function constructs a dictionary from the parameters that are passed in. It returns the dictionary.

        :param asn: The number of the AS you want to query
        :param time_before: The date you want to query before
        :param time_after: The date you want to query after
        :param time_strict_before: The date you want to query strictly before
        :param time_strict_after: The date you want to query strictly after
        :return: The dictionary of the parameters
        """
        return {
            "asn": asn,
            "timestamp%5Bbefore%5D": time_before,
            "timestamp%5Bstrictly_before%5D": time_strict_before,
            "timestamp%5Bafter%5D": time_after,
            "timestamp%5Bstrictly_after%5Dn": time_strict_after
        }

    def __construct_collection_url(self, items_per_page: str, optional_collection_arguments: dict) -> str:
        """
        This function constructs the URL for the collection API call. It takes the arguments and creates the correctly formatted string.

        :param items_per_page: The number of items per page you want to query
        :param date_before: The date you want to query before
        :param date_after: The date you want to query after
        :param date_strict_before: The date you want to query strictly before
        :param date_strict_after: The date you want to query strictly after
        :param asn: The number of the AS you want to query
        :return: The constructed API url
        """
        query = ''
        for key, value in optional_collection_arguments.items():
            if value:
                query += f"&{key}={value}"


        API_url = f"{self.base_url}?itemsPerPage={items_per_page}{query}"
        return API_url

    def __construct_session_url(self, id: str) -> str:
        """
        This function constructs the URL for the session API call. It takes the session ID and creates the correctly formatted string.
        :param id: The ID of the session you want to query
        :return: The constructed API url
        """
        return f"{self.base_url}/{id}"

    def __make_API_call(self, api_url: str, timeout: int = 15) -> dict:
        """
        This function makes the API call to the provided URL and returns the response as a dictionary.

        :param api_url: The URL to make the API call to
        :param timeout: The timeout for the API call
        :return: The response from the API call as a dictionary
        """
        try:
            response = requests.get(api_url, timeout=timeout)
            return response.json()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except ConnectionError as conn_err:
            print(f'Connection error occurred: {conn_err}')
        except Timeout as timeout_err:
            print(f'Timeout error occurred: {timeout_err}')
        except RequestException as req_err:
            print(f'An error occurred: {req_err}')
        except ValueError as json_err:
            print(f'JSON decoding failed: {json_err}')
        return None

    def fetch_Collection(self,
                                 items_per_page: str = 5,
                                 asn: str = "",
                                 date_before: str = "",
                                 date_after: str = "",
                                 date_strict_before: str = "",
                                 date_strict_after: str = ""
                                 ) -> dict:
        """
        This function makes the collection API call to the spoofer API. It takes the arguments and constructs the URL to make the call.

        :param items_per_page: The number of items per page you want to query
        :param date_before: The date you want to query before
        :param date_after: The date you want to query after
        :param date_strict_before: The date you want to query strictly before
        :param date_strict_after: The date you want to query strictly after
        :param asn: The number of the AS you want to query

        """
        if items_per_page <= 0:
            raise Spoofer_Argument_Exception(
                "Items per page must be greater than 0")

        optional_collection_arguments = self.__construct_optional_params(
            asn, date_before, date_strict_before, date_after, date_strict_after)
        api_url = self.__construct_collection_url(
            items_per_page=items_per_page, optional_collection_arguments=optional_collection_arguments)
        print(api_url)
        response = self.__make_API_call(api_url)
        return response

    def fetch_session(self, id: str):
        """
        This function makes the session API call to the spoofer API. It takes the session ID and constructs the URL to make the call.

        :param id: The ID of the session you want to query
        """
        api_url = self.__construct_session_url(id)
        return self.__make_API_call(api_url)
