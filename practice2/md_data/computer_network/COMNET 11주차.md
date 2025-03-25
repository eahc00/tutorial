## Network Layer : Network Protocols
### Objective
- 첫 번째 섹션에서는 IPv4 protocol에 대해서 다룬다.
	- 첫 번째로 IPv4 datagram format을 설명한다.
	- 이후 데이터그램에서의 분할(fragmentation)의 목적을 설명한다.
	- 그런 다음 데이터그램에서 옵션 필드와 그 용도에 대해 간략하게 설명한다.

- 두 번째 섹션에서는 ICMPv4에 대해 설명한다. 
	- 네트워크 계층에서 IPv4를 지원하기 위해 사용되는 보조 프로토콜 중 하나이다.
	- 먼저 각 옵션의 용도에 대해 간략하게 설명한다.
	- 그런 다음 ICMP를 디버깅 도구로 사용하는 방법을 설명한다.

- 세 번째 섹션에서는 IPv6 프로토콜에 대해 설명한다.
	- 새로운 패킷 형식(packet format)에 대해 설명한다.
	- 그런 다음 확장 헤더(extension header)를 사용하여 옵션을 대체하는 방법을 설명한다.


### Network-Layer Protocols
- version 4에서의 네트워크 계층은 하나의 메인(주요) 프로토콜과 세 개의 보조 프로토콜로 생각할 수 있다.
- 메인(기본) 프로토콜인 IPv4는 패킷의 **packetizing, forwarding, delivery**를 담당한다.
- ICMPv4는 IPv4에서 전송 중에 발생할 수 있는 몇몇 **오류를 처리하는 것을 지원**한다.
- [IGMP](https://www.cloudflare.com/ko-kr/learning/network-layer/what-is-igmp/)는 멀티캐스팅에서 IPv4를 지원하는 데 사용된다.
- **ARP는 주소 매핑**에 사용된다.


#### Position of IP and other network-layer protocols in TCP/IP protocol suite
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240515220549.png|400]]


#### IP datagram
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240515220636.png|450]]

- VER (4 bits) : version number.
	- IPv4에서는 0100(4).
- **HLEN (4 bits) : header length**
	- **\*4**를 해서 사용하도록 만들어짐.
	- 헤더 길이가 **20bytes~60bytes**의 범위를 가지므로 **최솟값은 5.**
		- 5보다 작으면 에러가 발생했다고 간주하고 데이터를 버림.
- **TTL(Time-to-live)** : **router 지날 때마다 값을 하나씩 줄여서 0이 되면 버린다**
	- default를 계속 도는 문제를 해결.


### Datagram Format
- IP가 사용하는 패킷을 **데이터그램(datagram)** 이라고 한다.
- 데이터그램은 **헤더와 페이로드(payload, 데이터)** 두 부분으로 구성된 가변 길이의 패킷이다.
- 헤더의 길이는 20~60바이트이며 routing과 delivery에 필수적인 정보를 포함한다.
- TCP/IP에서는 헤더를 4바이트 섹션으로 표시하는 것이 일반적이다.


#### Multiplexing and demultiplexing using the value of the protocol field

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240515221524.png|350]]


### IP Header
#### Example 1.
> [!problem]
> - IPv4 패킷의 첫 8비트가 (01000010)으로 도착했다.
> - 수신자는 패킷을 삭제하는 이유가 무엇인가?

> [!solution]
> - 이 패킷에는 오류가 존재한다.
> - 처음 4개 비트(0100)는 버전을 나타내고, 이는 4이므로 올바른 버전이다.
> - 다음 4개 비트(0010)은 헤더 길이를 나타낸다. 이때 헤더 길이는 2 * 4 = 8이 되는데 이는 헤더 길이의 최솟값인 20 bytes보다 작으므로 패킷이 전송 중에 손상되었다고 판단하고 버린다.


#### Example 2.
> [!problem]
> - IPv4에서, HLEN의 값이 (1000)이다.
> - 이 패킷에서 몇 바이트의 옵션이 전달되는가?

> [!solution]
> - HLEN 값이 8이라는 것은 헤더의 총 길이가 8 * 4 = 32bytes라는 것을 의미한다.
> - 첫 번째 20바이트는 base 헤더이고, 다음 12바이트가 옵션이 된다.


#### Example 3.
> [!problem]
> - IPv4 패킷에서, HLEN의 값은 5이다.
> - total length field는 $(0028)_{16}$이다.
> - 이 패킷에서 몇 바이트의 데이터가 전달되는가?

