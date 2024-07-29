import unittest

from classifiers.headers_classifier.headers_classifier import HeadersClassifier
from classifiers.headers_classifier.model.matching_headers import MatchingHeaders
from classifiers.headers_classifier.model.confidence_calculation import ConfidenceCalculation
from classifiers.headers_classifier.model.matching_header import MatchingHeader
from entities.table_processing.row_content import RowContent
from tests.unit_tests.classifiers.headers_classifier.headers_classifier_test_base import HeadersClassifierTestBase
from tests.unit_tests.common_unit_tests_utils import cd_to_project_root_path


class TestHeadersClassifier(HeadersClassifierTestBase):

    def setUp(self):
        cd_to_project_root_path()
        self.__under_test = HeadersClassifier()

    def test_should_return_correct_matching_headers_for_given_headers_content(self):
        # Given
        read_headers_content = ['Lp:', 'Rozliczenie z tytułu', 'Wartość netto (zł)', 'Stawka VAT (%)', 'Kwota VAT (zł)',
                                'Wartość brutto (zł)', 'Zużycie [kWh]']
        input_headers_content = RowContent(read_headers_content)

        # When
        found_matching_headers = self.__under_test.assign_corresponding_headers(input_headers_content)

        # Then
        expected_matching_headers = MatchingHeaders([
            MatchingHeader('Lp:', ConfidenceCalculation('ordinal_number', 1.0), 0),
            MatchingHeader('Rozliczenie z tytułu', ConfidenceCalculation('name', 1.0), 1),
            MatchingHeader('Wartość netto (zł)', ConfidenceCalculation('net_value', 1.0), 2),
            MatchingHeader('Stawka VAT (%)', ConfidenceCalculation('vat', 1.0), 3),
            MatchingHeader('Kwota VAT (zł)', ConfidenceCalculation('vat_value', 1.0), 4),
            MatchingHeader('Wartość brutto (zł)', ConfidenceCalculation('gross_value', 1.0), 5),
            MatchingHeader('Zużycie [kWh]', ConfidenceCalculation('quantity', 0.5), 6)
        ])
        self.assert_matching_headers_results(expected_matching_headers, found_matching_headers)

    def test_should_return_correct_matching_headers_for_given_headers_content_when_content_contains_typos(self):
        # Given
        read_headers_content = ['Lp.', 'Naza uslug', 'Cea ntto', 'losc']
        input_headers_content = RowContent(read_headers_content)

        # When
        found_matching_headers = self.__under_test.assign_corresponding_headers(input_headers_content)

        # Then
        expected_matching_headers = MatchingHeaders([
            MatchingHeader('Lp.', ConfidenceCalculation('ordinal_number', 1.0), 0),
            MatchingHeader('Naza uslug', ConfidenceCalculation('name', 0.8080808080808081), 1),
            MatchingHeader('Cea ntto', ConfidenceCalculation('net_price', 0.873015873015873), 2),
            MatchingHeader('losc', ConfidenceCalculation('quantity', 0.8888888888888888), 3),
        ])
        self.assert_matching_headers_results(expected_matching_headers, found_matching_headers)

    def test_should_assign_to_any_not_used_matching_header_when_content_does_not_match_any_patterns_set(self):
        # Given
        read_headers_content = ['Lp', 'Nazwa usługi', 'Cena netto', 'ilość', 'should be wrongly assigned']
        input_headers_content = RowContent(read_headers_content)

        # When
        found_matching_headers = self.__under_test.assign_corresponding_headers(input_headers_content)

        # Then
        expected_matching_headers = MatchingHeaders([
            MatchingHeader('Lp', ConfidenceCalculation('ordinal_number', 1.0), 0),
            MatchingHeader('Nazwa usługi', ConfidenceCalculation('name', 1.0), 1),
            MatchingHeader('Cena netto', ConfidenceCalculation('net_price', 1.0), 2),
            MatchingHeader('ilość', ConfidenceCalculation('quantity', 1.0), 3),
            MatchingHeader('should be wrongly assigned', ConfidenceCalculation('gross_price', 0.3088235294117647), 4)
        ])
        self.assert_matching_headers_results(expected_matching_headers, found_matching_headers)

    def test_should_assign_to_different_not_used_matching_header_when_content_does_not_match_any_patterns_set(self):
        # Given
        read_headers_content = ['Lp', 'Nazwa usługi', 'Cena netto', 'ilość', 'cena jednost brutto',
                                'should be wrongly assigned']
        input_headers_content = RowContent(read_headers_content)

        # When
        found_matching_headers = self.__under_test.assign_corresponding_headers(input_headers_content)

        # Then
        expected_matching_headers = MatchingHeaders([
            MatchingHeader('Lp', ConfidenceCalculation('ordinal_number', 1.0), 0),
            MatchingHeader('Nazwa usługi', ConfidenceCalculation('name', 1.0), 1),
            MatchingHeader('Cena netto', ConfidenceCalculation('net_price', 1.0), 2),
            MatchingHeader('ilość', ConfidenceCalculation('quantity', 1.0), 3),
            MatchingHeader('cena jednost brutto', ConfidenceCalculation('gross_price', 0.9259259259259259), 4),
            MatchingHeader('should be wrongly assigned', ConfidenceCalculation('net_value', 0.30094905094905094), 5)
        ])
        self.assert_matching_headers_results(expected_matching_headers, found_matching_headers)

    def test_should_not_assign_to_the_same_matching_header_twice_when_content_does_not_match_any_patterns_set(self):
        # Given
        read_headers_content = ['Lp', 'Nazwa usługi', 'Cena netto', 'should be wrongly assigned',
                                'ilość', 'cena jednostaaaaa brutto']
        input_headers_content = RowContent(read_headers_content)

        # When
        found_matching_headers = self.__under_test.assign_corresponding_headers(input_headers_content)

        # Then
        expected_matching_headers = MatchingHeaders([
            MatchingHeader('Lp', ConfidenceCalculation('ordinal_number', 1.0), 0),
            MatchingHeader('Nazwa usługi', ConfidenceCalculation('name', 1.0), 1),
            MatchingHeader('Cena netto', ConfidenceCalculation('net_price', 1.0), 2),
            MatchingHeader('ilość', ConfidenceCalculation('quantity', 1.0), 4),
            MatchingHeader('cena jednostaaaaa brutto', ConfidenceCalculation('gross_price', 0.8985507246376812), 5),
        ])
        self.assert_matching_headers_results(expected_matching_headers, found_matching_headers)

    def test_should_throw_value_error_when_overall_headers_fit_is_too_small(self):
        # Given
        read_headers_content = ['Some dummy text that will not fit', 'Blah blah blah blah',
                                'Greetings from the testing phase', 'Polan strong he he he']
        input_headers_content = RowContent(read_headers_content)

        # When/Then
        with self.assertRaises(ValueError) as context:
            self.__under_test.assign_corresponding_headers(input_headers_content)

        # Check the exception message
        self.assertEqual(str(context.exception), "Incorrect invoice table - cannot match headers content to known "
                                                 "header values.")