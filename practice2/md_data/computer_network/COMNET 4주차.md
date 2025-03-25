## Chapter 3 : Introduction to Physical Layer
### Layers in the TCP/IP Protocol Suite
- **Physical Layer**
    - 이 계층은 구조화되지 않은 **원시 비트 스트림 데이터**가 물리적 매체를 통해 송수신되는 방식을 제어한다.
    - 이 계층은 네트워크의 전기, 광학(optical) 및 **물리적 구성 요소**로 구성된다.
    - 물리 계층은 모든 상위 계층의 신호를 전달한다.
    - LAN 카드(l1, l2 layer)

### Objective
- 어떻게 데이터와 신호가 아날로그 또는 디지털이 될 수 있는지 보인다. 아날로그는 연속적인 entity를 의미하고 디지털은 불연속적인 entity를 의미한다.
    - 4가지 조합 : 아날로그 데이터, 디지털 데이터, 아닐로그 신호, 디지털 신호
- 이 섹션에서는 simple 신호와 composite 신호에 대해 설명한다. 주기, frequency(주파수), phase 등 아날로그 신호의 속성에 대해서도 설명한다.
- 비트 전송률과 비트 길이와 같은 디지털 신호의 속성에 대해 설명한다. 또한 아날로그 신호를 사용하여 디지털 데이터를 전송하는 방법도 보인다.
- 네 번째 섹션은 전송 장애(transmission impairment)에 대한 내용이다. 여기서는 감쇠(attenuation), 왜곡(distortion), 노이즈(noise)가 신호를 어떻게 손상시킬 수 있는지 보인다.
- 다섯 번째 섹션에서는 데이터 전송률 제한(data rate limit) : 사용 가능한 채널로 전송할 수 있는 bps(초당 비트수)에 대해 설명한다. 노이즈가 없는 채널과 노이즈가 있는 채널의 데이터 전송률을 조사하고 비교한다.
- 여섯 번째 섹션에서는 데이터 전송의 성능에 대해 설명한다. bandwidth, throughput, latency, jitter 등 여러 채널 측정값을 살펴본다.
  
- Communication at the physical layer
    - 신호를 다룬다. 전송 매체에 따라 신호는 달라짐.

### Analog and Digital Data
- **데이터는 아날로그 또는 디지털**일 수 있다. 아날로그 데이터는 **연속적인 정보**를 의미하고 디지털 데이터는 **불연속적인 상태**를 가진 정보를 의미한다. 예를 들어 시침, 분침, 초침이 있는 아날로그 시계는 시계 바늘의 움직임이 연속적인 형태로 정보를 제공한다. 반면에 시와 분을 알려주는 디지털 시계는 8시 5분에서 8시 6분으로 갑자기 바뀐다.
- 신호는 나타내는 데이터와 마찬가지로 아날로그 또는 디지털일 수 있는다. 아날로그 신호는 일정 시간(period) 동안 무한히 많은 level의 intensity를 갖는다. 파동이 값 A에서 값 B로 이동하면서 그 경로를 따라 무한한 수의 값을 통과하고 포함한다. 반면에 디지털 신호는 정의된 값의 수가 제한되어 있다. 각 값은 임의의 숫자가 될 수 있지만 대체로 1과 0이다.

### Comparison of Analog and Digital Signals
![[Untitled 38.png|Untitled 38.png|500]]


### Periodic and Nonperiodic
- **periodic signal(주기적 신호)** 는 주기라고 하는 측정 가능한 time frame 내에서 패턴을 완성하고 그 이후 동일한 주기 동안 그 **패턴을 반복**한다. 하나의 전체 패턴의 완성을 cycle이라고 부른다. **nonperiodic signal(비주기적 신호)** 는 시간이 지남에 따라 반복되는 패턴이나 주기를 나타내지 않고 변화한다. 아날로그 신호와 디지털 신호 모두 해당된다.
- 디지털 신호는 대체로 nonperiodic하다.
	- period : 주기의 길이 vs. cycle : 하나의 완전한 반복
		- 둘 다 주기로 번역되지만 약간 다른 의미를 가진다.


