# Chapter 5 : Analog Transmission
## Chapter 5: Objective

### First Section : digital-to-analog conversion 
- 첫 번째 섹션에서는 digital-to-analog 변환에 대하여 설명한다. 이 섹션에서는 우리가 band-pass channel이 가능할 때 어떻게 디지털 데이터를 아날로그 신호로 바꿀 수 있는지를 보인다.

#### 방법 네 가지
- 설명된 첫 번째 방법은 디지털 데이터를 사용하여 carrier(반송파)의 amplitude(진폭)을 변경하는 Amplitude Shift Keying(ASK)이다. 
- 두 번째로 설명하는 방법은 디지털 데이터를 사용하여 carrier의 주파수를 변경하는 Frequency Shift Keying(FSK)이다.
- 세 번째 방법은 디지털 데이터를 표현하기 위해 carrier의 phase를 변경하는 Phase Shift Keying라고 한다.
- 네 번째 방법은 디지털 데이터를 표현하기 위해 carrier signal의 amplitude와 phase 모두를 변경하는 quadrature amplitude modulation(QAM)이다.

### Second Section : analog-to-analog conversion
- 두 번째 섹션에서는 analog-to-analog 변환에 대해 설명한다. 이 섹션은 우리가 더 작은 bandwidth를 가지고 어떻게 아날로그 신호를 새로운 아날로그 신호로 바꿀 수 있는지를 보인다.

#### 방법 세 가지
- 첫 번재 방법은 Amplitude modulation(AM; 진폭 변조)로, 원래 아날로그 신호의 변화에 따라 carrier signal의 진폭을 변경하는 방식이다.
- 두 번째 방법은 Frequency modulation(FM; 주파수 변조)로, 원래 아날로그 신호의 변화에 따라 반송파의 phase(위상)이 변경된다.
- 세 번째 방법은 Phase modulation(PM; 위상 변조)로, 원래 아날로그 신호의 변화에 따라 신호의 위상을 변경한다.

## Digital-to-Analog Conversion
- Digital-to-Analog conversion은 디지털 데이터의 정보를 기반으로 아날로그 신호의 특성 중 하나를 변경하는 과정이다.

### Conversion Process
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240421235115.png|600]]

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240421235131.png|600]]

ex) ASK : 0일 때의 amplitude와 1일 때의 amplitude를 바꾸어 신호 전달

### Aspects of Conversion
#### Bandwidth
디지털 데이터의 아날로그 변환을 위해 **요구되는 bandwidth**는 **signal rate에 비례**한다.

#### Carrier Signal 반송파
- 아날로그 변환에서, 송신 장치는 정보 신호의 **베이스 역할을 하는 고주파 신호**를 생성한다.
- 이 base signal을 carrier signal 혹은 carrier frequency라고 부른다.


### Binary ASK (BASK)
 Binary Amplitude Shift Keying : Amplitude를 바꾸는 것. **1과 0에 따라서 자신의 amplitude를 변화**시킴.
 
 - BASK에서, carrier signal의 amplitude는 신호 요소를 만들기 위해 변화된다. frequency와 phase는 amplitude가 변화할 동안 유지된다.
	![[Pasted image 20240414205947.png]]
- carrier signal은 단지 하나의 simple sine wave이지만, 변조 과정을 통해 nonperiodic한 composite signal이 생성된다.
- bandwidth는 signal rate(baud rate)에 비례하며, 여기서 S는 signal rate, B는 bandwidth이다.
- 데이터 통신에서, 우리는 일반적으로 **양방향 통신을 하는 full-duplex link를 사용**한다. 우리는 두 개의 carrier frequency들을 가지도록 **대역폭을 두 개로 나눠야** 한다.

### Binary FSK(BFSK)
Binary Frequency Shift Keying : frequency를 바꾼다. **0과 1에 따라서 frequency가 바뀐다.**

