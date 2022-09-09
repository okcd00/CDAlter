def change(author_str):
    authors = author_str.split('and')
    for i, _str in enumerate(authors):
        _str = _str.strip()
        last_name = _str.split(' ')[-1]
        authors[i] = f'{last_name}, {_str[:-len(last_name)].strip()}'
    return ' and '.join(authors)


if __name__ == "__main__":
    text = """
    Ruiqing Zhang and Chao Pang and Chuanqiang Zhang and Shuohuan Wang and Zhongjun He and Yu Sun and Hua Wu and Haifeng Wang
    """

    for _line in text.split('\n'):
        _line = _line.strip()
        if _line:
            print(change(_line))