### periodic Analog Signals
- Periodic Analog Signal은 **simple signal과 composite signal**로 분류될 수 있다. simple periodic signal인 사인파는 더 단순한 신호로 분해할 수 없다. composite periodic analog signal은 여러 개의 사인파로 구성된다.
	- simple signal : 신호가 하나로만 이루어짐 -> 더 나눠지지 않음.
	- composite signal : 여러 신호가 합쳐짐 -> 여러 개의 simple 신호로 나눌 수 있다.

### Sine Wave 정현파
- 사인파는 **periodic analog signal**의 가장 기본적인 형태이다. 단순한 진동 곡선(oscillating curve)로 시각화하면 cycle 동안의 변화는 부드럽고 일관되며 연속적인 rolling flow이다.  ![[Pasted image 20240328215359.png||500]]

#### Amplitude(전압)
![[Pasted image 20240328215437.png|500]]
- 위 사진의 두 신호는 다른 신호인데, Amplitude(전압) 크기 차이가 있다.
	- **진폭의 차이**

#### Frequency(주파수)
![[Pasted image 20240328215750.png|500]]
- 위 사진의 두 신호는 **frequency의 차이**가 존재한다. **초당 사이클(초당 주기수)을 의미하는 Hz를 사용**한다.
	ex) 집에서 사용하는 전력의 frequency는 60Hz이다. 이 사인파의 period(주기)는 다음과 같이 결정할 수 있다.
				$$T = \frac{1}{f} = \frac{1}{60} = 0.166s = 0.166 * 10^3ms = 16.6ms$$
		-> period, 즉 주기 길이가 16.6ms
		 즉, 집에 있는 조명의 전원 주기는 16.6ms이다. 우리의 눈은 이러한 급격한 amplitude의 변화를 구분할만큼 민감하지 않다.
	
- Frequency는 **시간에 따른 변화률**이다. 짧은 시간 동안의 변화는 높은 frequency를 의미한다. 오랜 시간 동안의 변화는 frequency가 낮다는 것을 의미한다.
- 신호의 변화가 생기지 않으면 Frequency는 0이고, 신호가 갑자기 변하면 그것의 frequency는 infinite이다.
	- 갑자기 변하는 신호? -> digital 신호

#### Phase
- phase(위상) 혹은 Phase shift는 **time 0을 기준으로 한 waveform(파형)의 위치**를 설명한다. 파동을 시간 축을 따라 앞뒤로 이동할 수 있는 것으로 생각하면 Phase는 그 이동의 양을 설명한다. phase는 첫 번째 주기의 상태를 나타낸다.
	![[Pasted image 20240328223555.png|500]]
	- phase가 다른 세 가지 신호

### application of Simple sine waves in daliy life
- 한 곳에서 다른 곳으로 전기 에너지를 전달하기 위해 single 사인파를 보낼 수 있다.
- 예를 들어, 전력 회사는 60Hz의 single 사인파를 전송하여 가정과 기업에 전기 에너지를 분배한다.
- 또 다른 예로, 도둑이 집의 문이나 창문을 열면 single 사인파를 전송하여 보안 센터에 경보를 보낼 수 있다. 
- 첫 번째 예에서 사인파는 에너지를 전달하고, 두 번째 경우 사인파는 위험 신호이다.
- 데이터 통신에서 simple 사인파는 유용하지 않다.

### Composite Signal 복합파
- 모든 Composite signal은 **amplitude, frequency, phase가 다른 simple 사인파의 조합**이다.
- composite signal은 periodic일 수도, non periodic일 수도 있다.
	- 데이터 통신에서는 periodic한 신호를 사용.
	![[Pasted image 20240328224401.png|500]]
	- 세 개의 single 사인파의 조합으로 이루어진 composite signal


