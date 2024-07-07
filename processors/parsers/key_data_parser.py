from entities.key_data_processing.search_response import SearchResponse
from extractors.value_finding_status import ValueFindingStatus
from entities.key_data_processing.key_data import KeyData


class KeyDataParser:

    @staticmethod
    def parse_key_data(search_responses: list[SearchResponse]) -> KeyData:
        key_data = dict()
        for key_response in search_responses:
            if key_response.status == ValueFindingStatus.FOUND:
                key_data[key_response.key_word] = key_response.value
            else:
                key_data[key_response.key_word] = None
        return KeyData(key_data)
