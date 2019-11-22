_cyrillic_alphabet_lower = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
_cyrillic_alphabet_upper = _cyrillic_alphabet_lower.upper()
_cyrillic_alphabet = _cyrillic_alphabet_lower + _cyrillic_alphabet_upper

_cyrillic_alphabet_lower_set = {ch for ch in _cyrillic_alphabet_lower}
_cyrillic_alphabet_upper_set = {ch for ch in _cyrillic_alphabet_upper}
_cyrillic_alphabet_set = {ch for ch in _cyrillic_alphabet}


def _is_cyrillic(ch):
    return ch in _cyrillic_alphabet_set


def _get_only_cyrillic(s):
    only_cyrillic_list = []
    for ch in s:
        if _is_cyrillic(ch):
            only_cyrillic_list.append(ch)

    return ''.join(only_cyrillic_list)


def get_chars_freq_table(s):
    lowercase_s = s.lower()
    only_cyrillic = _get_only_cyrillic(lowercase_s)

    chars_freq_table = {}
    for ch in only_cyrillic:
        if ch in chars_freq_table:
            chars_freq_table[ch] += 1
        else:
            # Set default value
            chars_freq_table[ch] = 1

    # Sort by value
    sorted_chars_freq_table = sorted(chars_freq_table.items(), key=lambda kv: kv[1], reverse=True)
    return sorted_chars_freq_table


def _get_word_bigrams(word):
    bigrams = {}
    for i in range(0, len(word), 2):
        bigram = word[i:i + 2]
        if bigram in bigrams:
            bigrams[bigram] += 1
        else:
            bigrams[bigram] = 1
    return bigrams


def _update_bigrams_freq_table(bigrams_freq_table, updates):
    cpy = bigrams_freq_table.copy()
    for key in updates:
        if key in cpy:
            cpy[key] += updates[key]
        else:
            cpy[key] = updates[key]
    return cpy


def get_bigrams_freq_table(s):
    lowercase_s = s.lower()

    bigrams_freq_table = {}

    begin = -1
    end_index = len(lowercase_s) - 1

    for i in range(0, end_index + 1):
        if not _is_cyrillic(lowercase_s[i]) or i == end_index:
            if begin != -1:
                end = i if i != end_index else i + 1

                word = lowercase_s[begin:end]
                bigrams_freq_table = _update_bigrams_freq_table(bigrams_freq_table, _get_word_bigrams(word))

                begin = -1
        else:
            if begin == -1:
                begin = i

    # Sort by value
    sorted_bigrams_freq_table = sorted(bigrams_freq_table.items(), key=lambda kv: kv[1], reverse=True)
    return sorted_bigrams_freq_table


def encrypt(src, shift):
    shifted_alphabet_lower = _cyrillic_alphabet_lower[shift:] + _cyrillic_alphabet_lower[:shift]
    shifted_alphabet_upper = _cyrillic_alphabet_upper[shift:] + _cyrillic_alphabet_upper[:shift]

    table_lower = str.maketrans(_cyrillic_alphabet_lower, shifted_alphabet_lower)
    table_upper = str.maketrans(_cyrillic_alphabet_upper, shifted_alphabet_upper)

    encrypted = src \
        .translate(table_lower) \
        .translate(table_upper)

    return encrypted


def decrypt_by_chars_freq_table(enc, src_freq_table, enc_freq_table):
    src_freq_table_string = ''.join([pair[0] for pair in src_freq_table])
    enc_freq_table_string = ''.join([pair[0] for pair in enc_freq_table])

    # Fill a enc freq table to the length of the src freq table
    src_freq_table_string = src_freq_table_string[0:len(enc_freq_table_string)]

    table_lower = str.maketrans(enc_freq_table_string, src_freq_table_string)
    table_upper = str.maketrans(enc_freq_table_string.upper(), src_freq_table_string.upper())

    decrypted = enc \
        .translate(table_lower) \
        .translate(table_upper)

    return decrypted


def _decrypt_word_by_bigrams(enc_word, src_freq_table, enc_freq_table):
    dec_word = ''
    for i in range(0, len(enc_word), 2):
        bigram = enc_word[i:i + 2]
        index = next((i for i in range(len(enc_freq_table)) if enc_freq_table[i][0] == bigram), -1)

        if index == -1:
            raise Exception('Bigram in encryption frequency table not found')

        if index > len(src_freq_table) - 1:
            raise Exception('Encryption frequency table greater than source frequency table')

        dec_word += src_freq_table[index][0]
    return dec_word


def decrypt_by_bigrams_freq_table(enc, src_freq_table, enc_freq_table):
    lowercase_s = enc.lower()
    src_freq_table = src_freq_table[0:len(enc_freq_table)]

    begin = -1
    end_index = len(lowercase_s) - 1
    decrypted = ''

    for i in range(0, len(lowercase_s)):
        if not _is_cyrillic(lowercase_s[i]) or i == end_index:
            if begin != -1:
                end = i if i != end_index else i + 1

                enc_word = lowercase_s[begin:end]
                dec_word = _decrypt_word_by_bigrams(enc_word, src_freq_table, enc_freq_table)
                decrypted += dec_word

                begin = -1
        else:
            if begin == -1:
                begin = i

        if not _is_cyrillic(lowercase_s[i]):
            decrypted += lowercase_s[i]

    return decrypted