##### 참고
fourier Transform : \[시간 - 진폭] -> \[주파수 - 진폭]
![](http://upload.wikimedia.org/wikipedia/commons/7/72/Fourier_transform_time_and_frequency_domains_%28small%29.gif)
 
### Bandwidth (대역폭)
- Composite signal에 포함된 frequency range(주파수 범위)가 그 신호의 **Bandwidth(대역폭)** 이다. Bandwidth는 일반적으로 두 숫자 사이의 차이이다. 
	- 예를 들어, Composite signal에 1000과 5000 사이의 frequency가 포함된 경우 대역폭은 5000 - 1000 = 4000이다.
	- => Composite signal에서 single signal을 찍어봤을 때 **가장 큰 주파수와 가장 작은 주파수의 차이.**
	![[Pasted image 20240328231609.png|500]]
	- periodic이든 nonperiodic이든 대역폭은 같다.

#### Example : Wi-Fi 2.4GHz vs 5GHz
- Frequency
	- 2.4GHz vs. 5GHz : 주파수 대역
	- 긴 파장(wavelength ; 대역폭이 좁음)이 더 좋은 회절성을 가진다. 
- BandWidth 비교
	- 2.4~2.462GHz : 대역폭 0.062 정도
	- 5.180~5.850GHz : 0.67정도. 변화가 많다.(같은 시간에서)
	- 5GHz는 2.4GHz에 비해 회절성(벽을 뚫고 나가는 힘)이 떨어진다.

### Digital Signals
- 정보는 아날로그 신호로 표현되는 것 외에도 디지털 신호로 표현될 수 있다.
	- 예를 들어 1은 양의 전압(voltage)으로, 0은 0의 전압으로 인코딩할 수 있다.
- 디지털 신호는 2보다 큰 level을 가질 수 있다. 
	- **2보다 큰 level을 가질 경우 각 레벨에 대해 1비트 이상을 전송할 수 있다.** 
	![[Pasted image 20240328232347.png|600]]
	- 위 사진에서 왼쪽 그림은 초당 두 개의 레벨을 가진 디지털 신호를 보여준다. 
		- 오른쪽 사진에서는 2 level을 가지고 8bits를 전송하는 데 1초가 걸리므로 초당 전송 비트수인 bps가 8이 된다.
		- 왼쪽 사진에서는 1초에 16bits를 보내고(16bps) 오른쪽과 비교해서 같은 시간 내에 더 많은 비트를 전송해야 하기 때문에 level을 높여 더 많은 양의 bit를 전송한다.
		- 따라서 **bps를 높이려면 level을 높여야** 한다. -> 그러나 level을 높이면 amplitude가 애매하게 오면 무슨 레벨인지 정하기가 복잡해진다는 문제 등 **신뢰성이 낮아진다.**

### Bits Rate
- 대부분의 디지털 신호는 nonperiodic하고 따라서 period와 frequency는 적절한 특성들이 아니다. 디지털 신호를 설명할 때는 (frequency 대신) **bit-rate(비트 전송률)** 라는 다른 용어가 사용된다. 비트 전송률은 1초 동안 전송되는 비트의 수로, **초당 비트(bps)** 로 표현된다. 
	- ex) 디지털 신호를 사용하여 고화질 비디오 신호를 방송하는 HDTV를 생각해보자. 일반적으로 화면당 1920 x 1080 픽셀이 있으며 화면은 초당 30회 갱신된다(30fps). 하나의 컬러 픽셀을 나타내기 위해서 24 비트가 필요하다면 비트 전송률은 아래과 같이 계산할 수 있다. $$ 1920 * 1080 * 30 * 24 = 1,492,992,000 \simeq 1.5Gbps$$
	- TV station은 이러한 전송률을 압축(ex : 허프만)을 통해서 20에서 40Mbps로 낮출 수 있다.

## Data Communication
- 데이터 통신에서, 우리는 일반적으로 periodic analog signals와 nonperiodic digital signals를 사용한다.

