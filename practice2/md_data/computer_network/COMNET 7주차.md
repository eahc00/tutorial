참고 : https://ideadummy.tistory.com/112 ㅈㅈㅎ 블로그

# Chapter 6 : Introduction To Data-Link Layer
## Chapter 5 : Objective
### first section : data-link layer
- link와 node의 개념을 정의한다.
- data-link layer에서 제공하는 service를 나열하고 간략하게 설명한다.
- link의 두 가지 범주에 대해 정의한다.
	- point-to-point link : 둘만 연결
	- broadcast link : 여러명 연결
- 다음 몇 chapter에서 자세히 설명할 data-link layer에서 두 개의 하위 레이어를 정의한다.

### second section : link-layer addressing
- 데이터 링크 계층에 addressing 매커니즘이 존재하는 근거를 설명한다.
- (세 가지 유형의 링크 계층 주소에 대해 설명한다.)
- network layer에서의 주소와 data-link layer에서의 주소를 mapping해주는 Address Resolution Protocol(ARP)에 대해 설명한다.


## Introduction
- Internet은 (라우터 또는 스위치와 같은) 연결 장치를 통해 서로 연결된 네트워크의 조합이다.
- 패킷이 한 호스트에서 다른 호스트로 이동하려면 이러한 네트워크를 통과해야 한다.

## Communication at The Data-link Layer
- 자기 네트워크 안에 있는 통신을 관리
- **내부에서의 통신**을 효율적으로 관리

### Nodes and Links
- data-link layer에서의 통신은 node-to-node(노드간 통신)이다. 데이터 unit은 Internet에 한 point에서부터 다른 point에 도달하기 위해 많은 네트워크(LAN과 WAN)을 통과해야 한다.
- 이러한 LAN들과 WAN들은 router에 의해 연결돼있다. 
- 두 개의 **end host와 router를 노드**라고 하고 **그 사이의 네트워크를 link**라고 하는 게 일반적이다.
	![[Pasted image 20240416132359.png|500]]

![[Pasted image 20240416132439.png|500]]
- 위 사진에 Link : of type 1, Link :of type 2의 link type은 변할 수 있지만 Datagram은 변하지 않는다.

> [!my_question]
> data-link header가 바뀌는 거??  
> -> ㅇㅇ. 이건 라우터 지나면서 항상 바뀌는 거.  
> 링크 타입이 뭔데?  
> -> 잘 모르겠는데 이더넷 같이 데이터 링크 계층에서 쓰이는 프로토콜이 바뀔 수 있다는 의미 같음.




### Two categories of Links
- 두 노드가 케이블이나 air(무선)과 같은 전송 매체(medium)로 물리적으로 연결되어 있더라도, 데이터 링크 계층이 **매체 사용 방식을 제어** 한다는 점을 기억해야 한다.
- 매체의 전체 용량을 사용하는 데이터 링크 계층을 가질수도, 링크 용량의 일부만 사용하는 데이터 링크 계층을 가질 수도 있다.
- 즉, point-to-point link 또는 broadcast link가 있을 수 있다.

#### Two Sublayers
- 링크 계층의 기능과 링크 계층이 제공하는 서비스를 더 잘 이해하기 위해 데이터 링크 계층을 Data Link Control(**DLC**)과 Media Access Control(**MAC**)라는 두 가지 하위 계층으로 나눌 수 있다.
- LAN 프로토콜은 실제로 동일한 전략을 사용하기 때문에 이는 드문일이 아니다.
	![[Pasted image 20240416141624.png]]
	- *a. broadcast link* : 여러 명이 동시에 쓰기 때문에 데이터 충돌이 발생할 수 있다 -> 이게 노이즈처럼 인식된다. 따라서 **누가 지금 데이터를 보내야 하는지**가 추가적으로 필요하다.
	- *b. Data-link layer of a point-to-point link* : 둘만 연결돼있기 때문에 broadcast link에서 발생하는 문제를 고려할 필요가 없다.


