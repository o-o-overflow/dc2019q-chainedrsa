import sys, os, re, random, time
from shutil import copyfile


flag_file = sys.argv[1]
FLAG_DIR = 'flags'
MSG = ['This is letter %c\n', 'Letter is %c\n', 'The hint is %c\n']

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
    flag_len = scratch(flag_file)
    # shuffle(key_dir, flag_len)

if __name__ == '__main__':
    main()