### Digital As Composite Analog
- 푸리에 분석(fourier analysis)를 기준으로 , 디지털 신호는 composite analog signal이다. 
	- **디지털 신호는 analog signal들의 조합**
	- bandwidth는 infinite하다. (만약 신호가 갑자기 변화하면, 그것의 frequency는 infinite하다.)
	![[Pasted image 20240328235218.png|600]]
	- 위 사진에서 a는 periodic digital signal의 시간, 주파수 도메인을 각각 나타낸 것이다. (참고 : time -> frequecy를 하는 게 푸리에 변환)
	- b는 nonperiodic digital siganl의 시간, 주파수 도메인. 이때 nonperiodic digital signal의 frequency는 무한대로 가는 게 이상적이지만 주파수가 무한대로 가는 것은 실세계에서 불가능하다.
		참고 : ![[Pasted image 20240328235730.png]]

### Transmission of Digital Signal
- 두 가지 방식 : baseband transmission 혹은 **broadband transmission(광대역 전송 : modulation(변조) 사용)**. 이 중 하나를 사용하여 디지털 신호를 전송할 수 있다.
	- Baseband Transmission(기저 대역 전송) : 디지털 신호를 아날로그 신호로 바꾸지 않고 채널을 통해 디지털 신호를 전송하는 것. (**Low Pass Channel : 대역폭이 0부터 시작하는 채널**이다. 대역폭이 하나의 채널만 구성하는 전용 중간 매체가 있는 경우)
		- 대역폭 : 전송 매체의 전체 대역폭을 차지하는 단일 통신 채널을 사용
		- 신호 유형 : 디지털 신호
		- 거리 : 주로 건물 또는 단일 룸 내의 통신과 같은 단거리 통신에 사용
	- **Broadband transmission ; 광대역 전송(modulation ; 변조) :** 전송을 위해 **디지털 신호를 아날로그 신호로 변환**하는 것. Modulation은 **bandpass 채널(0부터 시작하지 않는 대역폭을 가진  채널)을 가능**하게 한다.
		-> 데이터 시그널을 사용할 수 있게됨.
		- 대역폭 : 더 넓은 주파수의 정보를 전송하기 위해 여러 채널을 사용
		- 신호 유형 : 아날로그 또는 디지털일 수 있다.
		- 거리 : WAN을 통한 통신과 같은 장거리 통신에 사용.
		- Broadband transmission![[Pasted image 20240329001013.png]]
	- 디지털 신호는 채널을 거쳐서 전송된다. 

### Transmission Impairment
- 신호는 완벽하지 않은 전송매체를 통해 이동한다(전달된다).  이러한 불완전성은 신호 손상(감쇠)를 야기한다. 즉 매체의 시작 부분의 신호와 매체의 끝 부분의 신호가 같지 않다. 전송된 것이 수신된 것이 아니다. attenuation(감쇠), distortion(왜곡), noise(노이즈)가 신호 손상을 야기한다. 

#### Attenuation
- **감쇠는 에너지 손실**을 뜻한다.
	- simple 혹은 composite 신호가 매체를 통과할 때 매체의 저항을 극복하면서 일부 에너지가 손실된다.
	- 그렇기 때문에 전기 신호를 전달하는 전선은 시간이 지나면 뜨겁지는 않더라도 따뜻해진다.
	- (전기 에너지 -> 열 에너지)
	- 이 손실을 보상하기 위해 신호를 증폭하기 위한 **증폭기가 사용**되곤 한다.
	- ![[Pasted image 20240329164428.png]]
	- 참고 : 이러한 신호 증폭기는 Ling형에 달려서 사용된다. (Ling형은 길기 때문에)

#### Distortion
 - **왜곡은 신호의 form이나 shape이 변하는 것**을 의미한다.
	 - 서로 다른 frequency로 구성된 composite signal에서는 왜곡이 발생할 수 있다.
	 - 각 신호 구성 요소는 매체를 통해 **고유한 전파 속도(propagation speed)** 를 가지므로, 최종 목적지에 도착하는 데 각각의 지연이 존재한다.
	 - 지연이 period duration과 정확히 같지 않으면 **지연의 차이로 인해 phase의 차이가 발생**할 수 있다.
	 - ![[Pasted image 20240329165600.png]]

