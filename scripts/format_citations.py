def change(author_str):
    authors = author_str.split('and')
    for i, _str in enumerate(authors):
        _str = _str.strip()
        last_name = _str.split(' ')[-1]
        authors[i] = f'{last_name}, {_str[:-len(last_name)].strip()}'
    return ' and '.join(authors)


if __name__ == "__main__":
    text = """
    Shulin Liu and Tao Yang and Tianchi Yue and Feng Zhang and Di Wang
    Zhao Guo and Yuan Ni and Keqiang Wang and Wei Zhu and Guotong Xie
    Heng-Da Xu and Zhongli Li and Qingyu Zhou and Chao Li and Zizhen Wang and Yunbo Cao and Heyan Huang and Xian-Ling Mao
    Li Huang and Junjie Li and Weiwei Jiang and Zhiyu Zhang and Minchuan Chen and Shaojun Wang and Jing Xiao
    
    """

    for _line in text.split('\n'):
        _line = _line.strip()
        if _line:
            print(change(_line))
