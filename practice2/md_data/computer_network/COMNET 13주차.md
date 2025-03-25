
## Transport Layer
### Objectvie
- 첫 번째 섹션
	- 전송 계층(transport layer) 프로토콜의 개념을 소개한다.
	- 먼저 프로세스 간 통신(process-to-process), 주소 지정(addressing), 멀티플렉싱 및 디멀티플렉싱, 오류와 흐름 및 혼잡 제어 등 일반적으로 전송 계층에 필요한 일반적인 서비스에 대해 설명한다.
	- 그런 다음 전송 계층 프로토콜이 비연결형(connectionless)과 연결 지향형(connect-oriented)의 두 가지 범주로 나뉜다는 것을 보인다.
- 두 번째 섹션
	- 일반적인 전송 계층 프로토콜에 대해 설명한다.
	- 실제 전송 계층 프로토콜이 제공하는 흐름 및 오류 제어 서비스에 집중한다.
	- 이러한 프로토콜을 이해하면 인터넷의 전송 계층 프로토콜(예를 들어 UDP, TCP)의 설계를 더 잘 이해하는 데 도움이 된다.


### Introduction
- 전송 계층은 응용 계층(Application layer)과 네트워크 계층 사이에 위치한다. 
- 이 계층은 **로컬 호스트(local host)와 원격 호스트(remote host)** 의 두 응용 계층 간에 프로세스 간 통신(process-to-process, inter-process communication, ipc)을 제공한다.
	- **포트(port) 번호**를 이용하여 **process를 구분**한다.
- 통신은 논리적 연결(logical connection)을 사용하여 제공된다.


#### Logical Connection at the Transport
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528132335.png|400]]


### Transport-Layer Services
- 전송 계층은 네트워크 계층과 응용 계층 사이에 위치한다.
	- 응용 계층에 서비스를 제공하고 네트워크 계층으로부터 서비스를 수신하는 역할을 담당한다.
- 이 섹션에서는 전송 계층에서 제공할 수 있는 서비스에 대해 설명하고 다음 섹션에서는 몇 가지 전송 계층 프로토콜에 대해 설명한다.


#### Network Layer vs. Transport Layer
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528132917.png|450]]

- Network Layer 
	- 목적지를 찾아가는 역할
- **transport-layer**
	- 한 컴퓨터(host) 내에 있는 **프로세스를 식별**한다.
	- 내가 **통신할 프로세스를 찾는 역할**을 수행 한다.


#### Port Number
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528133100.png|400]]

- 프로세스를 식별하기 위해 Port Number를 사용한다.
	- 대체로 **16bit, 65536개의 포트 번호** 존재.
- Daytime server 
	- 시간을 맞춰주는 역할(서버에서 시간을 가져오는)을 하는 서버 포트 번호 : 13
- client의 포트번호는 OS가 알아서 할당한다.


#### Some Well-known Ports used with UDP and TCP
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528133408.png|450]]

> [!important]
> - HTTP : 80
> - DNS : 53
> - HTTPS : 443
> - SSH : 22


#### IP Address vs. Port Number
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528133733.png|450]]

- Destination IP 주소는 server를 결정한다.
- Destination port number는 process를 결정한다.


#### Socket Address
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528133837.png|200]]

- IP address + Port number


#### Encapsulation and Decapsulation
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528134101.png|400]]


### Pushing vs. Pulling
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528134212.png|400]]

- Pushing : 상대방을 생각하지 않고 데이터를 밀어 넣는 것.
	- **flow control : 받을 수 있는 양만큼의 데이터만 전송해달라고 요청**한다.
- Pulling : 요청이 오면 데이터를 전송하는 것.

> [!note]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528134447.png|400]]
> - [출처(참고)](https://hongcana.tistory.com/64)


#### Flow Control at the Transport Layer
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528135024.png|400]]

- 전송 계층에서 수신자가 flow control 메세지를 보내면 송신자의 전송 계층은 응용 계층에 flow control 메세지를 전달하여 메세지 전송 속도를 조절하는 등 흐름을 제어한다.


