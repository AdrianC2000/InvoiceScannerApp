from entities.key_data_processing.search_response import SearchResponse
from extractors.value_finding_status import ValueFindingStatus
from entities.key_data_processing.key_data import KeyData


class KeyDataParser:

    def __init__(self, search_responses: list[SearchResponse]):
        self.__search_responses = search_responses

    def parse_key_data(self) -> KeyData:
        key_data = dict()
        for key_response in self.__search_responses:
            if key_response.status == ValueFindingStatus.FOUND:
                key_data[key_response.key_word] = key_response.value
            else:
                key_data[key_response.key_word] = None
        return KeyData(key_data)
