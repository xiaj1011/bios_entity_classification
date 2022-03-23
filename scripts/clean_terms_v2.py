import pandas as pd


class Filter:
    white_char_pattern = r"[a-z0-9()\[\]{}.,\-+' ]+"

    black_words = {'however', 'therefore', 'has', 'had', 'have', 'what', 'where', 'whereas', 'wherein',
                   'when', 'who', 'why', 'how', 'is', 'are', 'such', 'that', 'including', 'is', 'due',
                   'although', 'today', 'tomorrow', 'can', 'will', 'hope', 'wish', 'rare', 'very', 'next', 'even',
                   'also', 'must', 'though', 'should', 'those', 'become', 'here', 'show', 'always',
                   'almost', 'include', 'better', 'rather', 'often', 'appear', 'ever', 'thus', 'whether',
                   'either', 'anything', 'something', 'actual', 'already', 'further', 'then', 'indeed',
                   'hence', 'besides', 'but', 'was',
                   'wuhan', 'china', 'beijing', 'shanghai', 'shenzhen', 'guangzhou'}

    black_whole_words = {'severe', 'falls', 'sharp', 'lead', 'site', 'location'}

    black_head_tail_words = {'for', 'the', 'and', 'or', 'in', 'of', 'with', 'without', 'by', 'on', 'to', 'at', 'just',
                             'because', 'good', 'seem', 'too', 'both', 'between', 'need', 'never', 'as',
                             'another', 'while', 'since', 'during', 'possible', 'several', 'among',
                             'within', 'along', 'above', 'across', 'together', 'about', 'yet', 'except'}

    black_punctuations = {'_', '~', '^', '"', '#', '%', ':', '?', '`', '>', '$', '@', '*', '!', '&', ';', '|', '<',
                          '\\', '=', '/', '°', '”', '“', '？', '•', '●', '®', '☆', '…', '¿', '􀏐'}

    black_head_tail_punctuations = {',', '‐', '–', '-', '—', '-', '+', "'"}

    black_pos = {'CC', 'IN', 'PRP', 'PRP$', 'DT', 'TO', 'UH', 'WDT', 'WP', 'WP$', 'WRB'}

    def __init__(self, terms):
        self.terms = terms

    def _has_invalid_char(self):
        """
        指定白名单字符域
        """
        import re
        terms = set()
        pattern = re.compile(Filter.white_char_pattern)
        for term in self.terms:
            res = pattern.search(term)
            if not res or len(res.group(0)) != len(term):
                # print(term)
                continue

            terms.add(term)

        self.terms = terms

    def _has_black_words(self):
        """
        只要包含这些单词，直接丢弃
        不仅是空格分割包含，还要加上 横线word、 中文
        """

        def has_chinese(strs):
            for _char in strs:
                if '\u4e00' <= _char <= '\u9fa5':  # 中文
                    return True
            return False

        def has_black_word_by_seg(term, seg):
            splits = term.split(seg)
            for black_word in Filter.black_words:
                for word in splits:
                    if black_word == word:
                        return True
            return False

        terms = set()
        for term in self.terms:
            if has_chinese(term):
                continue

            if has_black_word_by_seg(term, " "):
                continue

            if ", " in term:
                continue

            if "; " in term or ",etc" in term:
                continue

            should_drop = False
            for seg in Filter.black_head_tail_punctuations:
                if has_black_word_by_seg(term, seg):  # 以-,—等后面接常见词的情况，都删除
                    should_drop = True
                    break

            if should_drop:
                continue

            terms.add(term)

        self.terms = terms

    def _has_black_punctuations(self):
        """
        只要包含这些不合理字符，直接丢弃
        """
        terms = set()
        for term in self.terms:
            should_drop = False
            for black_punc in Filter.black_punctuations:
                if black_punc in term:
                    should_drop = True
                    break
            if should_drop:
                continue

            terms.add(term)

        self.terms = terms

    def _has_black_head_tail(self):
        """
        开头结尾的词或字符不合理
        """
        terms = set()
        for term in self.terms:
            if term.endswith("\'s"):
                continue

            if term[0] in Filter.black_head_tail_punctuations or term[-1] in Filter.black_head_tail_punctuations:
                continue

            splits = term.split(" ")
            if splits[0] in Filter.black_head_tail_words or splits[-1] in Filter.black_head_tail_words:
                continue

            should_drop = False
            for seg in Filter.black_head_tail_punctuations:
                splits = term.split(seg)
                if splits[0] in Filter.black_head_tail_words or splits[-1] in Filter.black_head_tail_words:
                    should_drop = True
                    break
            if should_drop:
                continue

            terms.add(term)

        self.terms = terms

    def _has_odd_brackets(self):
        """
        包含奇数个括弧
        """

        def check_brackets(s):
            brackets = {'}': '{', ')': '(', ']': '['}
            bracket_left, bracket_right = brackets.values(), brackets.keys()
            arr = []
            for c in s:
                if c in bracket_left:
                    # 左括号入栈
                    arr.append(c)
                elif c in bracket_right:
                    # 右括号，要么栈顶元素出栈，要么匹配失败
                    if arr and arr[-1] == brackets[c]:
                        arr.pop()
                    else:
                        return False
            return not arr

        terms = set()
        for term in self.terms:
            if not check_brackets(term):
                continue

            terms.add(term)

        self.terms = terms

    def _has_dot(self):
        """
        含有不合理的点号
        """
        terms = set()
        for term in self.terms:
            if term[0] == '.' or term[-1] == '.':
                continue

            should_drop = False
            if len(term) >= 3:
                for idx in range(len(term)):
                    if term[idx] == '.':
                        if not term[idx - 1].isdigit() or not term[idx + 1].isdigit():
                            should_drop = True
                            break
            if should_drop:
                continue

            terms.add(term)

        self.terms = terms

    def _high_trieCnt_of_pedCnt(self):
        """
        过滤在预测集中匹配频数/预测频数 大于 10 的术语
        """

        def get_drop_terms():
            RATIO = 10
            drop_terms = set()
            with open("debug_compare_v1_new_terms_tf.txt", 'r') as r:
                _ = r.readline()
                for line in r:
                    _, trie_cnt, pred_cnt, term = line.rstrip("\n").split("\t")
                    if int(trie_cnt) / int(pred_cnt) >= RATIO:
                        drop_terms.add(term)
            # print("trieCnt/predCnt 比值过大的术语数 ", len(drop_terms))   #  209769个,总数2333097

            return drop_terms

        drop_terms = get_drop_terms()
        terms = set()
        for term in self.terms:
            if term in drop_terms:
                continue

            terms.add(term)

        self.terms = terms

    def _invalid_pos(self):
        """ 使用nltk判断词性"""
        import nltk
        terms = set()
        for term in self.terms:
            splits = term.split(" ")
            if len(splits) <= 2:
                tags = nltk.pos_tag(splits)
                should_drop = True
                for _, tag in tags:
                    if tag not in Filter.black_pos:
                        should_drop = False
                        break
                if should_drop:
                    continue

            terms.add(term)

        self.terms = terms

    def _invalid_length(self):
        """不合理长度"""
        terms = set()
        for term in self.terms:
            if len(term) >= 80 or len(term) <= 2:
                continue
            terms.add(term)

        self.terms = terms

    def _all_digits_or_punc(self):
        """
        全由数字和特殊字符构成
        """
        terms = set()
        for term in self.terms:
            should_drop = True
            for _char in term:
                if _char.isalpha():
                    should_drop = False
                    break
            if should_drop:
                continue

            terms.add(term)

        self.terms = terms

    def filter(self):
        # 0. 先过滤指定字符域
        print("初始术语个数 ", len(self.terms))
        cnt1 = len(self.terms)
        self._has_invalid_char()
        print("过滤非法字符域，当前术语个数 ", len(self.terms), " 过滤了 ", cnt1 - len(self.terms))

        # 1. 过滤长度
        cnt1 = len(self.terms)
        self._invalid_length()
        print("过滤非法长度，当前术语个数 ", len(self.terms), " 过滤了 ", cnt1 - len(self.terms))

        # 2. 过滤非法单词
        cnt1 = len(self.terms)
        self._has_black_words()
        print("过滤非法单词，当前术语个数 ", len(self.terms), " 过滤了 ", cnt1 - len(self.terms))

        # 3. 过滤非法字符
        cnt1 = len(self.terms)
        self._has_black_punctuations()
        print("过滤非法字符，当前术语个数 ", len(self.terms), " 过滤了 ", cnt1 - len(self.terms))

        # 4. 过滤开头结尾
        cnt1 = len(self.terms)
        self._has_black_head_tail()
        print("过滤非法开头结尾，当前术语个数 ", len(self.terms), " 过滤了 ", cnt1 - len(self.terms))

        # 5. 过滤不匹配的括号
        cnt1 = len(self.terms)
        self._has_odd_brackets()
        print("过滤不匹配的括号，当前术语个数 ", len(self.terms), " 过滤了 ", cnt1 - len(self.terms))

        # 6. 过滤不合理的点
        cnt1 = len(self.terms)
        self._has_dot()
        print("过滤不合理的点号，当前术语个数 ", len(self.terms), " 过滤了 ", cnt1 - len(self.terms))

        # 7. 过滤trieCnt/predCnt比例过高
        # cnt1 = len(self.terms)
        # self._high_trieCnt_of_pedCnt()
        # print("过滤trieCnt/predCnt比例过高，当前术语个数 ", len(self.terms), " 过滤了 ", cnt1 - len(self.terms))

        # 8. 过滤不合理词性组合
        # cnt1 = len(self.terms)
        # self._invalid_pos()   #  情况很少见
        # print("过滤不合理词性组合，当前术语个数 ", len(self.terms), " 过滤了 ", cnt1 - len(self.terms))

        # 9. 全是数字或符号
        cnt1 = len(self.terms)
        self._all_digits_or_punc()
        print("过滤全是数字和符号的术语，当前术语个数 ", len(self.terms), " 过滤了 ", cnt1 - len(self.terms))

        return self.terms


if __name__ == '__main__':
    cleanterms_path = 'otherterms.txt'
    terms = set()
    with open(cleanterms_path, 'r') as r:
        _ = r.readline()
        for line in r:
            term = line.split('\t')[1]
            terms.add(str(term))

    raw_terms = terms

    filter = Filter(terms)

    cleaned_terms = filter.filter()

    with open(cleanterms_path, 'r') as r:
        with open(cleanterms_path[:-4] + "_cleaned.txt", 'w') as w:
            w.write(r.readline())
            for line in r:
                term = line.split('\t')[1]
                if term in cleaned_terms:
                    w.write(line)

    print("dump over!")