### Connection
- 네트워크 계층 프로토콜과 마찬가지로 전송 계층 프로토콜은 **비연결형(connectionless)** 과 **연결 지향형(connection-oriented)** 이라는 두 가지 유형의 서비스를 제공할 수 있다.
- 그러나 전송 계층에서 이러한 서비스의 특성은 네트워크 계층의 서비스와는 다르다.
	- 네트워크 계층에서 비연결 서비스는 동일한 메시지에 속하는 다른 데이터그램에 대해 다른 경로를 의미한다.
	- 전송 계층에서의 비연결 서비스는 패킷 간의 독립성을 의미하며, 연결 지향적 서비스는 패킷 간의 종속성을 의미한다.

> [!my_question]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528135512.png|400]]
> - 네트워크 계층에서 연결형/비연결형?


#### Connectionless Service
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528141259.png|450]]

- **패킷들이 서로 독립적**이다.
	- **순서가 별로 중요하지 않음.**
- 연결 설정 과정이 필요 없다.
	- ex)UDP


#### Connection Oriented Service
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528141447.png|450]]

- **데이터 간의 관계**가 있다.
	- **순서가 중요.** 수신 후에 reordering 과정으로 순서를 맞추는 과정을 수행한다.
- **연결 설정 과정**을 가진다.
	- ex)TCP의 three-way handshaking


## Transport Layer Protocol
### Objective
- 첫 번째 섹션
	- 인터넷의 세 가지 전송 계층 프로토콜을 소개한다.
	- 모든 프로토콜에 공통적으로 적용되는 몇 가지 정보를 제공한다.
- 두 번째 섹션
	- 세 가지 프로토콜 중 가장 단순한 UDP에 대해 집중적으로 설명한다.
	- UDP는 전송 계층 프로토콜에 필요한 많은 서비스가 부족하지만, 그 단순성(간단함)이 일부 애플리케이션에서 매우 매력적이다.
- 세 번째 섹션
	- TCP에 대해 설명한다.
	- 이 섹션에서는 먼저 서비스와 기능을 나열한다.
	- 그런 다음 전환 다이어그램(transition diagram)을 사용하여 TCP가 연결 지향 서비스를 제공하는 방법을 보여준다.
	- 그런 다음 추상적인 window(abstract windows)를 사용하여 TCP에서 흐름 및 오류 제어가 어떻게 수행되는지 보여준다.
	- 다음에는 네트워크 계층에 대해 논의했던 주제인 TCP의 혼잡 제어(Congestion control)에 대해 설명한다.


### Position of Transport Layer in the TCP/IP Protocol Suite
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528142254.png|450]]

- SCTP : multimedia 서비스 특화 프로토콜


### UDP
- **UDP(User Datagram Protocol)** 은 **비연결성(connectionless)** 이고, **신뢰성이 없는 전송 프로토콜**이다.
- 만약 UDP가 그렇게 무력하다면 왜 프로세스가 이를 사용하려고 하는가?
	- 이러한 단점들은 몇 가지 장점들을 이끌어 낸다.
- UDP는 최소한의 오버헤드를 사용하는 **매우 간단**한 프로토콜이다.
	- TCP는 오버헤드가 크다.


#### User Diagram
- **User datagram**이라고 불리는 **UDP 패킷**은 각각 **2바이트(16비트)의 필드 4개로 구성된 8바이트의 고정 크기 헤더**를 가진다.
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528142912.png|450]]

- 처음 두 필드는 source 및 destination **포트 번호**를 정의한다.
- 세 번째 필드는 **헤더와 데이터를 더한 사용자 데이터그램의 총 길이를 정의**한다.
	- 데이터가 얼마나 되는지, 헤더가 얼마나 되는지를 알기 위해서 사용된다.
	- 16비트는 0~65,535바이트의 총 길이를 정의할 수 있다.
	- 그러나 UDP User datagram은 총 길이가 65,535바이트인 IP 데이터그램에 저장되므로 총 길이는 이보다 짧아야 한다.
- 마지막 필드에는 선택적으로 체크섬(checksum)을 포함할 수 있다.

> [!example]
> - 아래는 16진수 format에서의 UDP헤더의 내용이다.
> 	 ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528143758.png|300]]
> - source port number는 무엇인가?
> 	- 16진수 (CB84) = 52100
> - destination port number는 무엇인가?
> 	- 16진수 (000D) = 13
> - user datagram의 총 길이는 몇인가?
> 	- 16진수 (001C) = 28 bytes
> - data의 길이는 몇인가?
> 	- 28 - 8 = 20 bytes
> - 패킷이 클라이언트에서 서버로 전송되는가, 아니면 그 반대로 전송되는가?
> 	- destination port number가 13(well-know port)이므로, 패킷은 클라이언트에서 서버로 전송된다.
> - 클라이언트 프로세스는 무엇인가?
> 	- Daytime process이다.(port 번호 13)


