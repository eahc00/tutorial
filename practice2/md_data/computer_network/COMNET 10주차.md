
## Network Layer : Logical Addressing
- Logical Address : 바뀔 수 있음
- Physical Address : 변하지 않는다.


### Objective
- 첫 번째 섹션에서는 Network layer에 의해 제공하는 서비스를 정의하여 네트워크 계층을 소개한다. 
	- 먼저 패킷화(packetizing)에 대해 설명한다. 
	- forwarding과 routing에 대해 설명하고 두 가지를 비교한다. 
	- flow, error, congestion control(혼잡 제어)과 같은 다른 서비스에 대해 간략하게 설명한다.

- 두 번째 섹션에서는 네트워크 계층에서 발생하는 packet switching에 대해 설명한다.
	- 이 섹션에서는 packet switching의 datagram 접근 방식과 가상 회로(virtual-circuit) 접근 방식에 대해 자세히 설명한다.

- 세 번째 섹션에서는 네트워크 계층의 성능에 대해 설명한다.
	- 네트워크 계층 통신에서 발생하는 다양한 delay에 대해 설명하고 또한 패킷 손실 문제도 언급한다.
	- 마지막으로 네트워크 계층에서의 혼잡 제어(congestion control) 문제에 대해 설명한다.

- 네 번째 섹션에서는 네트워크 계층에서 가장 중요한 문제인 IPv4 주소 지정에 대해 설명한다. 
	- 먼저 주소 공간에 대해 설명한다.
	- 과거에 사용됐지만 classless addressing을 이해하는 데 유용한 classful addressing 지정에 대해 간략하게 설명한다.
	- 이후 classless addressing으로 이동하여 이 주제와 관련된 몇 가지 문제를 설명한다.
	- 그런 다음 organization에서 주소를 동적으로 할당하는 데 사용할 수 있는 DHCP에 대해 설명한다.
	- 마지막으로 주소의 부족을 어느 정도 해소하는 데 사용할 수 있는 NAT에 대해 설명한다.

- 다섯 번째 섹션에서는 네트워크 계층 패킷 전달에 대해 설명한다.
	- 먼저 패킷에서의 destination address를 기반으로 forwarding을 수행하는 방법을 보인다.
	- 그런 다음 레이블을 사용하여 포워딩을 수행하는 방법에 대해 설명한다.


### Packetizing
- 패킷 단위로 나누는 것.
- 네트워크 계층의 첫 번째 기능은 **패킷화(packetizing)** 이다.
	- source에서 네트워크 계층 패킷으로 payload(데이터)를 **캡슐화**하고 destination에서는 네트워크 계층 패킷으로부터 payload를 **decapsulating**하는 것이다.
	- source 주소와 destination 주소가 필요(IP address)
- 즉, 네트워크 계층의 한 가지 기능은 payload를 변경하거나 사용하지 않고 source에서 destination까지 전달하는 것이다.
- 네트워크 계층은 내용을 변경하거나 사용하지 않고 송신자에서 수신자에게 소포를 전달하는 우체국과 같은 운송업체의 서비스를 수행하고 있다.


### Two key network-layer functions
- **Forwarding(포워딩)**
	- 라우터 입력으로부터 적절한 라우터 출력으로 **패킷 이동**
	- 실제 패킷을 옮기는 것

- **Routing(라우팅)**
	- source에서 destination까지 **패킷이 이동하는 경로를 설정**
	- 패킷에서 이동할 route를 찾는 것.


### Forwarding process
- 목적지를 보고 어느 링크로 가야 하는지 찾고(routing) 이동 시키는 것(forwarding)
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240507121741.png|300]]


### Packet Switching
- 이전 섹션의 라우팅 및 포워딩에 대한 설명에서 네트워크 계층에서 일종의 **스위칭(switching)** 이 발생한다는 것을 유추할 수 있다.
- 사실 라우터는 전기 스위치가 입력과 출력을 연결하여 전기가 흐르도록 하는 것처럼 입력 포트와 출력 포트(또는 출력 포트 집합) 사이에 **연결을 생성하는 스위치**이다.


