import jieba
import sys

if '__main__' == __name__:
	infile = sys.argv[1]
	outfile = sys.argv[2]

	segs = jieba.cut(open(infile).read())
	kwds = set(segs)
	ks = '\n'.join(kwds)
	open(outfile,"w").write(ks.encode("utf8"))

			
	