### Link Layer Address
- IP 주소 : 네트워크 계층의 식별자
- Internet과 같은 내부 네트워크(internetwork)에서는 IP 주소만으로는 데이터그램을 목적지에 도달시킬 수 없다.
- source와 destination의 IP 주소는 양쪽 end를 정의하지만 패킷이 통과해야 하는 링크를 정의할 수 없다.
	![[Pasted image 20240416150038.png]]
	- **네트워크 내부에서 사용하는 주소**가 필요 : **Link-layer address**
		-> 네트워크가 바뀔 때마다 주소가 바뀐다.
	- IP address는 송신자에게 데이터가 전송될 때까지 변하지 않는다.(바뀌면 안된다.)


## Address Resolution Protocol(ARP)
- 노드가 링크에서 다른 노드로 전송할 IP datagram이 있을 때마다, 그것은 수신 노드의 IP 주소를 가진다.
- 그러나 다음 노드의 IP는 링크를 통해 프레임을 이동하는 데에 도움이 되지 않는다; **다음 노드의 link layer 주소**가 필요하다.
- 이때 **Address Resolution Protocol(ARP)** 이 유용하게 사용된다.
	![[Pasted image 20240416150825.png]]

> [!abstract]
> IP 주소를 가지고 Link-layer address를 자동으로 찾아줌. 이게 ARP이다.


### ARP Operation
- Request : destination IP address를 가지고 link-layer address를 찾는 것.
	- Request를 보낼때는 해당하는 IP가 누군지 모르므로 broadcast로.
- Reply : destination IP address와 일치하는 노드의 **link-layer address를 Reply.**
	- Reply할 때는 받은 ARP헤더의 source IP를 보고 1:1 전송으로 응답.
	![[Pasted image 20240416152845.png]]

### ARP Packet
![[Pasted image 20240416154208.png]]
- Operation 
	- 1은 요청, 2는 응답이다 -> 번호로 구분
- Source hardware address, Source protocol address : 자기(송신자)의 것
- **Destination hardward address** : 찾으려 하는 것. 요청 보낼 때는 비어있다.
- **Destrination protocol address** : 수신자는 이걸 보고 자신의 IP address와 같으면 link layer 주소로 응답.

- Example
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240422190010.png|400]]

### ARP Example
- IP 주소가 N1이고, MAC 주소가 L1인 호스트가 IP 주소가 N2이고 물리적 주소가 L2인 다른 호스트(첫 번째 호스트는 알수 없음)에게 보낼 패킷이 있다. 두 호스트는 동일한 네트워크에 있다.
	![[Pasted image 20240416155946.png]]

![[Pasted image 20240416160112.png]]
- Alice는 R1 router에게 ARP 요청 -> R1은 R2에게 ARP요청 -> R2는 bob에게 ARP 요청
- 만약 alice와 bob이 같은 network에 있으면 alice가 bob한테 바로 ARP를 요청해서 link layer를 받아 데이터 전송을 하면 된다.

#### Alice의 컴퓨터에서 패킷 flow
![[Pasted image 20240416160252.png|550]]

#### R1 router에서 패킷 flow
![[Pasted image 20240416160310.png|550]]

#### R2 router에서 packet flow
![[Pasted image 20240416160328.png|550]]

#### Bob의 컴퓨터에서 packet flow
![[Pasted image 20240416160349.png|300]]

### Unsolicated ARP Reply : 요청하지 않은 ARP Reply
- 모든 시스템이 ARP 요청에 대한 응답을 spoof할 수 있다.

> [!definition]
> **spoofing(스푸핑)**  
>  다른사람의 컴퓨터 시스템에 접근할 목적으로 ip주소를 변조한 후 합법적인 사용자인 것처럼 위장하여 시스템에 접근함으로써 나중에 ip주소에 대한 추적을 피하는 해킹 기법의 일종

- 수신 시스템이 응답을 캐시한다.
	- 기존 항목을 덮어쓴다.
	- 항목이 없는 경우 항목 추가