#### Datagram Approach
- 인터넷이 시작되었을 때 이것을 간단하게 만들기 위해 네트워크 계층은 **각 패킷을 독립적으로 처리하고 각 패킷은 다른 패킷과 연관이 없는 connectionless service**를 제공하도록 설계되었다.
- 네트워크 계층은 source에서 destination까지 **패킷을 전달하는 역할만 담당**한다는 아이디어이다.
- 이 접근 방식에서는 메시지의 패킷이 목적지까지 동일한 경로로 이동할 수도 있고 그렇지 않을 수도 있다.


#### A connectionless packet-switched network
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240507130808.png|500]]

- 받는 쪽에서는 패킷들을 순서대로 맞춰줄 수 없다.
- 순서를 맞춰야 한다면 상위 계층(layer)에 순서를 맞춰주는 기능을 추가해야 한다.


#### Forwarding process in a router when used in a connectionless network
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240507130941.png|450]]

- 목적지 주소를 보고 **Forwarding table**에서 찾아서 전송한다. 
	- Forwarding table design에 따라 성능이 달라진다.
	- router에서 내가 갈 경로를 찾기 위해 queuing time 또한 필요하다.


### Network-Layer Performance
- 네트워크 계층의 서비스를 사용하는 상위 계층 프로토콜은 이상적인 서비스를 받기를 기대하지만 네트워크 계층은 완벽하지 않다.
- 네트워크의 성능은 **delay, throughput, packet loss**로 측정할 수 있다.
- **혼잡 제어(Congestion control)** 는 성능을 개선할 수 있는 문제이다.


#### Delay
- 우리는 전부 네트워크에서 즉각적인 응답을 기대하지만, 패킷은 source에서 destination까지 **지연(delay)** 이 발생할 수 있다.
- 네트워크의 지연은 **전송 지연(transmission delay), 전파 지연(propagation delay), 프로세싱 지연(processing delay), 대기열 지연(queuing delay)** 의 네 가지 유형으로 나눌 수 있다.
	- **queuing delay**가 성능 결정에 가장 큰 영향을 미친다.


#### Throughput
- 네트워크의 어느 지점에서의 처리량(throughput)은 **1초 동안 해당 지점을 통과하는 비트 수**로 정의되며, 이는 실제로 해당 지점에서의 데이터 전송 속도이다.
- source에서 destination까지의 경로에서 패킷은 **각각 다른 전송 속도를 가진 여러 링크(네트워크)를 통과**할 수 있다.

##### Throughput in a path with three links a series
- 그렇다면 전체 경로의 처리량을 어떻게 확인할 수 있나?
	- 각각 다른 전송 속도를 가진 3개의 링크가 있다고 가정하자.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240507131821.png|450]]

- 내가 지나가는 링크들의 **transmission rate의 mimimum**이 **전체 경로의 throughput**이 된다.
	- 위 사진에서는 100Kbps가 전체 경로의 throughput


#### Packet Loss
- 통신 성능에 심각한 영향을 미치는 또 다른 문제는 전송 중 **손실되는 패킷 수**이다.
- 라우터가 다른 패킷을 처리하는 동안 패킷을 수신하면 수신된 패킷은 입력 버퍼(input buffer)에서 차례를 기다려야 한다. 
- 하지만 라우터는 크기 제한이 있는 입력 버퍼를 가진다.
- 버퍼가 가득 차서 다음 패킷을 삭제해야(버려야) 할 때가 올 수 있다. 
- 패킷 손실이 인터넷 네트워크 계층에 미치는 영향은 패킷을 **재전송**해야 한다는 것이며, 이로 인해 overflow가 발생하여 더 많은 패킷 손실이 발생할 수 있다는 것이다.


### Congestion Control
- **혼잡 제어는 성능 향상을 위한 메커니즘**이다.
- 네트워크 계층에서의 혼잡(congestion)은 인터넷 모델에서 명시적으로 다루고 있지는 않지만, 이 계층에서의 혼잡에 대한 연구는 전송 계층(transport layer)에서의 혼잡 원인을 더 잘 이해하고 네트워크 계층에서 사용할 수 있는 해결책을 찾는 데 도움이 될 수 있다.
- 네트워크 계층의 혼잡(정체)은 **처리량과 지연**이라는 두 가지 문제와 연관이 있다.  