#### Pseudoheader for Checksum Calculation
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528144333.png|400]]


#### UDP Applications
- UDP는 앞서 언급한 안정적인 전송 계층 프로토콜에 대한 기준을 거의 충족하지 못하지만, 일부 애플리케이션에서는 UDP를 사용하는 것이 더 바람직하다. 
- 그 이유는 일부 서비스에는 허용할 수 없거나 바람직하지 않은 부작용이 있을 수 있기 때문이다.
- 애플리케이션 디자이너는 때때로 최적의 결과를 얻기 위해 타협해야 할 때가 있다. 
	 - 예를 들어, 우리는 일상 생활에서 배송업체를 통한 1일 배송이 3일 배송보다 더 비싸다는 것을 알고 있다.
	 - 빠른 속도와 저렴한 비용은 모두 택배 배송에 있어 바람직한 특징이지만, 서로 상충되는 측면이 존재한다.

> [!example]
> - **DNS(Domain Name Service)** 와 같은 client-server 애플리케이션은 클라이언트가 서버에 짧은 요청을 보내고 서버로 부터 빠른 응답을 받아야 하므로 **UDP 서비스**를 사용한다.
> 	- 요청과 응답은 각각 하나의 user datagram에 들어갈 수 있다.
> 	- 각 방향으로 하나의 메시지만 교환되기 때문에 연결이 없는 기능은 문제가 되지 않으며, 클라이언트나 서버는 메시지가 잘못 전달될 염려가 없다.
> - e-mail에 사용되는 SMTP와 같은 client-server 애플리케이션은 사용자가 멀티미디어(이미지, 오디오 또는 비디어)를 포함할 수 있는 긴 이메일을 보낼 수 있으므로 UDP의 서비스를 사용할 수 없다.
> 	- 애플리케이션이 UDP를 사용하는데 메시지가 하나의 유저 데이터그램에 맞지 않는 경우 애플리케이션에서 메시지를 다른 유저 데이터그램에 맞지 않는 경우 애플리케이션에서 메시지를 여러 유저 데이터그램으로 분할해야 한다.
> 	- 여기서 비연결형 서비스가 문제를 일으킬 수 있다. 유저 데이터그램이 순서대로 도착하지 않고 수신 애플리케이션에 전달될 수 있다.
> - 인터넷에서 매우 큰 텍스트 파일을 다운로드한다고 가정하자. 신뢰성있는 서비스를 제공하는 전송 계층을 사용해야 한다.
> 	- 파일을 열 때 파일의 일부가 누락되거나 손상되는 것을 원하지 않는다.
> 	- 일부가 전송될 때 발생하는 지연은 가장 중요한 문제가 아니며, 전체 파일이 완성될 때까지 기다렸다가 파일을 확인한다.
> 	- 이 경우 UDP는 적합한 전송 계층이 아니다.
> - Skype와 같은 실시간 대화형 애플리케이션을 사용한다고 가정하자.
> 	- UDP 사용
> 	- 오디오와 비디오는 프레임으로 나뉘어 차례로 전송된다.
> 	- 전송 계층이 손상되거나 손실된 프레임을 다시 전송해야 하는 경우 전체 전송의 동기화가 손실될 수 있다.
> 	- 시청자는 갑자기 빈 화면을 보게 되고 두 번째 전송이 도착할 때까지 기다려야 한다. 이것은 용납할 수 없는 일이다.
> 	- 그러나 화면의 각 작은 부분이 하나의 유저 데이터그램을 사용하여 전송되는 경우 수신 UDP는 손상되거나 손실된 패킷을 쉽게 무시하고 나머지를 애플리케이션 프로그램에 전달할 수 있다.
> 	- 화면의 해당 부분은 매우 짧은 시간 동안 비어 있기 때문에 대부분의 시청자는 눈치 채지 못한다.


### TCP
- **TCP(Transmission Control Protocol)** 은 **연결 지향형**이고 **신뢰성 있는** 프로토콜이다. 
- TCP는 연결 지향 서비스를 제공하기 위해 **연결 설정(connection establishment)**, 데이터 전송, **연결 해제(connection teardown)** 단계를 명시적으로 정의한다.


