import unittest
import sys
import os
cwd = os.getcwd()
cwd.replace('\\test',"")
sys.path.append(cwd)

from Artus3DAPI import Artus3DAPI



class TestCasesArtus3DAPI(unittest.TestCase):

    artus_test_api = Artus3DAPI()

    def test_success(self):

        # check some constraint values
        output = self.artus_test_api.get_constraints()
        self.assertEqual(output['thumb_spread']['min'],-30)
        self.assertNotEqual(output['pinky_d2']['min'],-10)

        # check only updating the values that match params
        valid = self.artus_test_api.update_joint_params({'pinky_d2':{'velocity':20,'position':100}})
        self.assertEqual(valid['pinky_d2']['velocity'],20)
        self.assertEqual(valid['thumb_flex']['position'],0)

        # check compare constraints
        valid_target = self.artus_test_api.send_target_command()
        self.assertEqual(valid_target['pinky_d2']['position'],90)
        print(self.artus_test_api.robot_command)

if __name__ == "__main__":
    unittest.main()