#### Noise
- **노이즈**는 impairment의 또 다른 요인이다.
	- thermal noise, induced noise, crosstalk, impulse noise와 같은 여러 유형의 노이즈로 인해 신호가 손상될 수 있다.
	- **thermal noise**는 전선에서 전자가 무작위로 움직이면서 **원래 송신기에서 보내지 않은 추가 신호를 생성**하는 것이다.
	- **induced noise**는 모터와 같은 소스에서 발생한다.
	- **crosstalk**는 한 wire(전선)가 다른 wire에 미치는 영향이다.
		![[Pasted image 20240329171009.png]]


### SNR(Signal-to-Noise Ratio) : 신호 대 잡음비
- SNR
	- $$SNR = \frac{P_{signal}}{P_{noise}}$$
	- $P_{signal}$은 신호의 세기, $P_{noise}$는 노이즈의 세기를 뜻한다.
	- SNR은 신호 세기와 비례하고 노이즈의 세기와 반비례하다.
		- 크면 좋은 것.
		![[Pasted image 20240329171231.png]]
- Example
	- noiseless한 채널에서 SNR과 $SNR_{dB}$의 값
	- $SNR = (signal power)/0 = \infty$ ->  $SNR_{dB} = 10log_{10}\infty = \infty$

### Data Rate Limit
- 통신에서 매우 중요한 고려 사항은 채널을 통해 bps로 얼마나 데이터를 빠르게 전송할 수 있는가이다. **데이터 전송률**을 계산하는 두 가지 이론적 공식이 개발되었는데, 하나는 noise가 없는 채널에 대한 Nyquist 공식이고, 다른 하나는 noise가 있는 채널에 대한 Shannon 공식이다.

#### Noiseless Channel : Nyquist Rate
- **noiseless channe**l에서, Nyquist bit rate 공식은 이론적으로 **최대의 bit rate**를 정의한다.
- $$BitRate = 2 * bandwidth * log_2L$$
- noise가 없으면 이 정도의 bps를 보장 가능하다.
- L = level의 수

#### Noisy Channel : Shannon Capacity
- 실생활에서, noiseless한 채널을 가질 수 없다; 채널은 항상 noise를 가진다. 1944년, Claude Shannon은 noisy channel에서 이론적으로 가장 높은 data rate를 결정하는 Shannon capacity라고 불리는 공식을 소개했다.
	- $$Capacity = bandwidth * log_2(1+SNR)$$

#### Example
- SNR이 거의 0에 가까운 극도로 noise이 심한 채널을 생각하자. 이 채널의 경우 용량 C는 다음과 같이 계산된다.
	- $$C = Blog_2(1+SNR) = Blog_2(1+0) = Blog_21 = B * 0 = 0$$
	- C가 0이면 보낼 수 있는 정보가 없다는 뜻. 
- 즉, 이 채널의 용량은 대역폭에 관계없이 0이다. 이 채널을 통해 데이터를 수신할 수 없다.

#### Example : Using Both Limits
- 1-MHz 대역폭을 가진 채널이 있9다. 이 채널에서의 SNR은 63이다. 적절한 비트 전송률과 신호 레벨은 얼마인가?
	- Shannon 공식을 통해 상한(이론상 최대의 데이터 전송률)을 찾을 수 있다. $$C = Blog_2(1+SNR) = 10^6log_2(1+63)=10^6log_264 = 6Mbps$$
	- Shannon 공식으로 상한을 6Mbps로 구할 수 있다. 더 나은 성능을 위해 더 낮은 속도인 4Mbps를 선택한다. 이후 나이퀴스트 공식을 사용하여 signal level의 수를 찾는다. $$4Mps = 2 * 1 MHz * log_2L$$ -> L = 4

## Performance
- 지금까지 네트워크를 통해 데이터(신호)를 전송하는 도구와 데이터의 작동 방식에 대해 설명했다. 네트워킹에서 중요한 문제 중 하나는 네트워크의 성능 -- 네트워크가 얼마나 좋은가이다.