> [!solution]
> - HLEN 값은 5이고, 이것은 헤더의 총 길이가 5 * 4 = 20바이트임을 의미한다.
> 	- 옵션이 없다는 것.
> - total length는 $(0028)_{16} = 40$바이트이고, 이는 패킷이 20바이트(40 - 20)의 데이터를 전달함을 의미한다.


### Fragmentation
- 데이터그램은 여러 네트워크를 통해 이동할 수 있다.
- 각 라우터는 수신한 프레임으로부터 IP 데이터그램을 decapsulate하고 처리한 다음, 다른 프레임으로 캡슐화한다.
- 수신된 프레임의 형식과 크기는 프레임이 방금 통과한 물리적 네트워크에서 사용하는 프로토콜에 따라 달라진다.
- 전송된 프레임의 형식과 크기는 프레임이 이동할 물리적 네트워크에서 사용하는 프로토콜에 따라 달라진다.
- 예를 들어 라우터가 LAN을 WAN에 연결하는 경우 라우터는 LAN 형식의 프레임을 수신하고 WAN 형식의 프레임을 보낸다.


#### Maximum transfer unit(MTU)
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240515225007.png|450]]

- 데이터를 나누고 붙이고 해야.
- 붙이려면 어떤 패킷의 몇 번째인지를 알아야 붙일 수 있다.
	→ **offset을 사용**한다.
	- **Fragmentation offset은 IP header에 존재.**
- [MTU 참고](https://www.cloudflare.com/ko-kr/learning/network-layer/what-is-mtu/)

#### Fragmentation example
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240515225303.png|450]]

- **offset : 내가 보낸 데이터의 첫 번째 주소.**

> [!note]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605212433.png|300]]


#### Detailed fragmentation example
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240515225412.png|500]]


### Options
- IPv4 데이터그램의 헤더는 고정 부분(fixed part)과 가변 부분(variable part)의 두 부분으로 구성된다.
- **고정 부분(base header)은 20byte 길이**이다.
- 가변 부분은 헤더의 경계를 유지하기 위해 최대 **40byte**(4바이트의 배수로)가 될 수 있는 옵션으로 구성된다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240520194143.png|400]]

> [!info]
> - 옵션을 처리하는 순간 라우터의 성능이 떨어져서 현재 옵션은 실제로 사용하지 않는다.


### Security of IPv4 Datagrams
- IPv4 프로토콜과 인터넷 전체는 인터넷 사용자들이 서로를 신뢰하면서 시작됐다.
- **IPv4 프로토콜에는 어떤 보안도 제공되지 않았다.**
- 그러나 오늘날에는 상황이 달라져 인터넷이 더 이상 안전하지 않다.
- 네트워크 보안 전반과 IP 보안에 대해 논의 하겠지만, 여기서는 IP 프로토콜의 보안 문제와 해결 방안에 대해 간략하게 설명한다.
- 특히 IP 프로토콜에 적용되는 보안 문제에는 패킷 스니핑(packet sniffing), 패킷 변조(packet modification), IP 스푸핑(IP spoofing)의 세 가지가 있다.

> [!info]
> - 초반에 security 기능이 없었다. 
> - 기존 프로토콜을 바꾸지 않고 다른 프로토콜을 이용하여 IPv4를 보안한다.
> - best effort service : 최선형 서비스
> 	- IPv4 프로토콜은 최선을 다했기 때문에 다른 거에 대한 책임을 지지 않는다.
> 	- 에러를 검출하거나 고치는 등이 없다는 것.
> 	- → ICMP


### ICMPv4
- IPv4에는 오류 보고(error reporting) 또는 오류 수정(error-correcting) 메커니즘을 가지고 있지 않다.
- 또한 IP 프로토콜에는 호스트 및 관리 쿼리(management query)를 위한 메커니즘이 없다.
- **ICMPv4(Internet Control Message Protocol, 인터넷 제어 메시지 프로토콜)** 은 위의 두 가지 결함을 보완하기 위해 설계됐다.


#### Message
- ICMP 메시지는 **오류 보고 메시지(error-reporting message)** 와 **쿼리 메시지(query message)** 로 크게 두 가지 범주로 나뉜다.
- 오류 보고 메시지는 라우터 또는 호스트(destination)가 IP 패킷을 처리할 때 발생할 수 있는 문제를 보고한다.
- pair로 발생하는 쿼리 메시지는 호스트 또는 네트워크 관리자가 라우터 또는 다른 호스트로부터 특정 정보를 얻는 데 도움이 된다.

