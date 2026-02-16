import unittest

# -------------------------------------- Class ---------------------------------------------
class TestNamesMethod(unittest.TestCase):
     def test_names(self):
        lst_names = ["Guillaume", "Gilles", "Juliette", "Antoine", "François", "Cassandre"]
        nb_names = count_names_more_7_caracters(names=lst_names)
        self.assertEqual(nb_names, 4) # Check if the number of name with more than 7 caracters are 4

# -------------------------------------- Function ---------------------------------------------
def count_names_more_7_caracters(names : list) -> int:
    """
    Count names with more than seven letters

    Param: 
        - names (list) : list with names to count
    
    return: 
        - more_than_seven (int) : Number of name with more than 7 caracters
    """
    more_than_seven = 0
    for name in names:
        if len(name) > 7:
            more_than_seven += 1
            print(name + " est un prénom avec un nombre de lettres supérieur à 7")
        else:
            print(name + " est un prénom avec un nombre de lettres inférieur ou égal à 7")
    return more_than_seven

# -------------------------------------- Launcher ---------------------------------------------
if __name__=='__main__':
    unittest.main()