- BFSK에서, 데이터를 표현하기 위해 carrier signal의 주파수가 변화된다. 변조된 신호의 주파수는 한 신호 요소의 기간동안 유지되지만, 만약 데이터 요소가 바뀐다면 다음 신호 요소에 대하여 변화된다. 모든 신호에 대해서 peak amplitude와 phase는 둘 다 일정하게 유지된다.
	![[Pasted image 20240414212934.png]]

 - 주파수 두 개를 사용하는데 두 개가 겹치면 이 사이의 혼선이 발생하여 반드시 떨어져야 하는 공간이 필요하다. -> **더 많은 bandwidth가 필요**하다.

### Binary PSK(BPSK)
Phase Shift Keying : phase를 바꾼다.

- phase shift keying에서, 두 개 혹은 그 이상의 다른 신호 요소들을 표현하기 위해 carrier의 phase가 변화된다.
- 각 peak amplitude와 frequency는 phase가 변화하는 동안 일정하게 유지된다.
	![[Pasted image 20240414213301.png]]

- Binary PSK는 binary ASK만큼 간단하면서, 하나의 큰 이점을 가진다. - 이것은 **noise에 덜 취약하다(노이즈에 강하다)**.
- ASK에서, bit detection에 대한 기준은 신호의 진폭이며, PSK에서는 위상이다.
- 노이즈는 위상을 변경하는 것보다 진폭을 더 쉽게 변경할 수 있다. (noise가 전압을 바꾸기는 쉽지만 페이즈를 바꾸기는 쉽지 않음.)
- 두 개의 carrier signal이 필요하지 않기 때문에 PSK는 FSK보다 더 좋다.
- PSK는 phase를 구분할 수 있는 더 정교한 하드웨어가 필요하다.

> [!my_question]
> FSK든 PSK든 양방향 통신하는 거는 똑같은 거 아닌가? 왜 carrier signal을 하나만 필요로 함??



### Quadrature PSK(QPSK)
Binary는 한 비트만 보낼 수 있다. 두 개의 phase를 사용해서 변화시킬 수 있는 방법.
phase는 여러 개의 degree(각도)를 가진다.

- **QPSK**
	- 두 개의 개별(분리된) BPSK 변조를 사용한다. ; 하나는 in-phase, 하나는 quadrature(out-of-phase)
	- 각 multiplier에 의해 생성되는 두 개의 composite signal은 주파수는 같지만 위상이 다른 사인파이다.
	- 그것들이 추가 될 때, 결과는 다른 사인파이다.
	![[Pasted image 20240414215027.png]]
-> 한번에 두 데이터를 보낼 수 있음.

### Quadrature Amplitude Modulation : QAM
- QAM
	- PSK는 위상의 작은 차이를 구별하는 장비의 능력에 의해 제한된다.
	- **ASK와 PSK를 결합**하면?
		- Amplitude와 phase를 동시에 바꿔서 신호를 보낸다. 보낼 수 있는 비트수가 늘어난다.
	- 각 carrier에 대하여 다른 amplitude를 가지게 하는 in-phase와 quadrature 두 개의 carrier를 사용하는 아이디어는 QAM의 개념이다.
	![[Pasted image 20240414215642.png]]



## Analog-to-Analog Conversion
Analog-to-analog conversion, 혹은 아날로그 변조는 아날로그 신호에 의한 아날로그 정보의 표현이다.  누군가 이미 아날로그인 데이터를 왜 굳이 아날로그 신호로 변조해야하는 지 물을 수 있다. 만약 전송 매체가 본질적으로 bandpass이거나 bandpass channel만 가능한 경우 변조가 필요하다. analog-to-analog 변환은 세 가지 방법으로 수행할 수 있다. : AM, FM, PM

> [!summary]
> 아날로그 데이터도 아날로그 신호처럼 연속되게 표현된다. 근데 왜 굳이 아날로그 신호로 변조를 해야하나?  
> -> 우리가 쓰는 bandwidth가 다 다르다.  
> ex) 사람이 사용하는 bandwidth와 radio 신호의 bandwidth가 다 다르기 때문에 변환이 돼야한다.

![[Pasted image 20240414220429.png]]


### Amplitude Modulation (AM)
- AM 전송에서 carrier signal은 **변조 신호의 진폭 변화에 따라 진폭이 변하도록 변조**된다. 
	- Carrier frequency의 amplitude를 변환시킨다.