- 예를 들어 노드는 이웃을 발견할 수 있다. 
- 또한 호스트는 네트워크에서 라우터를 발견하고 라우터에 대해 알아볼 수 있으며 라우터는 노드가 자신의 메세지를 리디렉션(redirection, 다른 데로 보냄)하는 데 도움을 줄 수 있다.

> [!info]
> DOS : 한 서버에 ping 등 셔비스 등의 요청을 너무 많이 보내서 서버가 다른 것을 못하도록 막는다.


#### General format of ICMP messages
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240520225555.png|500]]


### Debugging Tools
- 인터넷에는 디버깅에 사용할 수 있는 몇 가지 도구가 있다.
- 호스트 또는 라우터의 실행 가능성을 확인할 수 있다.
- 디버깅에 **ICMP를 사용**하는 두 가지 도구 중에는 **ping**과 **traceroute**가 있다.


#### Example of ping
- 다음은 사이트에 핑 메시지를 보내는 방법을 보여준다.
- echo 요청 및 응답 메시지에서 식별자 필드를 설정하고 시퀀스 번호를 0부터 시작하여 새 메시지를 보낼 때마다 이 번호가 1씩 증가한다.
- ping은 왕복 시간을 계산할 수 있다.
- 메시지의 데이터 섹션에 전송 시간을 삽입한다.
- 패킷이 도착하면 출발 시간에서 도착 시간을 빼서 **왕복 시간(round trip time, rtt)** 를 구한다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240520230024.png|500]]


#### Example of traceroute program
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240520230119.png|500]]

- TTL을 1부터 늘려가며 **어느 라우터를 지나는 지 확인**할 수 있다.


## Network Layer : IPv6
### IPv6 Addressing
- IPv4에서 IPv6로 마이그레이션하는 주된 이유는 IPv4의 주소 공간이 작기 때문이다.
- 이 섹션에서는 IPv6의 넓은 주소 공간이 향후 주소 고갈을 방지하는 방법을 설명한다.
- 또한 새로운 주소 지정이 IPv4 주소 지정 메커니즘의 몇 가지 문제에 어떻게 대응하는지에 대해서도 설명한다.
- IPv6 주소의 길이는 **128bit** 또는 **16byte**(octets)로, **IPv4 주소 길이의 4배**이다.


### Representation
- 컴퓨터틑 일반적으로 주소를 2진수로 저장한다. 하지만 128bit를 사람이 쉽게 다룰 수 없다는 것은 명백하다.
- 사람이 처리할 때 IPv6 주소를 표현하기 위해 몇 가지 표기법이 제안되었다.
- 다음은 이러한 표기법 중 2진법과 콜론 16진법(colon hexadecimal)의 두 가지 표기법을 보여준다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240520230727.png|500]]

> [!summary]
> - 주소가 커지니까 주소는 많아지는데 사람이 읽고 직접 사용하기가 어렵다.
> - → 주소 자동 할당 방법 필요
> - 또 대부분의 주소가 0으로 채워진다.


### Address Space
- IPv6 주소 공간에는 $2^{128}$개의 주소가 있다.
- 이 주소 공간은 IPv4의 주소의 296배로 주소 고갈이 전혀 없으면 주소 공간의 크기는 다음과 같다.
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240520231620.png|450]]


### Address Space Allocation
- IPv4의 주소 공간과 마찬가지로 IPv6의 주소 공간은 다양한 크기의 여러 블록으로 나뉘며 각 블록은 특별한 용도로 할당된다.
- 대부분의 블록은 아직 할당되지 않았으며 향후 사용을 위해 따로 보관되어 있다.
- Prefixes for assigned IPv6 addresses
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240520232035.png|500]]
	- 위 표에서는 할당된 블록을 보여준다.
	- 이 표의 마지막 열은 각 블록이 전체 주소 공간에서 차지하는 비율을 보여준다.

#### Global Unicast Address
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521105925.png|500]]

- 이걸 매핑 시키는 것도 어렵다(unique 해야 함).
	 → 원래의 **unique한 주소(MAC : datalink)를 이용** 한다.
- MAC주소를 확장하여 사용한다.
- Site : 네트워크를 모아 놓은 걸 site라는 개념으로 정의하고 넓혀서 사용한다.


#### Mapping for Ethernet MAC
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521110344.png|500]]

- 기존에 있던 unique한 주소(MAC주소)를 이용해서 주소를 할당한다.


