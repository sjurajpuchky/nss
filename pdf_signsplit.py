import re
import sys
import binascii


regex = regex = r'.*ByteRange.*?\[.*?(?P<start0>[0-9]+).*?(?P<len0>[0-9]+).*?(?P<start1>[0-9]+).*?(?P<len1>[0-9]+).*'

def fwrite(file,content):
	f2 = open(file,'wb')
	f2.write(content)
	f2.flush()
	f2.close()

if len(sys.argv) < 2:
	print "use: %s file.pdf" % (sys.argv[0])
	sys.exit(-1)


inpdf = sys.argv[1]

pdfcontent = "%s.content" % inpdf
pdfsign = "%s.sign" % inpdf

f = open(inpdf,'rb')
tmp = f.read()
f.close()

res = re.search(regex,tmp)


if res is None:
	print "fail to find sign range"
	sys.exit(-1)
print res.groupdict()

start0 = int(res.group('start0'))
len0 = int(res.group('len0'))
end0 = start0+len0
start1 = int(res.group('start1'))
len1 = int(res.group('len1'))
end1 = start1+len1

sigstart = end0 + 1
sigend = start1 - 1

tmp2 = bytearray(tmp)

content = tmp2[start0:end0] + tmp2[start1:end1]
sign_hex = tmp2[sigstart:sigend]
sign = binascii.unhexlify(sign_hex)

fwrite(pdfcontent,content)
fwrite(pdfsign,sign)