- carrier의 frequency와 phase는 똑같이 유지된다.
- 정보의 변화에 따라 진폭만이 변화한다.
- 변조는 변조 신호의 대역폭에 두 배에 해당하는 대역폭을 생성하여 carrier 주파수를 중심으로 한 범위를 커버한다.
- AM 라디오의 표준 대역폭 할당.
	![[Pasted image 20240414221108.png|500]]
	![[Pasted image 20240414221138.png]]
	위와 같이 중간에 빈 상태를 두어서 구간이 서로 간섭하지 못하도록 한다.

### Frequency Modulation(FM)
- FM 전송에서, carrier signal의 **주파수는 변조 신호의 전압(진폭) 변화에 따라 변조**된다.
- carrier signal의 peak amplitude와 phase는 일정하게 유지되지만, 정보 신호의 진폭이 변화함에 따라 carrier signal의 주파수가 변화한다.
- FM 라디오의 표준 대역폭 할당
![[Pasted image 20240414221547.png|500]]

![[Pasted image 20240414221534.png]]

### Phase Modulation(PM)
- PM 전송에서 carrier signal의 **phase는 변조 신호의 전압(진폭) 변화에 따라 변조**된다. carrier signal의 peak amplitude와 frequency는 일정하게 유지되지만 정보신호의 진폭이 변함에 따라 carrier signal의 위상은 변한다.
- PM은 한 가지 차이점을 제외하고 FM과 동일하다는 것을 수학적으로 증명할 수 있다.
	- FM에서 carrier signal의 순간적인 변화는 변조 신호의 진폭에 비례한다.
	- PM에서 carrier signal의 순간적인 변화는 **변조 신호의 미분**에 비례한다.
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240420115211.png|500]]


# Bandwidth Utilization
## Multiplexing
- **Multiplexing**은 **하나의 데이터 link를 통해서 여러 신호들의 동시 전송을 가능**하게 하는 기술들의 집합이다. 데이터와 통신 사용이 증가함에 따라 많은 트래픽이 발생한다. 
- 새 채널이 필요할 때마다 개별 링크를 계속 추가하여 이러한 증가를 수용하거나 더 높은 대역폭의 링크를 설치하여 각각 여러 신호를 전송하는 데에 사용할 수 있다.
- 하나의 링크를 추가하는 게 아닌 하나의 큰 링크를 만들어 놓고 나눠쓰는 것.

### Dividing A link into Channles
![[Pasted image 20240414222426.png]]
- Bandwidth가 크다. -> logical하게 n개의 채널로 나눠서 n개의 Input, output을 만들어낸다.

![[Pasted image 20240414222530.png]]
- 주파수, 광신호, 시간으로 나누는 방법이 존재.

### Frequency Division Multiplexing
bandwidth에 들어있는 frequency를 나누어 하나의 채널을 만드는 것.

- FDM은 **링크의 대역폭(헤르츠 단위)이 전송할 신호의 대역폭을 합친 것보다 클 때** 적용할 수 있는 아날로그 기술이다. 
- FDM에서는 각 송신 장치에서 생성된 신호가 서로 다른 carrier frequency를 변조한다.
- 이러한 변조된 신호는 링크로 전송될 수 있는 **single composite signal로 결합**된다.

![[Pasted image 20240414223015.png]]
![[Pasted image 20240414223023.png]]
- 받는 측에서는 **각각의 filter를 이용하여 받은 composite signal을 분리**한다.


#### Example
- 음성 채널이 4kHz인 대역폭을 사용한다고 가정한다.
- 3가지 음성 채널을 20~32kHz 대역폭을 가진 12kHz의 링크로 결합해야 한다. 주파수 도메인을 사용하여 구성을 표시한다. 
- guard bands는 없다고 가정한다.
![[Pasted image 20240414223540.png]]
![[Pasted image 20240414223558.png]]
- 계층적이다.


