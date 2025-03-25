# Chapter4 : Digital Transmission
## Chapter 4: Objective
- 첫 번째 섹션에서는 digital-to-digital conversion(반드시 인코딩 필요)에 대해 설명한다. Line coding은 디지털 데이터를 디지털 신호로 변환하기 위해 사용되곤 한다. 몇몇 보통의 스키마들을 설명한다. 이 섹션은 또한 디지털 데이터가 디지털 신호로 인코딩 되기 전 디지털 데이터에 여분의 bit(정보)를 만들어내기 위한 block coding을 설명한다.

- 두 번째 섹션에서는 analog-to-digital conversion에 대해 설명한다. Pulse Code Modulation은 analog signal을 샘플링 하는 데에 쓰이는 main method로 설명된다. Delta Modulation은 Pulse Code Modulation의 효율을 향상시키는 데 이용된다.

- 세 번째 섹션에서는 transmission mode에 대해 설명한다. 우리가 데이터를 디지털하게 전송하기 원할 때, 우리는 parallel(병렬적)과 serial(직렬적)에 대해 생각할 필요가 있다. parallel transmission에서, 우리는 한 번에 여러 비트를 전송한다; serial transmission에서 우리는 한 번에 한 비트를 전송한다.

## Digital-to-Digital Conversion
- 이전 챕터에서, 데이터와 신호에 대해 설명했다. 데이터는 디지털과 아날로그 둘 다 될 수 있고, 신호는 디지털 혹은 아닐로그가 될 수 있는 데이터를 표현한다. 
- 이 섹션에서, 우리는 **어떻게 디지털 시그널을 이용하여 디지털 데이터를 표현**할 수 있는지를 본다. conversion은 두 가지 기술 : line coding과 block coding을 포함한다.
- Line coding은 항상 요구되고; block coding은 요구 될 수도, 아닐 수도 있다.

### Line Coding
- **Line coding은 디지털 데이터를 디지털 신호로 converting하는 과정**이다.
	- Line coding은 **bit sequence를 디지털 신호로 변환**한다.
	- 송신자에서 디지털 데이터는 디지털 신호로 인코딩된다. 수신자에서, 디지털 신호를 디코딩함으로써 디지털 데이터를 재생성한다.
		![[Pasted image 20240404011857.png]]

#### Signal Element vs Data Elements
![[Pasted image 20240404204915.png]]
- **r**은 각각의 signal element에 의해 옮겨지는 data element의 수이다. $$r = \frac{data\space element}{signal \space element}$$
> [!tip]
> r은 클수록 좋다 : 한 신호로 많은 데이터를 전달 가능


#### Data Rate vs Signal Rate
- data rate는 1초에 보내지는 data element(bits)의 수(=초당 데이터 요소)를 뜻한다. 단위는 bits per second(bps)이다. -> 높이는 게 좋음. 
- signal rate는 1초에 보내지는 signal element의 수(=초당 신호 요소)를 뜻한다. 단위는 baud이다. -> 낮추는 게 좋음.
- 데이터 통신에서의 하나의 목표는 **data rate(N)을 높이는 반면 signal rate(S)를 낮추는 것**이다.
	 - data rate을 높이는 것은 전송 속도를 높인다; signal rate를 낮추는 것은 요구되는 대역폭(=bandwidth requirement)를 낮춘다.
	 - 차량과 사람을 비유하자면, 교통 체증을 방지하지 위해 더 적은 수의 차량에 더 많은 사람을 태워야한다. 우리의 교통 시스템에는 제한된 대역폭이 있다.
	- $S = B_{min} = N/r$ (최소로 요구되는 대역폭)

#### Issues in Line Coding
- **DC Components**
	- digital signal의 voltage level이 일정하게 유지되면 스펙트럼(교류)은 매우 낮은 주파수(저주파)를 생성한다. DC(직류) component라고 하는 0 근처의 이러한 주파수는 저주파를 통과할 수 없는 시스템이나 변압기를 통해 전기적 결합을 사용하는 시스템에 문제를 일으킨다.
		- **constant 하면 안됨**
		- 특정 주파수 영역을 통과하지 못함
	- 기준선 문제 : signal의 평균 전압(amplitude)이 0이 아닌 경우, 해당 signal은 DC component 문제를 가진다.
		- **신호 세기의 평균이 0이 아닌 경우**
		![[Pasted image 20240404222438.png]]기준선 문제가 있는 신호(a)와 없는 신호(b)

