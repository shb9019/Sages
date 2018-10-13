def fn(a,b):
    print(a-b)
line = list(map(int, input().split(' ')))
fn(*line)
