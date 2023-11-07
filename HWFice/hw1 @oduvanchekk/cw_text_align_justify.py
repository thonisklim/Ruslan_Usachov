def justify1(text, width):
    new_text = text.split(' ')
    last_index = 0
    counter = 0
    for word_index in range(len(new_text)):
        counter += len(new_text[word_index])
        if counter >= width:
            counter = sum([len(new_text[i]) for i in range(word_index - last_index)])
            new_text[word_index - 1] += '\n'
            i = last_index
            while width - counter > 0:
                # -1 because we don`t want to add ' ' to last word
                if i >= word_index - 2:
                    i = last_index
                new_text[i] += ' '
                counter += 1
                i += 1

            last_index = word_index - 1
            counter = len(new_text[word_index])
        # because of ' '
        counter += 1
        # print(new_text)

    return ''.join(new_text)
    # return new_text


def justify(text, width):
    new_text = text.split(' ')
    last_index = 0
    line_width = 0
    for word_index in range(len(new_text)):
        if line_width + len(new_text[word_index]) > width:
            line_width -= 1
            while line_width < width:
                if word_index - 1 > last_index:
                    for i in range(word_index - 1 - last_index):
                        # print(new_text)
                        if line_width < width:
                            new_text[i + last_index] += ' '
                            line_width += 1
                        else:
                            break
                else:
                    break
            new_text[word_index - 1] = new_text[word_index - 1].replace(' ', '\n')
            last_index = word_index
            line_width = 0
        new_text[word_index] += ' '
        line_width += len(new_text[word_index])
    new_text[-1] = new_text[-1].replace(' ', '')
    return ''.join(new_text)
    #return new_text


lorem = ['Lorem', 'ipsum', 'dolor', 'sit', 'amet,', 'consectetur', 'adipiscing', 'elit.', 'Vestibulum', 'sagittis',
              'dolor', 'mauris,', 'at', 'elementum', 'ligula', 'tempor', 'eget.', 'In', 'quis', 'rhoncus', 'nunc,', 'at',
              'aliquet', 'orci.', 'Fusce', 'at', 'dolor', 'sit', 'amet', 'felis', 'suscipit', 'tristique.', 'Nam', 'a',
              'imperdiet', 'tellus.', 'Nulla', 'eu', 'vestibulum', 'urna.', 'Vivamus', 'tincidunt', 'suscipit', 'enim,',
              'nec', 'ultrices', 'nisi', 'volutpat', 'ac.', 'Maecenas', 'sit', 'amet', 'lacinia', 'arcu,', 'non',
              'dictum', 'justo.', 'Donec', 'sed', 'quam', 'vel', 'risus', 'faucibus', 'euismod.', 'Suspendisse',
              'rhoncus', 'rhoncus', 'felis', 'at', 'fermentum.', 'Donec', 'lorem', 'magna,', 'ultricies', 'a', 'nunc',
              'sit', 'amet,', 'blandit', 'fringilla', 'nunc.', 'In', 'vestibulum', 'velit', 'ac', 'felis', 'rhoncus',
              'pellentesque.', 'Mauris', 'at', 'tellus', 'enim.', 'Aliquam', 'eleifend', 'tempus', 'dapibus.',
              'Pellentesque', 'commodo,', 'nisi', 'sit', 'amet', 'hendrerit', 'fringilla,', 'ante', 'odio', 'porta',
          'lacus,', 'ut', 'elementum', 'justo', 'nulla', 'et', 'dolor.']

print(justify(' '.join(lorem * 5), 100))
# print(justify('123 45 6', 7))