#### Stream Delivery
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528160124.png|400]]

- 수신 측에서는 **바이트스트림**(Byte Stream)을 받아서 순서를 맞춰 응용 계층에 보낸다.


#### Sending and Receiving Buffer
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528160227.png|450]]

- sliding window와 비슷하다.


#### TCP Segment
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528160322.png|450]]


#### TCP Segment Format
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528160547.png|450]]

- **UDP에 비해 헤더가 크다.** (20 ~ 60byte의 패킷)
- **Sequence number**
	- 현재 내가 보내는 패킷이 몇 번째 패킷인지 전송
	- 순서를 맞추기 위함.
- Acknowledge number
	- **내가 받고싶은 패킷 번호**


##### TCP Control Field
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528160818.png|400]]


#### A TCP Connection
- TCP는 **연결 지향적**이다.
- 그런 다음 메시지에 속한 모든 세그먼트가 이 논리적 경로를 통해 전송된다.
- 전체 메시지에 대해 **단일 논리적 경로(single logical pathway)** 를 사용하면 **승인 프로세스(acknowledgement process)** 와 손상되거나 손실된 프레임의 **재전송이 용이**해진다.
- 비연결 프로토콜인 IP의 서비스를 사용하는 TCP가 어떻게 연결 지향적일 수 있는지 궁금할 수 있다.


##### Connection Establishing using Three way Handshaking
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528161515.png|450]]

- TCP에서 연결을 설정할 때 사용하는 **Three way handshaking**이다.
- TCP는 양방향 연결이므로 SYN → SYN + ACK → ACK로 양쪽에서 연결


##### Data Transfer
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528174638.png|400]]


##### Connection Termination using Three Way Handshaking
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528184628.png|450]]

- **FIN** : 내가 더 이상 너에게 **보낼 메시지가 없다.**
	- **수신은 가능. 프로세스가 죽는 게 아니다.**


##### Half Close
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528184901.png|450]]

- **4-way handshaking**
- 한 쪽이 먼저 FIN을 보내고 ACK를 받고 FIN을 기다린다.
- 만약 상대가 보낼 데이터가 있으면 더 전송하고 FIN을 기다리면서 데이터를 받는다.
- FIN이 오면 ACK를 보내고 연결을 끊는다.


##### Timeline for Common Sceanario
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528185302.png|300]]


#### Flow Control
- 앞서 설명한 것처럼 흐름 제어는 생산자가 데이터를 생성하는 속도와 소비자가 데이터를 사용할 수 있는 속도의 균형을 맞추는 역할을 한다.
- TCP는 흐름 제어와 오류 제어를 분리한다.
- 이 섹션에서는 오류 제어를 무시하고 **흐름 제어**에 대해 설명한다.
- 송신자와 수신자 사이의 논리적 채널에 오류가 없다고 가정한다.


##### Data Flow and Control Flow Feedback in TCP
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528191941.png|400]]


##### Example of Flow Control
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528192413.png|400]]

- sliding window를 사용하여 flow control한다.
	- **selective repeat 방식** 사용.
		- 수신측과 송신측에 모두 buffer가 존재.
	- **수신측이 송신측에 window size**를 알려준다.

> [!additional explanation]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240610015515.png|400]]


#### Error Control
- TCP는 신뢰할 수 있는 전송 계층 프로토콜이다.
- 즉, TCP로 데이터 스트림을 전달하는 애플리케이션 프로그램은 TCP에 의존하여 전체 스트림을 오류 없이, 손실 되거나 중복 되는 부분 없이 순서대로 상대방의 애플리케이션 프로그램에 전달한다.


##### Normal Operation
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528193420.png|450]]

- ACK가 누적되면 나중에 제일 큰 ACK 하나만 보내도 된다.
	- **누적 ACK** 사용 : 수신자가 마지막으로 올바르게(연속적으로) 수신한 SeqNo를 송신측에 알린다.

> [!additional explanation]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240610015611.png|400]]


##### Lost Segment
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528193517.png|500]]

- Selective Repeat 방식과 유사.
	- 누락된 패킷만을 재전송

> [!additional explanation]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240610015712.png|450]]


##### Fast Retransmission 
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528193553.png|490]]

