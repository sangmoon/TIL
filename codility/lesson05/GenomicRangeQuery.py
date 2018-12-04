def score(s):
    if 'A' in s:
        return 1
    elif 'C' in s:
        return 2
    elif 'G' in s:
        return 3
    else:
        return 4

def solution(S, P, Q):
    ans = []
    for start, end in zip(P,Q):
        ans.append(score(S[start:end+1]))
    return ans