#### Packet delay and throughput as functions of load
- 내가 보낼 수 있는 최대의 양을 보내면 throughput이 최대가 된다. 
- capacity를 넘어가면 혼잡(Conjestion)이 발생한다.
	- 혼잡 발생 
		→ packet lost(패킷 손실 발생) 
		→ **delay가 측정 불가이기 때문에 무한대**가 된다. 
		→ packet 재전송 필요 
		→ **throughput도 떨어지게 된다.**

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240507133118.png|450]]

> [!tip]
> - 전송 데이터의 양이 capacity 안에 들어오도록 해야 한다.(transport layer에 이런 기능이 있다.)


#### Backpressure method for alleviating congestion
- 혼잡 제어를 위한 Backpressure method
- transport layer에 의해 제공된다.
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240507133702.png|400]]

- 데이터를 줄여달라고 한 **이전 라우터에게 한 단계씩 요청**하여 source에까지 요청을 보낸다.


#### Choke packet
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240507133819.png|400]]

- 데이터를 줄여달라고 **source에게 바로 요청**한다.
- 마찬가지로 transport layer에 의해 제공된다.


### IPv4 Addresses
- 각 **디바이스의 인터넷으로의 연결을 식별**하기 위해 TCP/IP protocol suite의 **IP layer에서 사용되는 식별자**를 인터넷 주소 또는 IP address라고 한다.
- IPv4 주소는 호스트 또는 라우터의 인터넷로의 연결을 고유하고(유일하고) 보편적으로 정의하는 **32-bit(4byte)주소**이다.
- IP 주소는 호스트나 라우터가 아닌 **연결(connection)의 주소**이다.

### Address Space
- 주소를 정의하는 IPv4와 같은 프로토콜은 **주소 공간(Address Space)** 을 가진다.
- 주소 공간은 **프로토콜에 의해 사용되는 주소의 총 개수**이다.
- 프로토콜이 비트를 사용하여 주소를 정의하는 경우 각 비트는 두 가지 값(0 또는 1)을 가질 수 있으므로 주소 공간은 $2^b$이다.
- **IPv4는 32bit 주소**를 사용하므로 주소 공간은 $2^{32}$또는 4,294,967,296(40억 개 이상)이다.
- 제한이 없다면, 40억 개 이상의 디바이스를 인터넷에 연결할 수 있다.

#### Three different notations in IPv4 addressing
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240507212831.png|450]]

- 32bit : 4byte
- 한 바이트 당 0~255의 값을 가진다.


#### Hierarchy in addressing
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240507213021.png|450]]

- **Prefix**
	- 네트워크 주소
	- 네트워크를 정의
- **Suffix**
	- 호스트 주소
	- 노드로의 연결을 정의


### Classful Addressing
- classful 주소 지정 방식
	- 인터넷이 시작되었을 때 IPv4 주소는 **fixed-length prefix**로 설계되었다.
	- 소규모 및 대규모 네트워크를 모두 수용하기 위해 하나의 fixed-length prefix 대신 3개의 fixed-length prefix(n = 8, n = 16, n = 24)로 설계됐다.
	- 전체 주소 공간은 5개의 클래스(class A, B, C, D ,E)로 나누어졌다.
	- classful 주소 지정은 과거에 쓰였지만, 이후 설명하는 classless 주소 지정을 이해하는 데 도움이 된다.


#### Occupation of the address space in classful addressing
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240507214359.png|600]]


- 각 class별로 prefix가 네트워크 주소, suffix가 호스트 주소가 된다.
	- 예를 들어 A에서는 $2^{24}$개 만큼의 호스트가 있을 수 있다. → B, C로 갈수록 작은 네트워크
- **first byte의 수로 class를 판별 가능**하다.


![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240507214556.png|400]]

> [!problem]
> - A : $2^{24}$만큼의 호스트 주소를 가지는 굉장히 큰 네트워크이다.
> 	- 만약 이 네트워크를 할당 받고 다 쓰지 않으면 주소를 낭비하는 것.