- **Self-synchronization**
	- 신호의 모양을 가지고 synchronization을 맞춰줄 수 있을까?
	- seif-synchronizing digital signal은 전송되는 데이터에 timing information이 포함된다. 이는 수신자에 pulse의 시작, 중간, 혹은 끝을 알려주는 **신호의 transition(전환)** 이 있는 경우 달성할 수 있다. 수신자의 clock이 동기화 상태인 경우, 이러한 지점에서 clock을 reset할 수 있다


#### Line Coding의 종류
![[Pasted image 20240404222914.png]]

#### Unipolar : Non-Return-to-Zero(NRZ)
![[Pasted image 20240404231121.png]]
> [!note]
> **Unipolar : Positive voltage(양의 전압)만 사용**한다.\
> **NRZ : 비트의 중간에 0으로 돌아가지 않는다.**

- Positive voltage는 bit 1로 정의하고, zero voltage는 bit 0으로 정의한다.
	- Voltage(전압)는 시간 축의 한 쪽에 존재한다.
- NRZ는 bit의 중간에서 signal이 0으로 돌아가지 않는 것을 의미한다.
- 비용이 많이 든다. 지금의 데이터 통신에서는 사용되지 않는다.

> [!attention]
>  DC components(O) \
>  Self-synchronization(X)  \
>  r = 1

#### Polar : Non-Return-to-Zero(NRZ)
![[Pasted image 20240404231812.png]]
> [!note]
> **Polar : 양의 전압, 음의 전압을 모두 사용**

- polar scheme에서, 시간축의 양 쪽에 voltage가 모두 존재한다
	- 0에 대한 Voltage level은 positive가 될 수 있고 1에 대한 voltage level은 negative가 될 수 있다.

- NRZ-L에서 0들이나 1들의 long sequence가 있다면, 평균 signal power는 skew(왜곡)된다. -> **DC component**
	- Average 문제는 해결(음, 양의 전압을 모두 사용하므로) 

- NRZ - I에서도 Average 문제는 해결 -> but 0이 이어질 때 constant하므로 DC component 문제가 생긴다. 1이 이어지는 것은 계속 신호가 바뀌므로 문제가 생기지 않음.
	- 따라서 0들의 long sequence에 대해서만 DC components 문제가 발생한다. 

> [!attention]
> DC components (O) \
 > Self-synchronization(X) \
 > r = 1
 


#### Polar : Return-to-Zero(RZ)
![[Pasted image 20240404233805.png]]
- Polar Scheme

- **RZ(Return-to-Zero)**
	- Signal은 비트들 사이에서는 변하지 않지만 **비트 중간에 변한다.**
	- 중간에 zero로 돌아가므로 constant하지 않고 (average가 0이다.) -> DC components 해결
	- +, -의 amplitude에서 시작해서 0이었다가 -, +로 바뀌는 데에서 끝난다. -> Self-synchronization 가능
	- RZ encoding의 주요한 단점은 **한 비트를 인코딩하기 위해 두 번의 신호 변화가 요구** 된다는 것(r이 작음)이다. 따라서 **더 큰 bandwidth를 사용**(점유)하게 된다. 
	 - 근데 이건 신호 2개당 한 비트를 보낸다(r = 1/2). 큰 bandwidth필요.
	 - RZ는 생성하거나 식별하기에 더 복잡한 세 단계의 전압을 사용한다.

> [!attention]
> DC components(X) \
> Self-synchronization(O) \
> r = 1/2


#### Polar: Manchester and Differential Manchester
![[Pasted image 20240404235329.png]]
##### Biphase
- **Manchester**
	- RZ(bit의 중간에 transition(전환)한다)와 NRZ-L의 아이디어가 결합됨.
	- 전압은 처음 반(first half) 동안 한 레벨에서 유지(remain)되고 다음 반(second half)에 다른 레벨로 이동한다. 비트 중간에서의 전환은 synchronization을 제공합니다.
	