- 일반적으로 ARP poisoning이라고 한다.

> [!abstract]
> 보안적으로 취약.  
> IP address가 같지 않은 다른 네트워크가 응답하면?  
> -> 다른 주소로 보냄



# Chapter 7 : Error Detection and Correction
## Chapter 7 : Objective

- first section : types of error
	- redundancy의 개념과 error detection과 correction의 차이를 구별한다.
- second section : block coding
	- block coding을 이용하여 어떻게 에러를 검출하는지 보이고 Hamming distance의 개념을 소개한다.
- third section : cyclic codes
	- 데이터 링크 계층에서 매우 일반적인 cyclic code의 하위 집합은 CRC에 대해 설명한다. 
	- 이 섹션에서는 CRC를 하드웨어에서 쉽게 구현하고 다항식으로 표현할 수 있는 방법을 보인다.
- fourth section : checksums
	- checksum이 data word의 집합에 대해 계산되는 방식을 보인다.
	- 또한 전통적인 checksum(tranditional)에 대한 몇몇 다른 접근을 준다.
- fifth sector : foward error connection
	- Hamming distance가 이러한 목적으로 이용될 수 있는 방식을 보인다.
	- 또한 패킷의 XORing, interleaving chunks 혹은 compounding high and low resolution packet과 같은 방법으로 더 저렵하게 같은 목적을 달성할 수 있음을 설명한다.


## Types of Errors 
- 비트가 한 point에서 다른 point로 이동할 떄마다 간섭(interference)으로 인해 예측할 수 없는 변화가 일어날 수 있다.. 이러한 간섭은 신호의 모양을 바꿀 수 있다.
- **single-bit error**는 주어진 data unit(데이터 단위, 예 : 바이트, 문자 또는 패킷)의 **한 비트**가 1에서 0으로 또는 0에서 1로 변경되는 것을 의미한다.
- **burst 에러**라는 단어는 데이터 단위에서 **2개 이상의 비트**가 1에서 0으로 또는 0에서 1로 변경된 것을 의미한다.

### Single vs Bursty Error
![[Pasted image 20240416200458.png]]

## Redundancy
- 에러 검출 및 수정(detecting and correcting errors)의 중심 개념이다.
- 에러를 검출 및 수정을 가능하게 하기 위해, 데이터에 몇몇 여분의 비트를 보내야 한다. 이러한 **redundant bits(r bit)** 는 송신자에 의해 추가되고 수신자에 의해 제거된다.
- r bit의 존재는 수신자가 손상된 bit들을 검출하고 수정하게 해준다.

> [!tip]
> detection 후 correction를 하지 않으면 어떻게?  
> -> 에러가 있는 데이터면 그냥 버리고 아니면 r bit를 제외한 데이터만 뽑아낸다.


## Detection and Correction
- 에러의 수정은 검출보다 더 어렵다. 에러 검출에서는 단지 에러가 발생했는지만 보면 된다. 그 답은  간단한 yes or no 이다. 심지어 손상된 비트의 수조차 신경쓰지 않아도 된다. single-bit error와 burst-bit error와 우리에게는 똑같은 것이다.
- 에러 수정에서, 손상된 비트의 정확한 수를 알아야 한다. 더 중요한 것은 message에서 손상된 비트의 위치이다.

## Coding
- Redundancy는 다양한 coding schemes로 달성된다.
- 송신자는 redundant bit와 실제 데이터 비트 간의 관계를 생성하는 프로세스를 통해 r(Redundant) 비트를 추가한다.
- 수신자는 두 비트 집합 간의 관계를 확인하여 오류를 검출한다.
- 데이터 비트에 대한 redundant bit의 비율과 프로세스의 robustness는 모든 coding scheme에서 중요한 요소이다.

## Block Coding
- Block coding에서, 메세지를 dataword라고 불리는 각 k bit으로 구성되는 block으로 나눈다.
- 길이를 n  = k + r 으로 만들도록 r redundant bit를 각각의 블록에 추가한다.
- 결과인 n-bit blocks을 codeword라고 부른다.
- 여분의 r비트가 선택되거나 계산되는 방식

