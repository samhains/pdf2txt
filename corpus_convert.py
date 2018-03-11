
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import string
import re
import string
from os import listdir
from os.path import isfile, join

def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text


def is_digit(word):
    try:
        int(word)
        return True
    except ValueError:
        return False


def transliterate(line):
    cedilla2latin = [[u'Á', u'A'], [u'á', u'a'], [u'Č', u'C'], [u'č', u'c'], [u'Š', u'S'], [u'š', u's']]
    tr = dict([(a[0], a[1]) for (a) in cedilla2latin])
    new_line = ""
    for letter in line:
        if letter in tr:
            new_line += tr[letter]
        else:
            new_line += letter
    return new_line

def replace_with_conditions(conditions, text):
    # use these three lines to do the replacement
    rep = dict((re.escape(k), v) for k, v in conditions.iteritems())
    key_join = "|".join(rep.keys())
    pattern = re.compile(key_join)
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], text)

def remove_non_printable(s):
    printable = set(string.printable)
    return filter(lambda x: x in printable, s)

def remove_single_chars(text):
    blacklisted_strings =  [r'\s{}\s'.format(c) for c in "abcdefghijklmnopqrstuvwxyz."]
    s=  "|".join(blacklisted_strings)
    line = re.sub(s, "~ ", text)
    blacklisted_strings =  [r'\s{}~'.format(c) for c in "abcdefghijklmnopqrstuvwxyz."]
    s=  "|".join(blacklisted_strings)
    line = re.sub(s, "", line)
    line = re.sub("~", "", line)
    return line

def clean_pdf(fname):
    text = convert(fname+".pdf")

    # decode line to worrk with utf8 symbols
    line = text.decode('utf8')
    blacklisted_chars =  [c for c in "`_#$^"]
    blacklisted_dict = {k: "" for k in blacklisted_chars}
    conditions = {"+": ' ', ":": " ", "''": "", "\"": "", "pg.": "", "pg-": "", "pg": "", "pg+": ""}
    conditions.update(blacklisted_dict)
    line = remove_non_printable(line)
    line = replace_with_conditions(conditions, line)
    # remove digits with regex
    # remove digits with regex
    line = re.sub("(^|\W)\d+($|\W)", " ", line)
    # OR remove digits with casting to int
    new_line = []
    for word in line.split():
        if not is_digit(word):
            new_line.append(word)
    line = " ".join(new_line)
    # transliterate to Latin characters
    line = transliterate(line)
    line = line.lower()
    line = remove_single_chars(line)
    line = line.lower()

    text_file = open(fname+".txt", "w")
    text_file.write(line)
    text_file.close()

# path = "./corporate"
# onlyfiles = [path+"/"+f.split(".")[0] for f in listdir(path) if isfile(join(path, f)) and f.endswith(".pdf")]
# print(onlyfiles[31:])
for f in onlyfiles:
    try:
        print("filename", f)
        clean_pdf(f)

    except EOFError:
        print('Why did you do an EOF on me?')

    except KeyboardInterrupt:
        print('You cancelled the operation.')
    except:
        print('An error occurred.')
# clean_pdf("test")
