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

def anotherSolution(S, P, Q):
    preSum = [[0 for i in range(len(S) + 1)] for j in range(4)] # preSum = [3][N]
    result = []
    
    for char , idx in enumerate(S):
        deltaA = 0
        deltaC = 0
        deltaG = 0
        deltaT = 0
        if char == "A":
            deltaA = 1
        elif char == "C":
            deltaC = 1
        elif char == "G":
            deltaG = 1
        else:
            deltaT = 1
        
        preSum[0][i+1] = preSum[0][i] + deltaA
        preSum[1][i+1] = preSum[1][i] + deltaC
        preSum[2][i+1] = preSum[2][i] + deltaG
        preSum[3][i+1] = preSum[3][i] + deltaT

    for start, end in zip(P, Q):
        if preSum[0][end+1] - preSum[0][start] > 0:
            result.append(1)
        elif preSum[1][end+1] - preSum[1][start] > 0:
            result.append(2)
        elif preSum[2][end+1] - preSum[2][start] > 0:
            result.append(3)
        else:
            result.append(4)