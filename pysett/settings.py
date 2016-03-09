import xml.etree.ElementTree as etree
import ast


class Record(object):
    pass


class Settings(object):

    def __init__(self, filename):
        self.filename = filename
        try:
            self._xml = etree.parse(self.filename)
            self._root = self._xml.getroot()
            self._parseContent(self._root)
        except (IOError, etree.ParseError):
            raise IOError('Invalid file specified. XML only.')

    def _parseContent(self, root):
        for tab in root:
            if tab.tag == 'tab':
                r = Record()
                setattr(self, self._readName(tab), r)
                for opt in tab:
                    if opt.tag == 'option':
                        setattr(r, self._readName(opt), self._parseValue(opt))

    def _readName(self, item):
        try:
            return item.attrib['name'].replace(' ', '_')
        except (AttributeError, KeyError):
            raise AttributeError('Option name not specified')

    def _readValue(self, item):
        return item.get('value')

    def _readDefault(self, item):
        return item.get('default')

    def _readType(self, item):
        _type = item.get('type')
        if _type:
            return _type
        else:
            return 'str'

    def _parseValue(self, item, value=None):
        vtype = self._readType(item)
        if value is None:
            value = self._readValue(item)

        if value is not None:
            if vtype == 'int':
                return int(value)
            elif vtype == 'str':
                return str(value)
            elif vtype == 'bool':
                return ast.literal_eval(value)
            else:
                return value

    def _getElement(self, name):
        xpath = ".//*[@name='{}']"
        element = self._root.find(xpath.format(name))
        if element is None:
            element = self._root.find(xpath.format(name.replace('_', ' ')))
        return element

    def reload(self):
        self._parseContent(self._root)

    def save(self):
        for cat_name, cat in self.__dict__.items():
            if not cat_name.startswith('_') and isinstance(cat, Record):
                for opt_name, opt in cat.__dict__.items():
                    element = self._getElement(opt_name)
                    if element is not None:
                        element.set('value', str(opt))

        self._xml.write(self.filename)

    def defaults(self):
        for tab in self._root:
            if tab.tag == 'tab':
                r = getattr(self, self._readName(tab))
                for opt in tab:
                    if opt.tag == 'option' and isinstance(r, Record):
                        setattr(r,
                                self._readName(opt),
                                self._parseValue(opt, self._readDefault(opt)))
