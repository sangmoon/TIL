import sys

def solution(A):
    if len(A) == 2:
        return 0
    
    minSliceTwo = A[0] + A[1]
    minSliceTwoIdx = 0
    
    minSliceThree = sys.maxsize
    minSliceThreeIdx = 0
    for i, num in enumerate(A, start=2):
        if i == len(A):
            break;
        
        sliceTwo = A[i-1] + A[i]
        (minSliceTwo, minSliceTwoIdx) = (sliceTwo, i-1) if sliceTwo < minSliceTwo else (minSliceTwo, minSliceTwoIdx)
        
        sliceThree = A[i-2] + A[i-1] + A[i]
        (minSliceThree, minSliceThreeIdx) = (sliceThree, i-2) if sliceThree < minSliceThree else (minSliceThree, minSliceThreeIdx)

    if minSliceThree * 2 == minSliceTwo *3:
        return min(minSliceTwoIdx, minSliceThreeIdx)
        
    else:
        return minSliceTwoIdx if minSliceThree * 2 > minSliceTwo * 3 else minSliceThreeIdx
        