### Error Detection
- 어떻게 block coding을 사용함으로써 오류가 검출될 수 있나? 만약 다음의 두 조건이 만나면, 송신자는 기존의 codeword에서 변화를 검출할 수 있다.
	1. 수신자는 **유효한 codeword들의 리스트**를 가진다(혹은 찾을 수 있다).
	2. 기존의 codeword가 유효하지 않은 codeword를 가진다.

	![[Pasted image 20240416203332.png]]
	- Sender의 Generator는 r bit를 생성한다.
	- 이후 k bits의 Dataword와 생성된 r bit를 더하여 n bits의 Codeword를 구성하고 전송한다.
	- Receiver는 Codeword를 받아 Checker에서 Error를 검출한다. 만약 Error가 검출되면 폐기하고 아니면 Dataword를 추출한다.

#### Example
![[Pasted image 20240416203651.png]]
- sender가 dataword 01을 011로 Encoding하고 그것을 receiver에게 보낸다고 가정하다. 이어지는 경우를 고려해보자:
	 1. 수신자가 011을 받는다. 이것은 유효한 codeword이다.  수신자는 이것으로부터 dataword 01을 추출한다.
	 2. codeword가 전송 중에 손상되고, 111을 받는다(가장 왼쪽의 bit가 손상됨). 이것은 유효한 codeword가 아니므로 폐기한다.
	 3. codeoword가 전송 중에 손상되고, 000을 받는다(오른쪽의 두 비트가 손상됨). 이것은 유효한 codeword이다. 수신자는 올바르지 않은 dataword 00을 뽑아낸다. 두 개의 손상된 비트들은 error가 검출되지 못하게 만든다.

> [!summary]
> 만약 중간에 바뀌어서 111이 된다면? -> 오류 검출  
> 근데 어쩌다가 codeword에 존재하는 것으로 바뀐다면? -> 오류 검출 불가능


### Simple Parity Bit
- 1의 개수를 짝수 개로 맞춰준다.
	![[Pasted image 20240416204047.png]]

	![[Pasted image 20240416204116.png]]
- Generator
	- $r = (a_0 + a_1 + a_2 + a_3)  \% 2$ 로 생성하여 parity bit로 dataword에 붙여서 codeword 전달
- Checker
	- $s_0 = (b_3 + b_2 + b_1 + b_0 + q_0)\%2$을 검사하여 0이 아니면 오류. -> 폐기

#### Example
- 일부 전송 시나리오를 살펴보자. 송신자가 dataword 1011을 보낸다고 가정한다. 수신자에게 전송 될 dataword로부터 생성된 codeword는 10111이다. 우리는 다섯가지 경우를 검사한다.
	1. 어떤 에러도 발생하지 않음; 수신된 codeword가 10111이다. syndrome은 0이다. dataword 1011이 생성된다.
	2. 하나의 single_bit 에러가 $a_1$을 바꾼다. 수신된 codeword는 10011이다. styndrome은 1이다(에러 검출). 어떤 dataword도 생성되지 않는다.
	3. 하나의 single-bit error가 $r_0$(redundancy에 에러)을 바꾼다. 수신된 codeword는 10110이다.  어떤 dataword도 생성되지 않는다.  dataword 비트가 손상되지는 않았지만 코드가 손상된 비트의 위치를 보일만큼 정교하지 않기 때문에 dataword가 생성되지 않는다.
	4. 오류가 $r_0$을 변경하고 두 번째 오류가 $a_3$을 변경한다. 수신된 codeword는 00110d이다. syndrome은 0이다. dataword 0011은 수신자에서 생성된다. 여기서 dataword는 syndrome value로 인해 틀리게 생성되었다. simple parity-check decoder는 홀수 개의 에러를 검출하지 못한다. 에러는 서로 상쇄되어 syndrome의 값이 0이된다.
		-> 에러 검출 불가능
	5. 오류로 인해 세 개의 비트 $a_3, a_2, a_1$이 변경된다. 수신된 code word는 0101이다. syndrome은 1이다. dataword는 만들어지지 않는다. 이것은 one single error, 혹은 어떠한 홀수 개의 에러라도 simple parity check로 검출이 보장됨을 보인다.

	-> **짝수 번의 에러가 발생하면 검출 불가능.**

