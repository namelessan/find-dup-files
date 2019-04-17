import unittest
import core
import bonus
import find_duplicate_files as fdf
from subprocess import run
from os import getcwd


class Test_find_duplicate_files(unittest.TestCase):

    def setUp(self):
        self.dir = getcwd() + '/testDir'
        f1 = self.dir + '/a/d/g/f1'
        f2 = self.dir + '/b/e/h/f2'
        f3 = self.dir + '/c/f/i/f3'
        f4 = self.dir + '/a/d/f4'
        f5 = self.dir + '/b/e/f5'
        f6 = self.dir + '/c/f/f6'
        link_f4 = self.dir + '/link_to_f4'
        link_folder_g = self.dir + '/link_to_folder_g'

        self.require_files = [f1, f2, f3, f4, f5, f6]
        self.not_requires = [link_folder_g, link_f4]

        self.group_1 = [f1, f2, f3]
        self.group_2 = [f4, f5, f6]

        run('mkdir testDir', shell=True)
        run('mkdir testDir/a testDir/b testDir/c', shell=True)
        run('mkdir testDir/a/d testDir/b/e testDir/c/f', shell=True)
        run('mkdir testDir/a/d/g testDir/b/e/h testDir/c/f/i', shell=True)

        run('touch testDir/a/d/g/f1 testDir/b/e/h/f2 testDir/c/f/i/f3', shell=True)
        run('touch testDir/a/d/f4 testDir/b/e/f5 testDir/c/f/f6', shell=True)

        run('echo hello world > testDir/a/d/g/f1', shell=True)
        run('echo hello world > testDir/b/e/h/f2', shell=True)
        run('echo hello world > testDir/c/f/i/f3', shell=True)

        run('echo hello Intek > testDir/a/d/f4', shell=True)
        run('echo hello Intek > testDir/b/e/f5', shell=True)
        run('echo hello Intek > testDir/c/f/f6', shell=True)

        run('ln -s testDir/a/d/g testDir/link_to_folder_g', shell=True)
        run('ln -s testDir/a/d/f4 testDir/link_to_f4', shell=True)

    # def tearDown(self):
    #     run('rm -r testDir', shell=True)

    def test_scan_files(self):
        res_scan = core.scan_files(self.dir)
        for file in self.not_requires:
            self.assertNotIn(file, res_scan)
        for file in self.require_files:
            self.assertIn(file, res_scan)

    def test_group_file_by_size(self):
        res_scan = core.scan_files(self.dir)
        res_size = core.group_files_by_size(res_scan)
        for group in res_size:
            [self.assertIn(file, group) for file in self.require_files]

    def Test_find_duplicate_files(self):
        res_scan = core.scan_files(self.dir)
        res_size = core.group_files_by_size(res_scan)
        res_md5 = core.group_duplicate_files(res_size)
        for group in res_md5:
            if self.group_1[0] in group:
                [self.assertIn(file, group) for file in self.group_1]
            elif self.group_2[0] in group:
                [self.assertIn(file, group) for file in self.group_2]


if __name__ == '__main__':
    unittest.main()
