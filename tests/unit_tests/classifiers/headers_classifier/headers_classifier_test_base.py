from classifiers.headers_classifier.model.matching_headers import MatchingHeaders


class HeadersClassifierTestBase:

    @staticmethod
    def assert_matching_headers_results(expected_matching_headers: MatchingHeaders,
                                        actual_matching_headers: MatchingHeaders) -> None:
        assert len(expected_matching_headers.headers) == len(actual_matching_headers.headers)

        sorted_expected_headers = sorted(expected_matching_headers.headers, key=lambda header: header.column_index)
        sorted_actual_headers = sorted(actual_matching_headers.headers, key=lambda header: header.column_index)

        for actual, expected in zip(sorted_actual_headers, sorted_expected_headers):
            assert actual.phrase == expected.phrase
            assert actual.confidence_calculation.value == expected.confidence_calculation.value
            assert actual.confidence_calculation.confidence == expected.confidence_calculation.confidence