### Cyclic codes
- Cyclic code는 **하나의 추가(여분의) 속성**이 있는 특수한 linear block codes(선형 블록 코드)이다.
- 순환 코드에서 codeword가 주기적으로 이동(회전)하면 그 결과는 다른 codeword가 된다.
	- 예를 들어 1011000이 코드워드이고 cyclic하게 왼쪽으로 shift하면 0110001도 코드워드가 된다.

#### Cyclic Code with C(7, 4)
![[Pasted image 20240416214109.png]]


#### Cyclic Codes
![[Pasted image 20240416214144.png]]
- 데이터 길이 == divisior 길이
- **Divisor로 나눔.**
- Syndrome : 나머지가 0이 나오는지 검사

![[Pasted image 20240416214338.png]]
- Syndrome이 0이 아니면 오류

#### Advantage of Cyclic Codes
- cyclic code는 single-bit errors(단일 비트 오류), double errors(이중 오류), odd number of errors(홀수 오류) 및 burst 오류를 감지하는 데 매우 우수한 성능을 보인다.
- 하드웨어와 소프트웨어에서 쉽게 구현할 수 있다. 특히 하드웨어로 구현할 때 속도가 빠르다.
- 이 때문에 cyclic code는 많은 네트워크에 대하여 적합한 후보가 되었다.

> [!abstract]
> 여러 에러를 쉬운 구현으로 검출 가능


## Checksum
 - **어떠한 길이의 메세지에도 적용**될 수 있는 오류 검출 기술이다. 
 - Internet에서, 체크섬 기술은 대부분 data-link layer보다 network와 transport 계층에서 사용된다. 

![[Pasted image 20240416215202.png]]

### Traditional Checksum
- 메세지가 destination에 보내길 원하는 4-bit 수들의 목록 5개라고 가정한다.
- 이러한 수들을 보내는 것 이외에 추가로 수들의 합을 전송한다.
	- 예를 들어, 숫자 집합이 (7, 11, 12, 0, 6)인 경우 (7, 11, 12, 0, 6, **36**)을 보내면 여기서 36이 기존 숫자들의 합이다.
- 수신자는 다섯 개의 숫자를 더하고 그 결과를 합과 비교한다. 
	- 두 값이 같으면 수신자는 오류가 없는 것으로 간주하고 다섯 개의 수를 받고 합을 버린다.
	- 그렇지 않으면 어딘가에 오류가 있는 것으로 간주하고 메세지를 수락하지 않는다.

> [!warning]
> 오류가 나도 합이 맞으면 오류 검출이 불가능하다.  
> 합으로 계산하므로 추가되는 합의 비트 수가 커지는 문제가 생긴다.  
> ex) 위 예시에서 4-bit 수들을 보내는데 36은 4-bit의 최대인 15를 넘어버린다.


- 위 예시에서 10진수 36은 2진수로 $100100_2$ : 6비트이다.
- 이걸 4-bit 수로 바꾸기 위해 가장 왼쪽의 남는 비트를 오른쪽의 4비트들과 더한다.
	$$10_2 + 0100_2 = 0110_2 \rightarrow 6_{10}$$

- 합으로 36을 보내는 것 대신, 우리는 합으로 6을 보낼 수 있다 : (7, 11, 12, 0, 6, 6).
- 수신자는 1의 보수 연산으로 첫 다섯 숫자를 더할 수 있다.
- 만약 결과가 6이면, 수들은 수락되고 아니면 거절된다.