> [!solution]
> - A의 prefix를 8bit 더 추가하면 작은 네트워크를 더 추가하는 효과가 발휘된다.
> 	- 한 네트워크 당 가질 수 있는 호스트의 수는 줄어들지만 네트워크가 많아지는 것.(총합은 같음)
> - 큰 네트워크를 작은 네트워크로 나눠 쓰는 것
> 	- 주소 낭비를 줄일 수 있다.
> - 내가 붙이는 호스트 수에 따라 네트워크 주소(prefix의 길이)를 조절해야   
> → 이 방식이 Classless



### Classless Addressing
- 인터넷의 성장과 함께 장기적인 해결책으로 더 큰 주소 공간이 필요하다는 것이 명백해졌다.
- 그러나 주소 공간이 커지면 IP 주소의 길이도 늘어나야 하므로 IP 패킷의 형식도 변경해야 한다.
- 장기적인 해결책은 이미 고안되어 IPv6라고 불리지만, 동일한 주소 공간을 사용하되 각 organization(조직)에 공평한 몫을 제공하기 위해 주소 분배를 변경하는 단기적인 해결책도 고안되었다.
- 단기적인 해결책은 여전히 IPv4 주소를 사용하지만, **classless 주소 지정**이라는 방법을 사용한다.

> [!abstract]
>  - 네트워크 주소(prefix length)가 고정 되어 있지 않다.
> 	 - 네트워크 주소에 낭비가 없도록 가변적(variable-length prefix)으로


#### Variable-length blocks in classless addressing
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240507215550.png|400]]

- Address space에 여러 길이의 Block이 존재한다.


#### Slash notation(CIDR)
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240507215636.png|450]]

- prefix length를 "/" 뒤에 표기한다.
	- **prefix length** : 네트워크 주소의 bit 수
	- prefix length를 **호스트 수에 맞춰서 가변적으로 사용**하게끔 한다.


![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240507215746.png|400]]

- 위의 예시와 같이 사용
- **Subnet Mask**
	- 처음부터 prefix length만큼의 비트가 1이고 나머지가 0인 Subnet Mask를 이용하여 **네트워크 주소를 걸러낸다**(prefix 부분만 걸러내는 것).


#### Information extraction in classless addressing
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240507220013.png|450]]

- **호스트 주소(Suffix)** 가 모두 0인 것부터 호스트 주소(Suffix)가 다 1인 것까지 첫 주소와 끝 주소가 정해진다.


#### Two levels of hierarchy in an IPv4 address
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240507220611.png|300]]

- Area code(지역 번호)
- Exchange office(전화국)
- Subsciber

> [!my_question]
> level이 세 갠데 이게 왜 Two level hierarchy?? Three level 아닌지
> - 이거는 예시고 IPv4에서는 네트워크 주소 - 호스트 주소 two level을 사용


#### Configuration and addresses in a subnetted network
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240507220251.png|500]]

- prefix length가 26인 network를 27인 **subnetwork 2개**로 나누고
- 다시 27인 network를 28인 network 두 개로 나눈다.

- prefix가 26인 network는 내부에 호스트 64개를 가질 수 있다.
- 26을 두 개로 나누려면 27을 prefix length로 주고
- 또 27을 두 개로 나누려면 28을 prefix length로 주면 된다.


#### Three-level hierarchy in an IPv4 address
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240507220807.png|570]]

- Subnet 1
	- 26 네트워크를 두 개로 나눴다는 말
- Subnets 2 and 3
	- 26 네트워크를 두 개로 나누고
	- 이걸 또 다시 두 개로 나눴다는 말


##### Example
- **ISP(Internet Service Provider)** 는 199.100.0.0/16(65,536개 주소 = $2^{16}$)로 시작하는 주소 블록을 부여 받는다.
- ISP는 아래와 같이 세 가지 customer 그룹에 이 주소를 배포해야 한다.
	- 첫 번째 그룹에는 64 customer가 있고, 각각 256개의 주소가 필요하다.
	- 두 번째 그룹에는 128 customer가 있고, 각각 128개의 주소가 필요하다.
	- 세 번째 그룹에는 128 customer가 있고, 각각 64개의 주소가 필요하다.
- 하위 블록(subblock)을 설계하고 이러한 할당 후에도 사용할 수 있는 주소가 몇 개 있는지 알아내라.