### Bandwidth
- 네트워크 성능을 측정하는 특성 중 하나는 **Bandwidth(대역폭)**이다.
	- 대역폭은 두 가지 다른 측정 값으로 두 가지 다른 맥락에서 사용될 수 있다. 
		- **Hz(hertz : 헤르츠) 단위**의 대역폭
		- **bps단위**의 대역폭
	- hertz 단위의 대역폭
		- **composite signal에 포함된 frequency의 범위** 또는 채널이 통과할 수 있는 frequency의 범위이다. 예를 들어, 가입자(구독자) 전화선의 대역폭이 4kHz라고 가정할 수 있다.
	- bps 단위의 대역폭
		- **채널, 링크, 혹은 심지어 네트워크가 전송할 수 있는 bps**이다. 예를 들어, 고속 이더넷 네트워크(또는 이 네트워크의 링크)의 대역폭은 최대 100Mbps라 할 수 있다. 즉, 이 네트워크는 100Mbps를 전송할 수 있다.

### Throughput
- **처리율** : 네트워크를 통해 **실제로 데이터를 얼마나 빠르게 보낼 수 있는지** 측정값
	- 언뜻 보기에는 bps의 대역폭과 처리량이 동일해 보이지만, 이 둘은 다르다.
	- 내가 보낼 수 있는 최대가 bandwidth이다.
	- 한 링크의 대역폭이 Bbps일 수 있지만, 이 링크를 통해 전송할 수 있는 대역폭은 Tbps이며, T는 항상 B보다 작거나 같다.
- Bandwidth는 **링크의 잠재적 측정값**이며, Throughput은 데이터를 얼마나 빨리 전송할 수 있는지에 대한 **실제 측정값**이다.
	- 예를 들어, 우리가 1Mbps의 대역폭을 가진 링크가 있더라도, 연결된 디바이스는 200kbps만을 다룰 수 있다. 즉, 이 링크를 통해 200kbps 이상을 전송할 수 없다.

ex)
- 10Mbps의 대역폭은 가진 네트워크는 분당 평균 12,000개의 프레임만 전달할 수 있으며 각 프레임은 평균 10,000비트를 전달한다. 이 네트워크의 처리량은 얼마인가?
	- 대역폭은 10Mbps : 내가 초당 보낼 수 있는 최대가 10Mbps -> 실제 이만큼을 나 혼자 쓸 수 없음.
	- Throughput = (12,000 * 10,000) / 60 = 2Mbps 
	- 위 식에서 구해진 2Mbps가 내가 실제 지금 보낼 수 있는 양이다. 
	- 위 케이스에서는 처리율이 대역폭의 거의 5분의 1이다.

### Latency
- **latency(지연율)** 혹은 delay는 source에서 첫 비트가 전송된 시점부터 전체 메세지가 destination에 완전히 도착할 때까지 걸리는 시간을 정의한다.
	- latency는 4개의 요소로 이루어진다. : propagation time(전파 시간), transmission time(전송 시간), queuing time(대기 시간), processing delay(처리 지연 시간)
	- Latency = propagation time + transmission time + queuing time + processing delay

### Four source of packet delay
시간은 네 개의 포인트로 만들어진다.
![[Pasted image 20240330124813.png]]
- $d_{proc}$ : nodal processing
	- 비트 에러 확인
	- output link  결정
	- 일반적으로 ms(millisecond)보다 짧음
- $d_{queue}$ : **queueing delay**
	- 전송을 위해 output link에서 기다리는 시간
	- 큐에 들어가서 큐를 떠나는 데에 걸리는 시간이다.
	- **router의 혼잡 정도**에 달려있음.
	- queue에 요소가 많으면 늦어지고(데이터 전송량이 많음 ; 이용하는 사람이 많음.) 적으면 빨라진다.
	- Jitter 발생과 연관. 
		- Jitter의 시간을 맞춰주는 건 불가능하다. 
		- -> 몰리지 않는 방법을 찾아내야(알고리즘)
- $d_{trans}$ : transmission delay
	- L : packet length(bits) 메세지 크기
	- R : link bandwidth(bps) 대역폭
	- $d_{trans} = L/R$
- $d_{prop}$ : propagation delay
	- d : length of physical link 거리
	- s : **propagation speed** in medium 전송 매체의 속도 (~$2*10^8 m/sec$)
	-  $d_{prop} = d/s$ 