### Wavelength Division Mulitplexing
- Wavelength-division multiplexing(WDM)는 **광섬유 케이블**(fiber-optic cable)의 고속 데이터 전송 기능(high-data-rate capability)을 사용하도록 설계됐다.
- 광섬유 데이터 속도(optical fiber data)는 금속 전송 케이블(metallic transmission cable)의 데이터 속도보다 높지만 단일 회선(single line)에 광섬유 케이블을 사용하면 사용 가능한 대역폭이 낭비된다.
- Multiplexing은 여러 회선(several lines)를 하나로 결합하게 헤준다.
![[Pasted image 20240414224101.png]]
- 빛은 $\lambda$로 구분한다.
![[Pasted image 20240414224120.png|500]]

### Time Division Multiplexing
- Time-division multiplexing(TDM)은 여러 connection이 하나의 링크의 높은 대역폭을 공유하도록 해주는 디지털 프로세스이다.
- FDM에서와 같이 대역폭의 일부를 공유하는 대신 **시간을 공유**한다.
- 각 connection은 링크에서 시간의 일부분을 차지한다.
- FDM에서와 동일한 링크가 사용되지만 여기서는 주파수가 아닌 시간별로 링크가 구분되어 표시된다.
	![[Pasted image 20240414224636.png]]
	 - 시간에 흐름에 따라 각각이 쓸 수 있는 link를 시간동안 쓰게 만든다.
	 - 신호 1, 2, 3, 4의 일부가 순차적으로 링크를 차지한다.

#### Synchronous time-division multiplexing
![[Pasted image 20240414224811.png]]
![[Pasted image 20240414225004.png]]

#### Interleaving(끼워넣기)
![[Pasted image 20240414225011.png]]
- clock이 있고 clock을 돌리면서 multiplexing, demultiplexing을 수행한다.
- **clock의 synchronization을 이용**한다.

#### Framing bits
![[Pasted image 20240414225342.png]]
- 데이터를 보낼 때 특정한 frame의 형태, **추가적인 정보를 붙여서 synchronization을 맞춰줌**.


#### Comparison
![[Pasted image 20240414225502.png]]
- 그냥 Synchronous TDM을 사용하면 Frame에 빈 공간이 생김.

![[Pasted image 20240414225632.png]]
- 데이터를 있는 것만 불러와서 쓰게 됨. 그러면 synchronization이 안 맞게 될 수 있으나 각 데이터마다 추가 정보를 붙임 -> 이 주소를 보고 demultiplexing 할 수 있다.


## Spread Spectrum
- 몇몇 application에서, 대역폭 효율성보다 더 중요한 몇 가지 문제가 있다.
- 무선 application에서 station은 도청기나 악의적인 침입자의 방해 전파를 받지 않고 이 매체를 공유할 수 있어야 한다. : 보안
- 이러한 목표를 달성하기 위해 스프레드 스펙트럼 기술은 중복성(redundancy)을 추가한다.

> [!abstract]
> 쓰고 있는 bandwidth를 다른 목적으로 쓸 수 없을까? -> **보안**으로?  
> 데이터를 보낼 때 bandwidth가 크면 남는 bandwidth를 내 데이터를 보호하는 데에 쓸 수 있지 않을까?

![[Pasted image 20240414230551.png]]
- 내 데이터를 넓은 지역으로 분포시켜서 bandwidth의 한 지역을 감청 당해도 정보가 모두 감청되지 않고 보호 될 수 있다.

### Frequency hopping spread spectrum(FHSS) 
![[Pasted image 20240414230756.png]]
![[Pasted image 20240414230803.png]]

- 비트의 패턴에 따라서 frequency를 바꿔서 사용하는 것.
- 예를 들어, 누가 200 kHz만 보고 있으면 데이터를 일부밖에 볼 수 없게 된다. 어느 주파수 대역을 사용하는지 모르면 데이터를 뽑아낼 수 없다.

### Directed Sequence Spread Spectrum(DSSS)
- DSSS도 원본 신호의 대역폭을 확장하지만 프로세스가 다르다.
- DSSS에서는 spreading code를 사용하여 각 데이터 비트를 n비트로 대체한다. 즉, 각 비트에는 chip이라고 하는 n비트의 코드가 할당되며, 여기서 chip rate는 데이터 비트의 n배이다.
	![[Pasted image 20240414231201.png]]
	- Chip generator를 이용하여 신호를 변조해서 보낸다.
	- 받는 쪽은 spreading code를 이용하여 original data를 복원한다.
