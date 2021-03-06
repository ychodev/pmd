\@label(chapter: 1)

### 코드 실행

``` python \@linenum 
print("안녕하세요. 첫 번째 파이썬 프로그램입니다.")
print('안녕하세요. 첫 번째 파이썬 프로그램입니다.')
print("안녕하세요. 첫 번째 파이썬 프로그램입니다.")
print('안녕하세요. 첫 번째 파이썬 프로그램입니다.')
print("안녕하세요. 첫 번째 파이썬 프로그램입니다.")
print('안녕하세요. 첫 번째 파이썬 프로그램입니다.')
print("안녕하세요. 첫 번째 파이썬 프로그램입니다.")
print('안녕하세요. 첫 번째 파이썬 프로그램입니다.')
print("안녕하세요. 첫 번째 파이썬 프로그램입니다.")
print('안녕하세요. 첫 번째 파이썬 프로그램입니다.')
print("안녕하세요. 첫 번째 파이썬 프로그램입니다.")
print('안녕하세요. 첫 번째 파이썬 프로그램입니다.')
print("안녕하세요. 첫 번째 파이썬 프로그램입니다.")
print('안녕하세요. 첫 번째 파이썬 프로그램입니다.')
print("안녕하세요. 첫 번째 파이썬 프로그램입니다.")
print('안녕하세요. 첫 번째 파이썬 프로그램입니다.')
print("안녕하세요. 첫 번째 파이썬 프로그램입니다.")
print('안녕하세요. 첫 번째 파이썬 프로그램입니다.')
```

\@ref(fig:img_execution)은 고급 프로그래밍 언어를 이용해서 작성한 프로그램을 실행시키는 방법을 보인다. 사람이 이해하기 쉽게 만들어진 프로그래밍 언어를 컴퓨터가 이해할 수 있는 기계어로 변환시켜야 한다. 기계어는 일반적으로 컴퓨터의 프로세서에서 실행시킬 수 있는 이진 코드 형태로 만들어진 언어를 의미한다. 하지만 언어에 따라서는 소프트웨어로 만들어진 가상의 컴퓨터에서 실행시킬 수 있는 독자적인 언어인 경우도 있다. 하지만 이 경우에도 일반적으로 사람보다는 컴퓨터에 좀 더 친화적인 언어이므로, 직접 사람이 이러한 언어로 프로그램을 작성하는 일은 거의 없다. 

![\@label(fig:img_execution) 고급 프로그래밍 언어로 작성한 프로그램을 실행하는 방법](figures/01/Execution.png)

> 더 알아보기: 키워드
> 키워드는 파이썬 언어에서 특정 목적을 위해서 사용하기 위해 지정한 단어들이다. 파이썬의 키워드는 \@ref(table: keyword)에 보인 것과 같다. 

\@label(table: keyword) 키워드 
> | 키워드 | 키워드 | 키워드 | 키워드 | 키워드 | 키워드 |
> | --- | --- | --- | --- | --- | --- |
> | False | None | True | and | as | assert |
> | async | await | break | class | continue | def |
> | del | elif | else | except | finally | for |
> | from | global | if | import | in | is | 
> | lambda | nonlocal | not | or | pass | raise |
> | return | try | while | with | yield | |

### print() 명령과 문자열

print() 명령에 전달된 \"안녕하세요 ... 프로그램입니다.\"을 파이썬에서는 문자열이라고 부른다. 문자열에 대해서는 자료형을 다룰 때 다시 설명하겠지만, 파이썬 코드에서는 두 개 따옴표를 붙여서 표시한다. 이때 같은 종류만 사용한다면, 큰 따옴표와 작은 따옴표 모두 문자열을 표현할 때 사용할 수 있다. 예를 들어 \@ref(code: first_program) 는 동일한 출력 내용을 보인다. 

\@label(code: first_program) 
```
print("안녕하세요. 첫 번째 파이썬 프로그램입니다.")
print('안녕하세요. 첫 번째 파이썬 프로그램입니다.')
```

``` \@linenum  
print("안녕하세요. 첫 번째 파이썬 프로그램입니다.")
print('안녕하세요. 첫 번째 파이썬 프로그램입니다.')
```