- **빠른 재전송**
	- ACK가 계속 온다는 거 자체가 요청 데이터 외의 다른 데이터는 잘 갔다는 뜻이므로 **ACK로 요청 온 데이터**만 보내면 된다.
	- ACK가 세 번 중복되면 바로 재전송을 실행

> [!additional explanation]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240610015900.png|450]]


#### TCP Congestion control
- TCP는 네트워크의 혼잡을 처리하기 위해 다양한 정책을 사용한다. 이 섹션에서는 이러한 정책에 대해 설명한다.
- **혼잡 제어**


##### Slow Start(SS), Exponential Increase
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528194235.png|490]]

- **네트워크가 허용(cwnd)** 하고 **receiver가 받을 수 있는 양(rwnd)** 만큼을 보내야.
	- **둘 중 더 작은 값(min값)으로**
- 지금 네트워크가 얼만큼 데이터를 보낼 수 있는지
- 혼잡이 발생하지 않으면서도 많은 양의 데이터를 보낼 수 있어야.
	- **TCP → 혼잡이 생길 때까지 데이터 양(cwnd)을 높여보는 방식으로 알아낸다.(지수적으로)**
	
> [!definition]
> - RTT(round trip time) : 왕복시간
> 	- 요청이 목적지로 갔다가 응답이 돌아오는 시간

> [!additional explanation]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240610020233.png|450]]


##### Congestion Avoidance, Additive Increase
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528194829.png|400]]

- **처음에는 지수적으로, 나중에는 더해서** 높인다.
	- RTT마다 1씩 증가
- 나중에는 혼잡이 발생할 수 밖에 없다.
	- 언젠가는 Packet이 loss되는 시점이 발생.
	- 이 지점을 찾아서 또 cwnd 크기를 조절.

> [!additional explanation]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240610020257.png|450]]


##### Example of TCP
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528195028.png|400]]

- **cwnd(congestion window, 혼잡 윈도우)** 를 지수적으로 높여가며 데이터를 전송하다가 Time-out이 발생하면 **cwnd가 1로 떨어짐.** 
- 다시 cwnd를 늘려가다가 Time out이 발생한 **cwnd의 크기 절반부터는(ssthresh, 여기서부터 조심해) 1씩 더해가며** cwnd를 높인다.

- 이때 **time out은 혼잡(congestion)이 발생한 것**. 패킷의 loss가 발생한 것이다.
- 3dup ACKs는 혼잡이 아닌 패킷 문제이다. 
- 이때 혼잡이 아닌 패킷 문제여도 loss가 발생하면 무조건 1로 떨어지게 되는 문제가 생긴다.
- 사이즈를 적당히 줄여야 한다.

> [!example]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528200509.png|400]]
> - **Reno TCP**에서는 3개의 중복 ACK가 도착하는 RTT 13까지 cwnd의 변화가 동일하다.
> 	- 이때 Reno TCP는 ssthresh를 6 MSS(maximum segment size)로 낮추지만 cwnd는 1 MSS 대신 훨씬 더 높은 값(ssthresh + 3 = 9 MSS)으로 설정한다. 
> 	- 이제 **빠른 복구 상태(fast-recovery state)** 로 이동한다.
> - cwnd가 기하급수적으로 증가하는 RTT 15까지 두 개의 중복 ACK가 더 도착한다고 가정한다.
> 	- 이 순간, 손실된 세그먼트의 수신을 알리는 새로운 ACK(중복되지 않음)가 도착한다.
> 	- 이제 혼잡 회피 상태(congestion avoidance state)로 이동하지만, 먼저 전체 고속 복구 상태를 무시하고 이전 트랙으로 돌아가는 것처럼 혼잡 윈도우를 6 MSS로 축소한다.

> [!additional explanation]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240610020321.png|450]]

> [!additional explanation]
> [MSS](https://www.cloudflare.com/ko-kr/learning/network-layer/what-is-mss/)  
> [혼잡제어 + ssthresh](https://velog.io/@mu1616/TCPIP-%ED%98%BC%EC%9E%A1-%EC%A0%9C%EC%96%B4)


##### Additive Increase, Multiplicative Decrease
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240528200553.png|400]]

- TCP는 네트워크가 혼잡되면 줄이고 아니면 늘린다.
	- **UDP는 이런 거 안한다.**
- 둘이 같이 쓰면 UDP만 데이터를 많이 보내고 TCP는 데이터를 못 보내게 된다.