> [!solution]
> - Group1. 64 customer * 256개의 주소(=$2^8$)  
> 	- prefix length = 32 - 8 = 24
> 	- 첫 번째 customer에 대해서만 일단 생각해보면 (199.100.0.0/24 ~ 199.100.0.255/24)의 주소 공간을 할당 받는다.
> 	- 이러한 customer가 64개 존재하니 최종적으로 Group1에는 (199.100.0.0/24 ~ 199.100.63.255/24)의 주소 공간이 할당된다.
> 	- Group1에 할당된 주소 공간은 64 * 256 = 16,384개가 된다.    

> [!solution]
> - Group2. 128 customer * 128개의 주소(=$2^7$)
> 	- prefix length = 32 - 7 = 25
> 	- 첫 번째와 두 번째 customer에 대해 생각해보자.
> 		- 첫 번째 customer는 Group1에서 사용된 주소를 제외하고 (199.100.64.0/25 ~ 199.100.64.127/25)의 주소 공간을 할당 받는다.
> 		- 두 번째 customer는 이어서 (199.100.64.128/25 ~ 199.100.64.255/25)까지의 주소 공간을 할당 받는다. 맨 뒤 8비트를 두 customer가 나누어 쓰게 된다.(suffix 한 숫자에 2개씩 할당된다는 뜻)
> 	- 이러한 customer가 128개 존재하니 최종적으로 (199.100.64.0/25 ~ 199.100.127.255/25)의 주소 공간이 할당된다.
> 	- Group2에 할당된 주소 공간은 128 * 128 = 16,384개가 된다.    

> [!solution]
> - Group3. 64 customer * 64개의 주소(=$2^6$)
> 	- prefix length = 32 - 6 = 26
> 	- Group2의 주소공간을 할당한 것과 같이 생각하면 맨 뒤 8비트를 4 customer가 나누어쓰므로 128 / 4 = 32(suffix 한 숫자에 4개씩 할당받는 뜻) 이고, 즉 (199.100.128.0/26 ~ 199.100.159.255/26)의 공간을 Group3이 할당받는다.
> 	- Groupt3에 할당된 공간은 64 * 64 = 8,192이다.

> [!solution]
> - 남는 공간은 199.100.160.0 ~ 199.100.255.255이다.
> 	- 즉 남는 공간은 96 * 256 = 24,576이 된다.

> [!solution]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240508214035.png|400]]

- 반 씩 네트워크를 나눠가는 효과가 있다.


##### Example2
- classless address가 167.199.170.82/27로 지정된다. 
- 호스트의 주소 수는 $2^{32-27} - 2^5 = 32$개 이다.
- 첫 번째 주소는 처음 27bit를 유지하고 나머지 비트를 0으로 바꾸면 찾을 수 있다.
- 마지막 주소는 처음 27bit를 유지하고 나머지 비트를 1로 바꾸면 찾을 수 있다.

> [!example]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240508214837.png|400]]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240508214853.png|400]]

- 위에서 찾은 첫 번째 주소와 마지막 주소 사이에 범위 내에 있는 것은 **나와 같은 네트워크**에 있는 것.
	- data link로 직접 통신이 가능하다는 것이다.
- 다른 네트워크에 있는 것과는 라우터를 통해서 통신해야 한다.
- 네트워크 주소로 같은 네트워크에 있는지 없는지 알 수 있다.


##### Example3
- classless address에서 주소 자체로는 주소가 속한 블록을 정의할 수 없다.
- 예를 들어 주소 230.8.24.56은 여러 블록에 속할 수 있다. 
- 아래는 prefix 값에 따라 그 중 일부를 표시한 것이다.
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240508225350.png|450]]


#### Network address
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240508225438.png|450]]

- 전체 주소가 아닌 **network 주소로 찾아가서** 같은 network 내에서는 직접 통신을 하면 된다.
	- **network 주소만 보면 된다**는 것.
- 이렇게 하면 **훨씬 더 작은 forwarding table을 구성**할 수 있다.


##### Example
- 한 ISP(18.14.12.0)가 1,000개의 주소 블록을 요청했다.
- 1,000은 2의 거듭제곱이 아니므로 1,024개의 주소가 부여된다.
- prefix length는 $n = 32 - log_21024 = 22$로 계산된다. 
	- host주소로 10bit가 사용된다.
