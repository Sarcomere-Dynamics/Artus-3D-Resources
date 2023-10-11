import unittest
import sys
import os
cwd = os.getcwd()
cwd.replace('\\test',"")
sys.path.append(cwd)

from Artus3DAPI import Artus3DAPI
from src.Artus3DJoint import Artus3DJoint



class TestCasesArtus3DAPI(unittest.TestCase):

    artus_test_api = Artus3DAPI()

    def test_data_send_target_command(self):
        self.artus_test_api.joints['thumb_spread'].input_angle = 80
        self.artus_test_api.joints['thumb_spread'].input_speed = 90
        self.assertNotEqual(self.artus_test_api.send_target_command(),f'c176p[0,80,0,0,0,0,0,0,0,0,0,0,0,0,0,0]v[80,90,80,80,80,80,80,80,80,80,80,80,80,80,80,80]end\n')
        self.assertEqual(self.artus_test_api.send_target_command(),f'c176p[0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0]v[80,90,80,80,80,80,80,80,80,80,80,80,80,80,80,80]end\n')

if __name__ == "__main__":
    unittest.main()