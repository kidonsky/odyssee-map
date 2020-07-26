import unittest
import contextlib
import subprocess
import toml
import odyssee_map

logfile = open(".tests_output.log", "w")
defaults_file = open("default_values.toml", "r")
defaults_loaded = toml.loads(defaults_file.read())
defaults = defaults_loaded["argparse_default_values"]
duration_offset = defaults_loaded["edge_default_values"]["duration_offset"]
duration_landings = defaults_loaded["edge_default_values"]["duration_landings"]
defaults_file.close()


class NominalCase(unittest.TestCase):

    def test_min_parse_arguments(self):
        with contextlib.redirect_stdout(logfile):
            result = odyssee_map.parse_parameters(["-i", ' my_5é~#"ile.md'], defaults)
        self.assertEqual(result, (' my_5é~#"ile.md', 'pdf', 'odyssee-map', 'example/color_places.toml.example', True))

    def test_max_parse_arguments(self):
        with contextlib.redirect_stdout(logfile):
            result = odyssee_map.parse_parameters(
                ["-i", "my_file2.md", "-o", "my_output", "-cf", "my_colors", "-f", "png", "-noview"],
                defaults)
        self.assertEqual(result, ('my_file2.md', 'png', 'my_output', 'my_colors', False))

    def test_extract_additionnal_value(self):
        with contextlib.redirect_stdout(logfile):
            result = odyssee_map.extract_additional_infos("15PA", 5)
        self.assertEqual(result, ("", 30, "15PA"))

    def test_extract_additionnal_bigvalue(self):
        with contextlib.redirect_stdout(logfile):
            result = odyssee_map.extract_additional_infos("500000PA", 5)
        self.assertEqual(result, ("", 500015, "500000PA"))

    def test_extract_additionnal_info_note(self):
        with contextlib.redirect_stdout(logfile):
            result = odyssee_map.extract_additional_infos("{hEll0 W0rld. }", 5)
        self.assertEqual(result, (" {hEll0 W0rld. } ", 15, "0PA"))

    def test_extract_info_value(self):
        with contextlib.redirect_stdout(logfile):
            result = odyssee_map.extract_info_fromline("Paris->15PA->Toulouse", 5)
        self.assertEqual(result, ("Paris", "Toulouse", 30, "15PA", ""))

    def test_extract_info_note(self):
        with contextlib.redirect_stdout(logfile):
            result = odyssee_map.extract_info_fromline("Paris->{TGV}->Toulouse", 5)
        self.assertEqual(result, ("Paris", "Toulouse", 15, "0PA", " {TGV} "))

    def test_extract_info_notewithspaces(self):
        with contextlib.redirect_stdout(logfile):
            result = odyssee_map.extract_info_fromline(" Paris ->{ TGV }-> Toulouse ", 5)
        self.assertEqual(result, ("Paris", "Toulouse", 15, "0PA", " { TGV } "))

# This test does not pass but I would like to obtain this result
#   def test_extract_info_placeswithspaces(self):
#       with contextlib.redirect_stdout(logfile):
#       result = odyssee_map.extract_info_fromline("La Capitale ->{ma voiture}->le bord de mer")
#       self.assertEqual(result,("La Capitale","le bord de mer",15,"0PA"," {ma voiture} "))

    def test_main(self):
        with contextlib.redirect_stdout(logfile):
            result = odyssee_map.main(
                ["-i", "example/places-example.txt", "-o", "outputfile", "-noview"])
        self.assertEqual(result, 0)
        ls_result = subprocess.run(["ls", "output"], capture_output=True, text=True)
        self.assertIn("outputfile.pdf", ls_result.stdout)


class BadCase(unittest.TestCase):

    def test_parse_arguments_required_arg(self):
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(logfile):
                odyssee_map.parse_parameters(["file"], defaults)

    def test_parse_arguments_bad_arg(self):
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(logfile):
                odyssee_map.parse_parameters(["-i", "my_file2.md", "-f", "pg"], defaults)

    def test_extract_noteandduration(self):
        with self.assertRaises(AssertionError):
            with contextlib.redirect_stderr(logfile):
                odyssee_map.extract_info_fromline("Paris->15PA{tgv}->Toulouse", 5)

    def test_extract_negativeduration(self):
        with self.assertRaises(AssertionError):
            with contextlib.redirect_stderr(logfile):
                odyssee_map.extract_info_fromline("Paris->-5PA->Toulouse", 5)

    def test_extract_threelocations(self):
        with self.assertRaises(AssertionError):
            with contextlib.redirect_stderr(logfile):
                odyssee_map.extract_info_fromline("Paris->5PA->Toulouse->Fusée", 5)

    def test_extract_durationstr(self):
        with self.assertRaises(AssertionError):
            with contextlib.redirect_stderr(logfile):
                odyssee_map.extract_info_fromline("Paris->beaucoupPA->Toulouse", 5)


if __name__ == '__main__':
    unittest.main()