- 사용 가능한 블록인 18.14.12.0/22가 ISP에 부여된다.
- 첫 번째 주소는 십진수로 302,910,464이며 1,024로 나눌 수 있음을 알 수 있다.

##### Example
- organization에 시작 주소가 14.24.74.0/24인 주소 블록이 부여된다.
- organization은 3개의 address subblock을 가져야 한다.
	- 10개의 주소로 구성된 subblock
	- 60개의 주소로 구성된 subblock
	- 120개 주소로 구성된 subblock
- subblock을 설계하라.

> [!solution]
> - 이 블록에는 $2^{32-24} = 256$개의 주소가 있다.
> - 첫 번째 주소는 14.24.74.0/24이고 마지막 주소는 14.24.74.255/24이다.
> - 가장 큰 블록부터 가장 작은 블록까지 subblock에 주소를 할당한다.

> [!solution]
> - 120개 주소로 구성된 subblock 주소 할당
> 	- 120개의 주소가 요구되는 가장 큰 subblock의 주소 수(120)는 2의 거듭제곱이 아니므로 128개의 주소를 할당한다.
> 	- 이 subnet의 subnet mask(=prefix length)는 $n = 32 - log_2128 = 25$로 구할 수 있다.
> 	- 이 블록의 첫 번째 주소는 14.24.74.0/25이고 마지막 주소는 14.24.74.127/25이다.
> - 60개 주소로 구성된 subblock 주소 할당
> 	- 60개의 주소가 요구되는 두 번째로 큰 subblock의 주소 수(60)는 2의 거듭제곱이 아니므로 64개의 주소를 할당한다.
> 	- 이 subnet의 subnet mask는 $n = 32 - log_264 = 26$로 구할 수 있다.
> 	- 이 블록의 첫 번째 주소는 14.24.74.128/26이고 마지막 주소는 14.24.74.191/26이다.
> - 10개 주소로 구성된 subblock 주소 할당
> 	- 10개의 주소가 요구되는 세 번째 subblock의 주소 수(16)는 2의 거듭제곱이 아니므로 16개의 주소를 할당한다.
> 	- 이 subnet의 subnet mask는 $n = 32 - log_216 = 28$로 구할 수 있다.
> 	- 이 블록의 첫 번째 주소는 14.24.74.192/28이고 마지막 주소는 14.24.74.207/28이다.
> - 남는 주소
> 	- 이전s subblock의 주소를 더하면 결과는 208개의 주소가 되며, 이는 48개의 주소가 예비로 남는다는 것이다.
> 	- 남는 주소의 첫 번째 주소는 14.24.74.208이고 마지막 주소는 14.24.74.255이다.
> 	- prefix length에 대해서는 아직 알 수 없다.

> [!solution]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240508233307.png|400]]

- ISP는 이러한 네 개의 블록들을 하나의 단일 블록으로 결합하여 더 큰 블록으로 바깥에 나타낸다.
- 이 더 큰 블록으로 향하는 모든 패킷은 이 ISP로 전송되어야 한다.
- 패킷을 **적절한 organization으로 전달하는 것은 ISP의 책임**이다. 
- 이는 우편 네트워크에서 볼 수 있는 라우팅과 유사하다. 
	- 국가 외부에서 들어오는 모든 소포는 먼저 수도로 보내진 다음 해당 목적지로 배포된다.

> [!example]
> - Example of address aggregation(군집)
> 	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240508233737.png|450]]
> 	- 24 block을 26 subblock 4개로 나눈 것.
> 	- 24 네 개보다 26짜리 하나로 뭉쳐서 밖에 보내주면 **forwarding table의 entry 수가 줄어들어서** 더 효율적이다.
> 		- forwarding table 탐색 시간이 줄어듬
> 		- **밖으로 보낼 때는 최대한 entry수를 줄여서** 보내야 
> 	- 이후 26으로 내부에서 알아서 나눈다.


### DHCP
- 조직(orgrnization)에 주소 불록이 할당 된 후 네트워크 관리자(administration)은 개별 호스트 또는 라우터에 주소를 수동으로 할당 할 수 있다.
- 그러나 조직 내 주소 할당은 **DHCP(Dynamic Host Configuration Protocol** : 동적 호스트 구성 프로토콜)를 사용하여 자동으로 수행할 수 있다.
- **DHCP는 client-server 패러다임을 사용하는 응용 계층 프로그램**으로, 네트워크 계층에서 TCP/IP를 실제로 지원(help)한다.

