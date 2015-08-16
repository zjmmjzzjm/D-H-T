import os

if (__name__ == "__main__"):
    dirname = "download/txt/"
    for f in os.listdir(dirname):
        cmd = "python download_torrent.py " + dirname + f
        print cmd
        os.system(cmd)


