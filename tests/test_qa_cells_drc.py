__unittest = True

import unittest
import subprocess
import shutil

from pathlib import Path

class TestQaCellsDrc(unittest.TestCase):

    TEST_DATA_DIR = Path(__file__).parent / 'test_data'

    def setUp(self):
        if self.TEST_DATA_DIR.exists():
           shutil.rmtree(self.TEST_DATA_DIR) 
        self.TEST_DATA_DIR.mkdir()
        
    def test_keepout_heater_drc(self):

        keepout_heater_drc = Path(__file__).parents[2] / 'drc' / 'KEEP_OUT_HEATER.lydrc'
        keepout_heater_qa_cell = Path(__file__).parents[2] / 'qa_cells' / 'HEATER_PADDING' / 'QA_HEATER_PADDING.gds'
        report_file_path = keepout_heater_drc / 'keepout_heater_drc_report.lyrdb'

        sp_args = [
            'klayout_app',
            '-b',
            '-r',
            keepout_heater_drc.as_posix(),
            '-rd',
            f'input_layout={keepout_heater_qa_cell.as_posix()}',
            '-rd',
            f'output_report={report_file_path.as_posix()}'
        ]

        sp = subprocess.run(sp_args)

        self.assertEqual(sp.returncode, 1)