> [!info]
> - 내 IP 주소 
> 	- 나의 주소를 알아올 수 있다
> - prefix 서브넷 마스크
> 	- IP 주소만 알려주면 여러 네트워크에 속할 수 있으므로 prefix length를 알려줘야
> - default gateway 
> 	- 나를 다른 네트워크에 연결해줄 수 있는 router 주소가 필요
> - 위 세 가지 주소를 자동 할당 해주는 것.


#### DHCP client-server scenario
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240508235213.png|450]]

- DHCP 서버에게 **내가 사용할 IP 주소를 할당 받는다**.


#### DHCP message format
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240508235309.png|300]]

- **DHCP header**


#### Operatioin in DHCP
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240508235347.png|450]]

> [!my_question]
> - DHCP는 헤더의 값이 바뀌면서 주소를 할당받고 통신하는 건지?
> 	- 데이터 전송 목적이 아니기 때문에 헤더 값만 바꾸면서 통신하는 것


### NAT : Network Address Translation
- 대부분의 경우 소규모 네트워크에서는 일부 컴퓨터만 동시에 인터넷에 액세스하면 된다.
- **프라이빗 IP(private address)와 퍼블릭 IP(universal address) 간의 매핑을 제공**할 수 있는 기술이 **NAT(Network Address Transloation, 네트워크 주소 변환)** 이다.

- NAT를 사용하면 사이트에서 내부 통신을 위한 프라이빗 IP 집합과 전 세계와의 통신을 위한 global Internet 주소 집합(적어도 하나 이상)을 사용할 수 있다.


#### Operation of NAT
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240515161344.png|350]]

- NAT ⇄ Internet : 외부 연결 네트워크
- **외부에서의 연결**은 호스트가 아니라 **네트워크를 찾아오는 것**
- **NAT : 내부와 외부를 연결**


#### Address translation
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240515161601.png|400]]

- NAT router의 주소는 이 네트워크의 주소이다.
	- 위 그림에서 200.24.5.8
	- 외부에서 온 데이터는 **네트워크 내부에서 프라이빗 IP로 바꿔서 알아서 처리**한다.

- NAT를 사용하는 이유
	- NAT를 쓰면 **부족한 주소 공간을 많이 쓸 수 있다.**
	- 각각 unique한 주소를 쓰는 게 아닌 연결된 네트워크 주소(퍼블릭 IP주소) 하나로 내부 네트워크(프라이빗 네트워크)를 커버할 수 있다.


#### Translation
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240515162249.png||400]]

- private address와 universal address의 **mapping table** 필요.
- 만약 여러 프라이빗 IP 주소가 하나의 universal IP로 바뀌면 구별을 못하는 문제가 생긴다.
	- 추가적인 정보를 넣어줘야 한다.(**포트 번호**, 프로세스 식별)


##### Five-column translation table
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240515162428.png|400]]

- port 번호는 **운영체제에서 알아서 할당**해준다.
- entry가 5개인 형태로 table을 변경


### Forwarding of IP Packets
- 이 chapter의 앞부분에서 네트워크 계층에서의 포워딩 개념에 대해 설명했다.
- 이 섹션에서는 이 개념을 확장하여 포워딩에서의 IP 주소의 역할을 포함한다.
- 앞서 설명한 것처럼 포워딩은 패킷을 목적지까지의 경로에 배치 시키는 것을 의미한다.
	- 목적지와 테이블 보고 어디로 가야되는지 결정


#### Destination Address Forwarding
- **목적지만을 생각**한다. 목적지만을 보고 어디로 갈지 결정

- 먼저 destination address 기반 forwarding에 대해 설명한다. 이는 오늘날 널리 사용되는 전통적인 접근 방식이다.
- 이 경우 포워딩을 수행하려면 호스트 또는 라우터에 포워딩 테이블이 있어야 한다.
- 호스트가 전송할 패킷이 있거나 라우터가 전달할 패킷을 수신하면 이 테이블을 살펴보고 **패킷을 전달할 다음 hop을 찾는다**.


