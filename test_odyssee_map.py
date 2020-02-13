import unittest
import odyssee_map

class NominalCase(unittest.TestCase):

    def test_min_parse_arguments(self):
        result = odyssee_map.parse_parameters(["-i","my_file.md"])
        self.assertEqual(result, ('my_file.md', 'pdf', 'odyssee-map', 'example/color_places.toml.example'))

    def test_max_parse_arguments(self):
        result = odyssee_map.parse_parameters(["-i","my_file2.md","-o","my_output","-cf","my_colors","-f","png"])
        self.assertEqual(result, ('my_file2.md', 'png', 'my_output', 'my_colors'))

    def test_extract_additionnal_info(self):
        result = odyssee_map.extract_additional_infos("15PA")
        self.assertEqual(result,("",30,"15PA"))
        result = odyssee_map.extract_additional_infos("{hEll0 W0rld. }")
        self.assertEqual(result,(" {hEll0 W0rld. } ",15,"0PA"))

    def test_extract_info(self):
        result = odyssee_map.extract_info_fromline("Paris->15PA->Toulouse")
        self.assertEqual(result,("Paris","Toulouse",30,"15PA",""))        
        result = odyssee_map.extract_info_fromline("Paris->{TGV}->Toulouse")
        self.assertEqual(result,("Paris","Toulouse",15,"0PA"," {TGV} "))
        result = odyssee_map.extract_info_fromline(" Paris ->{ TGV }-> Toulouse ")
        self.assertEqual(result,("Paris","Toulouse",15,"0PA"," {TGV} "))
        # Next test does not pass but I would like to obtain this result
        #result = odyssee_map.extract_info_fromline("La Capitale ->{ma voiture}->le bord de mer")
        #self.assertEqual(result,("La Capitale","le bord de mer",15,"0PA"," {ma voiture} "))

class BadCase(unittest.TestCase):

    def test_parse_arguments_required_arg(self):
        with self.assertRaises(SystemExit):
            odyssee_map.parse_parameters(["file"])

    def test_extract_bad_file(self):
        with self.assertRaises(ValueError):
            odyssee_map.extract_info_fromline("Paris->15PA{tgv}->Toulouse")


if __name__ == '__main__':
    unittest.main()
