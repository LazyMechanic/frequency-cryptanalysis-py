import frequency_analysis as fa
import time


def readFile(path):
    file = open(path, 'rt', encoding='utf-8')
    return file.read()


def writeToFile(s, path):
    file = open(path, 'w+', encoding='utf-8')
    file.write(s)
    file.close()


def doCharsEncryption(src, enc):
    out_file = '../out/out_by_chars.txt'

    src_table = fa.get_chars_freq_table(src)
    enc_table = fa.get_chars_freq_table(enc)
    decrypted = fa.decrypt_by_chars_freq_table(enc, src_table, enc_table)

    writeToFile(decrypted, out_file)


def doBigramsEncryption(src, enc):
    out_file = '../out/out_by_bigrams.txt'

    src_table = fa.get_bigrams_freq_table(src)
    enc_table = fa.get_bigrams_freq_table(enc)
    decrypted = fa.decrypt_by_bigrams_freq_table(enc, src_table, enc_table)

    writeToFile(decrypted, out_file)


def main():
    src_file = '../resource/text.txt'
    src = readFile(src_file)
    enc = fa.encrypt(src, 1)

    start_time = time.time()
    doCharsEncryption(src, enc)
    elapsed_time = time.time() - start_time
    print('Decryption time with chars: %ssec' % elapsed_time)

    start_time = time.time()
    doBigramsEncryption(src, enc)
    elapsed_time = time.time() - start_time
    print('Decryption time with bigrams: %ssec' % elapsed_time)


if __name__ == '__main__':
    main()