- 위에서 설명한 checksum의 아이다어를 사용해보자. 송신자 다섯 숫자를 1의 보수로 모두 더하여 합계 6을 얻는다.

> [!question]
> 뭐 어케 1의 보수 쓰라고요  
> -> 비트수 초과해서 올라간 거 다시 밑으로 더해주는 게 1의 보수로 연산하는 것

- 이후 송신자는 다시 결과에 보수를 취해 15 - 6인 체크섬 9를 얻는다.
- $6 = 0110_2$, $9 = 1001_2$는 서로의 보수이다.
- 송신자는 5개의 data number들과 체크섬(7, 11, 12, 0, 6, 9)을 전송한다.
- 전송에 손상이 없으면, 수신자는 (7, 11, 12, 0, 6, 9)를 수신하고 이를 자신의 보수에 더하여 15를 얻는다. 
	-> 이렇게 다 더해서 보수 취하면 0이 나오도록 검사한다.

![[Pasted image 20240416224940.png]]

> [!seealso]
> 다른 체크섬 방식  
> - 하나의 변화가 여러 체크섬의 변화가 되도록 한다. (조합으로 더해주고 또 그걸 더해줌.)  
> ex) 7 11 8이면 (7+11) + (11+8) = 37   
> 	 -> 데이터가 중복돼서 쓰이도록 checksum을 만든다.

### Enhanced Checksum - Fletcher's
![[Pasted image 20240416225404.png]]
- 체크섬은 16비트로 왼쪽(L) 8비트, 오른쪽(R) 8비트가 있다.
- 여기서 데이터가 추가될 때마다 (R + $D_i$)를 256으로 나눈 나머지를 R에 넣고 L은 (L + R)을 256로 나눈 나머지를 256으로 나눈 나머지가 된다.
- 보낼 데이터가 없으면 최종적으로 **checksum은 L x 256 + R**이 된다.


## Error Correction
#### Backward Error Correction
- Automatic Repeat request(ARQ)로도 알려져있음.
- 수신기(receiver)에서 송신기(transmitter)로의 피드백 사용 : receiver는 데이터 블록이 올바르게 수신되었는지 여부를 송신기에게 알린다(신호를 전달). 
- 수신이 잘못되면 전송이 반복된다.

> [!summary]
> 다시 뒤로 가서 에러를 고쳐온다.  
> 송신자에게 **재전송 요청**


### Forward Error Correction
- 오류 검출과 재전송에 대해서 이전 섹션에서 설명했다. 하지만 손상되거나 손실된 packet들의 재전송은 real-time multimedia transmission(실시간 멀티 미디어 전송)에 유용하지 않다. 즉시 오류를 수정하거나 패킷을 재생성해야 한다.

 > [!summary]
 > 오류를 직접 고친다.


####  Hamming Code
![[Pasted image 20240416231022.png]]

- **여러 조합을 이용하여 에러의 위치**를 찾아낸다. 1이 나오는 위치에 따라 에러가 결정된다.

##### Example
![[Pasted image 20240416231122.png]]
- 7이 들어간 곳은 다 문제가 생기고(1이 나옴) 7이 안 들어간 곳에 문제가 없다(0이 나옴).
	 -> 한 비트씩 빼서 조합을 만들고 검사한다.

#### interleaving
![[Pasted image 20240416231228.png]]
- 데이터를 **column by column으로 전송**하여 전송 중 packet이 하나 손실 되더라도 전체 패킷이 사라지지 않고 각 패킷에 하나만 손실되도록 한다.

#### Compound
- 또 다른 solution은 low-resolution(저해상도) redundancy(중복)으로 각 패킷의 복제본을 생성하고 중복 버전을 다음 패킷과 결합하는 것이다.

![[Pasted image 20240416231532.png]]
- 위 그림과 같이 손실된 패킷을 잘 도착한 다음 패킷에 있는 저해상도 복제 버전으로 대치할 수 있다.
- 고해상도 패킷 5개 중 저해상도 패킷 4개를 생성하여 전송할 수 있다.