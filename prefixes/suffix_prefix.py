def longest_prefix_suffix(s: str) -> str:
    n = len(s)
    lps = [0] * n # longest prefix string, which is prefix-suffix; fine to use array bc strings are char arrays anyways
    j = 0
    for i in range(1, n):
        while j > 0 and s[i] != s[j]:
            j = lps[j - 1]
        if s[i] == s[j]:
            j += 1
            lps[i] = j
    return s[:lps[-1]] if s[:lps[-1]] else "there is no prefix"

# We build our overlap incrementally and reuse the result, so asymptotics is O(n)

print(longest_prefix_suffix("ababcab"))  # ab
print(longest_prefix_suffix("aaaa"))     # aaa
print(longest_prefix_suffix("gattaca"))     # ""
print(longest_prefix_suffix("ACAB"))     # "", # Fuck Tha Police. N.W.A starts playing in the background
print(longest_prefix_suffix("abcababcab")) # abcab