- 여기서 L, R, d, s의 값은 상수이거나(정해져 있거나) 영향이 별로 크지 않다. 또한 $d_{proc}$의 값은 ms보다 작으니 결국 전체 시간은 $d_{queue}$에 의해 좌우된다.
- 참고 : $d_{trans}$와 $d_{prop}$ 의 개념은 매우 다르다. 

#### Propagation Time
- 전파 시간은 **bit가 source에서 destination까지 이동하는 데 필요한 시간**을 측정한다.
	- **Propagation time = Distance / (Propagation Speed)**
- ex)
	- 두 지점 사이의 거리가 12,000Km인 경우에 전파 시간이 어떻게 되는가? 케이블의 전파 속도는 $2.4 * 10^8$ m/s로 가정한다.
	- 전파 시간 = $(12,000 * 1,000) / (2.4 * 10^8)$ = 50ms(0.05s)
- 이 예는 source와 destination 사이에 direct cable이 있는 경우 비트가 대서양을 단 50ms 만에 건너갈 수 있음을 보여준다.

#### Transmission Time
- 데이터 통신에서 우리는 1비트만을 보내지 않고 메세지를 보낸다.
	- 첫 번째 비트는 destination에 도착하는 데에 propagation time과 같은 시간 들것이다; 마지막 비트 또한 같은 시간을 가진다.
	- **메세지 전송이 시작될 때부터 끝날 때까지의 시간**. (첫 번째 비트부터 마지막 비트까지 걸리는 시간 : 비트가 수신측에 전송되는 시간은 고려하지 않고 **단지 송신측에서 전송을 끝낸 그 시점까지의 시간**)
	- 하지만, 첫 번째 비트가 송신자를 떠날 때와 마지막 비트가 수신자에게 도착할 때 사이에 시간이 있다. 첫 번째 비트는 더 일찍 출발하여 더 일찍 도착하고 마지막 비트는 더 늦게 출발하여 더 늦게 도착한다. 메세지의 transmission time은 메세지의 크기와 채널의 대역폭에 따라 달라진다.
	- **Transmission time = (Message size) / Bandwidth**

- ex1) 
	- 만약 네트워크의 대역폭이 1 Gbps라면, 2.5KB의 메세지에 대하여 Propagation time과 transmission time은 무엇인가? 송신자와 수신자 사아의 거리는 12,000 km이고 빛은 $2.4 * 10^8$로 이동한다고 가정한다.
		- Propagation time = $(12,000 * 1000) / (2.4 * 10^8)$ = 50ms
		- Transmission time = $(2500 * 8) / 10^9$ = 0.020ms
	- 메세지가 짧고 대역폭이 높기 때문에 transmission time이 아닌 propagation이 가장 중요한 요소이다.

- ex2) 
	- 만약 네트워크의 대역폭이 1 Mbps라면, 5-MB의 메세지(이미지)에 대하여 Propagation time과 transmission time은 무엇인가? 송신자와 수신자 사아의 거리는 12,000 km이고 빛은 $2.4 * 10^8$로 이동한다고 가정한다.
		- Propagation time = $(12,000 * 1000) / (2.4 * 10^8)$ = 50ms
		- Transmission time = $(5,000,000 * 8) / 10^6$ = 40s
	- 메세지가 길고 대역폭이 높지 않기 때문에 propagation time이 아닌 transmission time이 가장 중요한 요소이다. propagation time은 무시될 수 있다.

#### Queuing Time 대기 시간
- 각 중간 또는 최종 디바이스가 메시지를 처리하기 전에 대기하는 데 필요한 시간이다.
	- queuing time은 고정된 요소가 아니며 네트워크에 가해지는 부하에 따라 달라집니다.
	- 네트워크에 트래픽이 많으면 queueing time이 증가한다.
	- **router와 같은 중간 장치는 도착한 메세지를 queue(대기열)에 넣고 하나씩 처리**한다. 만약 메세지가 많으면 각 메세지는 대기해야 한다.
