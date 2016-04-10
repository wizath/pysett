import unittest
import sys
sys.path.append('..')
from pysett.settings import Settings, Record
from xml.etree.ElementTree import ElementTree, Element
import xml.etree.ElementTree as et


class BasicTest(unittest.TestCase):

    def setUp(self):
        self.obj = Settings('dummy.xml')
        self.xmlstring = '''<settings>
            <tab name="general">
                <option name="text size" type="int" value="1" default="80"/>
                <option name="font" type="str" value="nop" default="Arial"/>
                <option name="enable" type="bool" value="True" default="True"/>
                <option name="list_test" type="list" value="[1,2,3,4]" default="[1]"/>
                <option name="dict_test" type="list" value="{'1' : 1, '2' : 2}" default="{'3' : 3}"/>
            </tab>
        </settings>'''

    def testFileNotFound(self):
        with self.assertRaises(IOError):
            test = Settings('not_existing_file.txt')
            del test

    def testIfLoadsProperly(self):
        test = Settings('dummy.xml')
        self.assertIsInstance(test._xml, ElementTree)
        self.assertIsInstance(test._root, Element)

    def testReadNameFunction(self):
        test = Element('option', {'name': 'Test'})
        testNoName = Element('option')
        testReplaceWhitespace = Element('option', {'name': 'test test'})

        self.assertEqual(self.obj._readName(test), 'Test', 'Wrong name')
        self.assertEqual(self.obj._readName(testReplaceWhitespace), 'test_test')
        with self.assertRaises(AttributeError):
            self.obj._readName(testNoName)

    def testReadTypeFunction(self):
        test = Element('option', {'type': 'int'})
        testNoType = Element('option')

        self.assertEqual(self.obj._readType(test), 'int')
        self.assertEqual(self.obj._readType(testNoType), 'str')

    def testReadDefaultFunction(self):
        testNoDefault = Element('option')
        testWithDefault = Element('option', {'default': '20'})

        self.assertEqual(self.obj._readDefault(testWithDefault), '20')
        self.assertEqual(self.obj._readDefault(testNoDefault), None)

    def testParseContentFunction(self):
        rootfile = et.fromstring(self.xmlstring)
        self.obj._parseContent(rootfile)

        # category
        self.assertIsInstance(self.obj.general, Record)

        # values
        self.assertEqual(self.obj.general.text_size, 1)
        self.assertEqual(self.obj.general.font, "nop")
        self.assertEqual(self.obj.general.enable, True)
        self.assertEqual(self.obj.general.list_test, [1,2,3,4])
        self.assertEqual(self.obj.general.dict_test, {'1': 1, '2': 2})

    def testReloadFunctionWithoutSaving(self):
        rootfile = et.fromstring(self.xmlstring)
        self.obj._parseContent(rootfile)
        self.obj._root = rootfile

        self.obj.general.text_size = 20
        self.obj.general.font = "changed"
        self.obj.general.enable = False

        self.obj.reload()

        self.assertEqual(self.obj.general.text_size, 1)
        self.assertEqual(self.obj.general.font, "nop")
        self.assertEqual(self.obj.general.enable, True)
        self.assertEqual(self.obj.general.list_test, [1,2,3,4])
        self.assertEqual(self.obj.general.dict_test, {'1': 1, '2': 2})

    def testSaveContentFunction(self):
        rootfile = et.fromstring(self.xmlstring)
        self.obj._parseContent(rootfile)
        self.obj._root = rootfile

        self.obj.general.text_size = 20
        self.obj.general.font = "changed"
        self.obj.general.enable = False

        self.obj.save()

        newroot = et.tostring(self.obj._root)

        nroot = et.fromstring(newroot)
        self.obj._parseContent(nroot)
        self.obj._root = nroot

        self.assertEqual(self.obj.general.text_size, 20)
        self.assertEqual(self.obj.general.font, "changed")
        self.assertEqual(self.obj.general.enable, False)
        self.assertEqual(self.obj.general.list_test, [1,2,3,4])
        self.assertEqual(self.obj.general.dict_test, {'1': 1, '2': 2})

    def testSetDefaultsFunction(self):
        rootfile = et.fromstring(self.xmlstring)
        self.obj._parseContent(rootfile)
        self.obj._root = rootfile

        self.obj.general.text_size = 9999
        self.obj.general.font = "changed"
        self.obj.general.enable = False

        self.obj.defaults()

        self.assertEqual(self.obj.general.text_size, 80)
        self.assertEqual(self.obj.general.font, "Arial")
        self.assertEqual(self.obj.general.enable, True)
        self.assertEqual(self.obj.general.list_test, [1])
        self.assertEqual(self.obj.general.dict_test, {'3': 3})

if __name__ == '__main__':
    unittest.main()