### Auto-configuration
- 주소를 manual하게(수동으로) 받는 건 의미가 없다.
- IPv6 주소 지정의 흥미로운 기능 중 하나는 호스트의 자동 구성(auto-configuration)이다.
- IPv4에서 설명했듯이 호스트와 라우터는 원래 네트워크 관리자가 수동으로 구성한다.
- 하지만 **DHCP(동적 호스트 구성 프로토콜, 주소 자동 할당)** 를 사용하여 네트워크에 가입하는 호스트에 IPv4 주소를 할당할 수 있다.
- **IPv6에서도 DHCP 프로토콜을 사용하여 호스트에 IPv6 주소를 할당**할 수 있지만 호스트가 직접 구성할 수도 있다.

### The IPv6 Protocol
- IPv6 주소 크기를 변경하려면 IPv4 패킷 형식의 변경이 필요한다.
- IPv6 설계자는 변경이 불가피한 지금 다른 단점에 대한 보완책을 구현하기로 결정했다.
- 다음은 주소 크기 및 형식 변경 외에 프로토콜에 구현된 다른 변경 사항을 보여준다.


### IPv6 datagram
- 결론적으로 주소가 커지는 게 좋은 것 같지만 모든 네트워크에 부담이 됨.
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521111403.png|500]]

- **기본 헤더(Base header)가 40bytes**
- 주소가 차지하는 공간이 늘어난 것.(32bit → 128bit)


#### Payload in an IPv6 datagram
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521111535.png|450]]


#### Extension Header
- IPv6 패킷은 기본 헤더와 일부 확장 헤더로 구성된다.
- **기본 헤더의 길이는 40byte**로 고정되어 있다.
- 그러나 IP datagram에 더 많은 기능을 부여하기 위해 기본 헤더 뒤에 최대 6개의 확장 헤더를 추가할 수 있다.
- 이러한 헤더 중 다수는 IPv4에서 옵션이다.
- 6가지 유형의 확장 헤더가 정의되어 있다.
	- hop-by-hop option, source routing, fragmentation, authentication, encrypted security payload, destination option이 있다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521112050.png|550]]


### ICMPv6 Protocol
> [!abstract]
> - error reporting 해주는 IPv6

- TCP/IP protocol suite version6에서 수정된 또 다른 프로토콜은 ICMP이다.
- 이 새로운 버전인 ICMPv6는 version4와 동일한 전략과 목적을 따른다.
- 하지만 version 4에서는 독립적이었던 일부 프로토콜이 이제 ICMPv6의 일부가 되었고, 더 유용하도록 몇 가지 새로운 메시지가 추가되어 ICMPv4보다 더 복잡해졌다.


### Comparision of network layer in version 4 and version 6
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521112659.png|500]]


### Transition From IPv4 to IPv6
- **IPv4와 IPv6 사이는 통신이 안된다** 
	- 프로토콜이 완전 다른 것.
	- 전 세계가 한 번에 바꾸지 않는 이상 통신이 안된다.
- 새 버전의 IP 프로토콜이 있지만 어떻게 하면 IPv4 사용을 중단하고 IPv6를 사용하도록 전환할 수 있나?
	- 어떻게 그럼 이걸 바꿔나가나?
- 인터넷에서 IPv4와 IPv6 시스템 간의 문제를 방지하려면 전환이 원활하게 이루어져야 한다.


### Transition Strategies
- 전환(transition)을 위한 세 가지 전략이 고안되었다.
	- dual stack
	- tunneling
	- header translation
- 전환 기간 동안 이 세가지 전략 중 하나 또는 모두를 구현할 수 있다.


#### Dual stack
- **듀얼 스택(dual stack)** 을 사용하여 IPv4, IPv6로 둘 다 통신할 수 있도록 한다.
	- 근데 이건 그럼 모든 기기에서 둘 다 통신할 수 있도록 하는 것을 가지고 있어야 한다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521113438.png|400]]


#### Tunneling strategy
- 터널링
- **헤더를 IPv4로 한 번 더 씌운다.**

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521113517.png|400]]

> [!note]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605220725.png|300]]



#### Header translation strategy
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521113603.png|500]]

- 헤더를 바꾼다.
- **IPv6 주소를 IPv4 주소로** 바꿔야 한다.
- IPv6(128bit) → IPv4(32bit)
- **IPv6주소를 만들 때 IPv4 주소를 포함 시켜서 빼서 사용**한다.