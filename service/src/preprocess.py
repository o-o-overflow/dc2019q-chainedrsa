import sys, os, re, random, time
from shutil import copyfile


flag_file = sys.argv[1]
key_dir = sys.argv[2]
KEY_DIR = 'keys'
FLAG_DIR = 'flags'
MSG = ['This is letter %c\n', 'Letter is %c\n', 'The hint is %c\n']


def shuffle(key_dir, flag_len):
    items = [x for x in xrange(flag_len)]
    start = (int(time.time()) / (60 * 60 * 3) - 144218) * flag_len
    items = [x for x in xrange(start, start + flag_len)]
    random.shuffle(items)
    j = 0
    for i in items:
        src = os.path.join(key_dir, '%d.pem' % i)
        dst = os.path.join(KEY_DIR, '%d.pem' % j)
        copyfile(src, dst)
        src = os.path.join(key_dir, '%d.pub' % i)
        dst = os.path.join(KEY_DIR, '%d.pub' % j)
        copyfile(src, dst)
        j += 1

def scratch(flag_file):
    with open(flag_file, 'r') as f:
        line = f.readline().strip()
    # m = re.search('(?<={).*(?=})', line)
    # flag = m.group(0)
    flag = line
    i = 0
    for l in flag:
        msg = random.sample(MSG, 1)[0] % l
        dst = os.path.join(FLAG_DIR, '%d' % i)
        with open(dst, 'w') as f:
            f.write(msg)
        i += 1
    return len(flag)

def main():
    # flag_len = scratch(flag_file)
    shuffle(key_dir, flag_len)

if __name__ == '__main__':
    main()