- **Diffrential Manchester**
	- RZ와 NRZ-I의 아이디어를 결합
	- 비트의 증간에서 항상 전환이 있지만, 비트 값은 비트의 시작에서 결정된다. 만약 다음 비트가 0이면 전환이 있고, 다음 비트가 1이면 전환이 없다.

- 장점
	- Manchester scheme는 NRZ-L에 연관된 몇몇 문제를 극복하고, differential Manchester는 NRZ-I와 연관된 몇몇 문제를 극본한다.
	- 각각의 비트가 positve와 negative voltage contribution(기여)를 가지므로 DC component 문제가 없다.

> [!attention]
> DC components(X) \
> Self-synchronization(O) \
> r = 1/2


#### Bipolar : AMI and Pseudoternary
- Bipolar
	- 세 개의 voltage level : positive, negative, zero
	- **한 데이터 요소에 대한 전압 level은 0**이고, **다른 요소에 대한 전압 level은 positive와 negative를 번갈아**가며 나타난다.

- Alternate Mark Inversion(AMI) and Pseudoternary
	![[Pasted image 20240405000202.png]]
	- AMI는 0이 전압 level 0으로, 1이 positive와 negative를 번갈아가며 나타나고 Psudoternary는 1이 0의 전압으로, 0이 positive와 negative 전압을 번갈아가며 나타남.
	- bipolar scheme는 NRZ와 같은 **signal rate를 가지지만, 기준선 문제가 없다.**
		- (constant -> 저주파 문제는 발생 가능)
	

> [!attention]
> DC component(O)   
> Self-synchronization(X)       
 > r = 1          

> [!tip]
> AMI 자체로는 저주파 문제(DC component)를 해결할 수 없지만 스크램블이라는 기법이랑 합쳐서 해결할 수 있다함 \
> -> clocking을 맞춰서 많이 씀


#### Bipolar : Multilevel Schemes
-  m개의 데이터 요소들의 그룹은 $2^m$개의 데이터 패턴들의 조합을 만들어 낼 수 있다.
- 만약 L개의 다른 레벨들을 가진다면, $L^n$개의 신호 패턴들의 조합을 만들어 낼 수 있다. n은 signal pattern의 길이이다.
- **2B1Q(Two binary, one Quaternary)**
	- 두 개의 이진 비트로 한 quaternary를 표현한다
	- **한 quaternary : 4개의 가능한 레벨 중 하나**를 나타낸다. 
![[Pasted image 20240405001805.png]]

- 수신자는 4개의 다른 threshold를 식별해야 한다.

> [!attention]
> DC components는..? (모르겠는데 아마 완전히는 해결 못할 듯) \
> Self-synchronization(X) \
> r = 2


#### Multi-transition : MLT-3
![[Pasted image 20240405002936.png]]

- 두 개 이상의 level을 가진 신호가 있는 경우,  두 개 이상의 전환 규칙으로 differential encoding scheme(차등 인코딩 체계)를 설계할 수 있다. MLT-3는 그 중 하나이다.

- Multiline transmission(전송) : **three-level(MLT-3)**
	- 세 가지 레벨(+V, 0, -V)를 이용하고 세 가지 전환 규칙을 사용하여 레벨 사이를 이동한다.
		규칙 1. 다음 비트가 0이면 전환히 없다.
		규칙 2. 다음 비트가 1이고 현재 레벨이 0이 아닌 경우 다음 레벨은 0이다.
		규칙 3. 다음 비트가 1이고 현재 레벨이 0이면 다음 레벨은 마지막 0이 아닌 레벨과 반대(opposite)이다.

### Block Coding
- synchronization과 몇몇 종류의 inherent(내재적) 오류 감지 기능을 제공하기 위해 **redundancy(중복성)** 이 필요하다.
- Block coding은 이러한 중복성을 제공할 수 있고 line coding의 성능을 향상한다.
- 일반적으로 블록 코딩은 m 비트 블록을 n 비트 블록으로 변경하며, 여기서 n은 m보다 크다.
- 블록 코딩을 **mB/nB 인코딩** technique(기술)이라고 한다.

![[Pasted image 20240405003352.png]]

- 4B/5B
	![[Pasted image 20240405003417.png]]
	- 4B/5B 인코딩을 하고 NRZ-I 인코딩을 시켜줌.