#### Simplified forwarding module in classless address
- **랴우터는 내가 데이터를 어디로 보낼지(어떤 인터페이스로 갈지)** 를 가지고 있어야 한다.
- 내가 어느 네트워크에 속하는지는 **서브넷 마스크(subnet mask)** 로 알아낼 수 있다.
	- 만약 destination 주소에 **서브넷 마스킹을 했을 때 나와 같으면 ( = 같은 네트워크에 존재)** 내가 받아서 그 쪽(목적지쪽) 인터페이스로 보내주면 된다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240515163606.png|400]]

> [!my_question]
> - interface : Network interface(NIC)??
> - MAC주소는 NIC마다 할당.
> - IP는????

> [!answer]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605162103.png|400]]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605162135.png|400]]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605162233.png|400]]


#### Forwarding Table
- configuration을 사용하여 라우터 R1에 대한 **포워딩 테이블**을 만든다.
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240515163953.png|400]]
	- default
		- 모르는 거 : 네트워크 적용했을 때 아무것도 안 걸리면 보낼 인터페이스, 주소.
		- default는 모든 서브넷이 0. **결과도 0이여서 모든 주소가 다 걸린다**. prefix가 모두 0인것.
		- 다른 네트워크와 연결 돼있다.
	- 위와 같은 테이블 구성으로 entry를 줄여서 entry 유지 비용을 낮춘다.
	- 참고 
		- mask가 클수록 작은 네트워크
		- 즉, 좀 더 나한테 정확한 네트워크이다.
		- prefix가 길면 길수록 정확한 네트워크이다.


> [!my_question]
> - default에서 Next hop에 있는 거는 다음 라우터 주소??
> - 인터페이스가 정확히 뭔지. 주소랑은 뭐가 다른 건지

> [!answer]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605162250.png|400]]
> - 따라서, 인터페이스는 데이터가 라우터를 떠나거나 들어오는 출입구이며, 다음 홉은 데이터가 목적지로 가는 도중에 거쳐야 하는 다음 라우터를 의미한다.


##### Configuration

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240515164820.png|400]]

- 위 그림에서는 라우터가 네 개의 인터페이스를 가진다.


#### Routing Decision
> [!example]
> - 목적지 주소 180.70.65.140을 가진 패킷이 위 표에서의 R1 router에 도착했을 때의 forwarding process

> [!solution]
> - 라우터는 다음 과정을 수행한다.
> 	1. 목적지 주소에 첫 번째 마스크(/26)가 적용되면 그 결과는 180.70.65.128로, 테이블에 연관된 네트워크 주소와 맞지 않는다. 
> 	2. 목적지 주소에 두 번째 마스크(/25)가 적용되면 그 결과는 180.70.65.128로. 연관된 네크워크 주소와 일치한다. 패킷을 forwarding하기 위해 next-hop address(다음 hop 주소)와 인터페이스 번호 $m_0$가 뽑힌다.


##### Address aggregation
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240515171254.png|400]]

- 주소 군집
- 이런 식으로 각 라우터 fowarding table의 entry를 줄인다.


##### Longest mask matching
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240515171507.png|400]]

- 가장 prefix가 높은 걸 찾아야
- fowarding table entry에서 여러 개에서 일치하는 네트워크가 겹쳐도 **prefix가 가장 긴 것을 선택**한다.
	- mask가 클수록 작은 네트워크
	- 즉, 좀 더 나한테 정확한 네트워크이다.
	- **prefix가 길면 길수록 정확한 네트워크**이다.


### Hierarchical routing with ISPs
- 계층적 라우팅의 예
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240515172032.png|400]]

- regional ISP에 120.14.64.0부터 시작하는 16,384개의 주소가 부여된다.
- regional ISP는 이 블록을 4.096개의 주소를 가진 4개의 하위블록으로 나누기로 결정한다.
- 이 하위 블록 중 3개는 3개의 local ISP에 할당되고, 두 번째 하위 블록은 향후 사용을 위해 예약된다.
- mask가 /18인 원본 블록을 4개의 블록으로 나누기 때문에 각 하위 블록의 마스크는 /20이다.
- 이 그림은 또한 로컬 및 소규모 ISP가 주소를 할당하는 방법을 보여준다.



