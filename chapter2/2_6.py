#람다 함수같은 것.
#한줄 형태로 넘겨줄 수 있음.
#attrs의 갯수가 두개인 것을 뽑는 것.

def plus(val_1, val_2):
    return val_1, val_2

#def val_1: val^2 (제곱)

#val_1 등이 매개변수임
#그런데 람다는
#tags = bsObj.findAll(lambda tag: len(tag.attrs) == 2)
#findall은 텍스트나 함수를 받을 수 있음.
#findall에다가

tagSrc=bs0bj.findAll("img")
#문서에서 img라는 테그가 true인 것.
#findall이 한줄 씩 꺼내서, 이터레이터 돌려서
#img인것만 쭉 뽑는 거야.
#img테그면 넣는 것.
#img인 테그를 검색 하는 것.

#원래 이렇게 쓰는 건데 함수를 넘겼잖아.
#lambda는 이렇게 이터레이터에 attributes가 2개면 넘기는 것.


def getIsTwice(tag):
    return len(element.attrs)==2

#바로 람다는 익명인 것.