- **NRZ-I**
	- NRZ-I에서 constant 문제는 0들의 long sequence에서만 발생한다.
	- **0들의 long sequence가 이어지지 못하게** 인코딩을 하나 더 추가 : 4B -> 5B로 바꾼다.
		![[Pasted image 20240405003528.png]]

> [!info]
> Block Coding과 같은 방법을 사용하면 \
> 오류 감지, 재전송 가능, 때로는 동기화 문제도 해결이 가능하다.




## Analog-to-Digital Conversion
- 하지만 마이크나 카메라에서 생성되는 신호와 같은 아날로그 신호가 있을 때도 있다.
- Chapter 3에서 디지털 신호가 아날로그 신호보다 우수하다는 것을 살펴보았다. 오늘날에는 아날로그 신호를 디지털 데이터로 변경하는 추세이다.
- 이 섹션에서는 Pulse Code Modulation(PCM)** 과 **Delta Modulation(DM)** 이라는 두 가지 기술을 설명한다.


### Pulse Code Modulation(PCM)
![[Pasted image 20240405165400.png]]
- 아날로그 신호를 디지털 데이터로 변경(**digitization : 디지털화**)하는 가장 일반적인 기술을 Pulse Code Modulation(PCM)이라고 한다. PCM 인코더에는 세 가지 프로세스가 있다.
	- **Sampling** : 얼마나 자주 데이터를 읽을 건지
		- sampling을 많이 할수록 아날로그 신호와 비슷해진다. -> but 데이터 사이즈가 늘어난다. 
	- **Quantizing**(정량화)
	- **Encoding**

> [!note]
> 나이퀴스트 샘플링 : 샘플링 할 때는 최소한 최대 주파수의 두 배만큼 샘플링 해야 한다.

- Quantization and encoding of a sampled signal
	![[Pasted image 20240405165714.png]]


### Delta Modulation(DM)
![[Pasted image 20240405165854.png]]

- PCM은 매우 복잡한 기술이다.
	- PCM의 복잡도를 줄이기 위해 다른 기술이 개발 됨

- 가장 **간단**한 것은 delta modulation이다.
	- PCM은 각 샘플에 대해 signal amplitude의 값을 찾는다.
	- DM은 **이전 샘플로부터의 변화**를 찾는다.
		- 값이 커지면 1, 작아지면 0으로.



## Transmission Mode
- 한 device에서 다른 device로의 데이터 전송을 고려할 때 주요하게 봐야할 것은 wiring(배선)이며, wiring을 고려할 때 주요하게 봐야할 것은 data stream(데이터 스트림)이다.
- 한 번에 한 비트씩 전송할건지, 비트를 더 큰 그룹으로 그룹화 할 건지, 만약 그렇다면 어떻게 할 것인지?
- 링크를 통한 binary 데이터의 전송은 parallel(병렬) 혹은 serial(직렬) 모드로 수행할 수 있으며, isochronous(등시성)으로 수행할 수 있다.

> [!info]
> isochronous(등시성) : 데이터 간에 일관성 있게 일정한 시간 간격을 유지하며 전송시키는 것.
> 

![[Pasted image 20240405171540.png]]



### Parallel Transmission
![[Pasted image 20240405171755.png]]
- 1과 0으로 구성된 Binary data는 각각 n비트로 구성된 그룹으로 구성할 수 있다.
	- 그룹화를 통해 데이터를 1bit가 아닌 **n비트로 한 번에 전송**할 수 있다. 이를 parallel transmission(병렬 전송)이라고 한다.
	 - **n개의 lines 필요.**

### Serial Transmission
![[Pasted image 20240405171951.png]]
- serial transmission(직렬 전송)에서 한 비트가 다른 비트를 따른다. 따라서 두 통신 디바이스 간에 데이터를 전송하려면 n개가 아닌 **하나의 통신 채널**만이 필요하다.

#### Asynchronous transmission
![[Pasted image 20240405172213.png]]
- **Asynchronous transmission(비동기 전송)** 은 신호의 timing이 중요하지 않기 때문에 붙여진 이름이다. 대신, **합의된 패턴**에 따라 정보를 수신하고 translate(번역)한다.

