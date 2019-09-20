from sauron.parsers import DefaultParser


class TestCaseOne:
    test_string = """
    [
        {
            "name": "first_condition",
            "args": {"lower_number": 3, "greater_number": 10},
            "job_type": "condition"
        },
        {
            "name": "print_the_equation",
            "args": {"lower_number": 3, "greater_number": 10},
            "job_type": "action"
        }
    ]
    """

    def setup(self):
        test_string = self.test_string.strip()
        p = DefaultParser()
        result = p.parse(test_string)
        return result

    def test_can_parse_the_test_string(self):
        result = self.setup()

        assert result is not None

    def test_acuratelly_parsed_first_job(self):
        result = self.setup()
        assert result[0].name == "first_condition"
        assert result[0].args == {"lower_number": 3, "greater_number": 10}
        assert result[0].job_type == "condition"

    def test_acuratelly_parsed_second_job(self):
        result = self.setup()
        assert result[1].name == "print_the_equation"
        assert result[1].args == {"lower_number": 3, "greater_number": 10}
        assert result[1].job_type == "action"
