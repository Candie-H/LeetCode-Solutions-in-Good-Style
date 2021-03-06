from typing import List
from collections import deque


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        size = len(s)
        # 题目中说非空字符串，以下 assert 一定通过
        assert size > 0

        # 预处理，把 wordDict 放进一个哈希表中
        word_set = {word for word in wordDict}
        # print(word_set)

        # 状态：以 s[i] 结尾
        # 这种状态定义很常见
        dp = [False for _ in range(size)]

        dp[0] = s[0] in word_set

        # print(dp)

        # 使用 r 表示右边界，可以取到
        # 使用 l 表示左边界，也可以取到
        for r in range(1, size):
            # Python 的语法，在切片的时候不包括右边界
            # 如果整个单词就直接在 word_set 中，直接返回就好了
            # 否则把单词做分割，挨个去判断
            if s[:r + 1] in word_set:
                dp[r] = True
                continue

            for l in range(r):
                # dp[l] 写在前面会更快一点，否则还要去切片，然后再放入 hash 表判重
                if dp[l] and s[l + 1: r + 1] in word_set:
                    dp[r] = True
                    # 这个 break 很重要，一旦得到 dp[r] = True ，循环不必再继续
                    break
        res = []
        # 如果有解，才有必要回溯
        if dp[-1]:
            queue = deque()

            self.__dfs(s, size - 1, wordDict, res, queue, dp)
        return res

    def __dfs(self, s, end, word_set, res, path, dp):
        # print('刚开始', s[:end + 1])
        # 如果不用拆分，整个单词就在 word_set 中就可以结算了
        if s[:end + 1] in word_set:
            path.appendleft(s[:end + 1])
            res.append(' '.join(path))
            path.popleft()

        for i in range(end):
            if dp[i]:
                suffix = s[i + 1:end + 1]
                if suffix in word_set:
                    path.appendleft(suffix)
                    self.__dfs(s, i, word_set, res, path, dp)
                    path.popleft()


if __name__ == '__main__':
    # s = "leetcode"
    # wordDict = ["leet", "code"]
    s = "pineapplepenapple"
    wordDict = ["apple", "pen", "applepen", "pine", "pineapple"]

    # s = "a"
    # wordDict = ["a"]
    solution = Solution()
    result = solution.wordBreak(s, wordDict)
    print(result)

    # ["pine apple pen apple","pineapple pen apple","pine applepen apple"]
