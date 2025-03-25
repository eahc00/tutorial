
## Data Link Control(DLC)

### Objectives 
- 첫 번째 섹션은 DLC sublayer에 의해 제공되는 일반적인 서비스를 설명한다. 
	- 먼저 **framing**과 이 서브 레이어에서 사용되는 두 가지 유형의 프레임에 대해 설명한다.
	- 그런 다음 **흐름(flow)과 오류 제어**에 대해 설명한다.
	- 마지막으로 DLC 프로토콜이 비연결형(connectionless) 혹은 연결 지향형(connection-oriented)일 수 있음을 설명한다.

- 두 번째 섹션은 DLC sublayer에서 구현되는 몇 가지 간단하고 일반적인 **데이터 링크 프로토콜**에 대해 설명한다.
	- 이 섹션에서는 먼저 Simple Protocol에 대해 설명한다.
	- 이후 Stop-and-Wait Protocol에 대해 설명한다.

- 세 번째 섹션은 PPP(The Point-to-Point Protocol)와 이더넷(Eternet)과 같이 오늘날 사용되는 모든 일반적인 데이터 링크 프로토콜의 기반이 되는 프로토콜인 **HDLC**에 대해 소개한다.
	- 이 섹션에서는 먼저 구성(configuration) 및 전송 모드(transfer mode)에 대해 설명한다.
	- 그런 다음 이 프로토콜에서 사용되는 프레임과 세 가지 프레임 포맷에 대해 설명한다.


### DLC Services
- Data link Control(DLC)는 링크가 전용(dedicated)인지 broadcast인지와 관계 없이 **두 인접 노드 간**의 통신 절차를 처리한다.
- Data link control function에는 **Framing과 흐름(flow) 및 오류 제어가 포함**된다.
- 이 섹션에서는 먼저 Framing, 즉 **물리 계층에 전송되는 비트를 구성**하는 방법에 대해 설명한다. 
- 이후 흐름 및 오류 제어에 대해 설명한다.

> [!info]
> - 이더넷에서 실제로 하는 건 framing밖에 없다.
> 	- 흐름 제어는 상위 레이어에서 한다.
> 	- 오류 제어는 오류 안나서 안함

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240602220034.png|500]]

- **CRC(Cyclic redundancy check)** : **error 제어**를 위해 사용
	- checksum 같은 거.
- 에러가 없는 걸 송신자에게 알리기 위해 ACK를 전송한다.

> [!etc]
> - 이더넷은 유선
> - 무선은 와이파이


### Framing 
- 데이터 링크 계층은 각 프레임을 **서로 구분할 수 있도**록 비트를 프레임으로 패킹해야 한다.
	- 데이터 링크 계층은 **네트워크 계층에서 데이터를 받는다.**

> [!example]
> 우편 시스템은 일종의 framing을 실행한다. 봉투에 편지를 넣는 간단한 행위만으로도 한 정보를 다른 정보와 구분할 수 있으며, 봉투는 구분자 역할을 한다.

- 데이터 링크 계층의 framing은 **송신자 주소(sender address)와 수신자 주소(destination address)를 추가**하여 메시지를 한 source부터 destination으로 분리한다.
- 수신자 주소는 패킷이 어디로 갈지 정의하고 송신자 주소는 수신자가 수신을 확인(acknowledge)하는 데 도움이 된다.

#### A frame in character-oriented protocol
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240505040203.png|500]]

- Header 
	- data link layer Header
- Trailer
	- redundancy bit가 trailer에 → error control
- flag
	- frame의 시작과 끝을 알려준다.


### Byte Stuffing and unstruffing
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240602214644.png|500]]

- 데이터 내부에 flag와 똑같은 비트가 들어있으면 flag로 인식될 수 있음
	- flag가 아님을 표시하기 위해 ESC를 넣어줌
- 근데 ESC와 같은 비트가 또 있으면?
	- ESC를 두 번씩 집어넣어줌.


### Flow and Error Control
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240505040351.png|500]]

> [!info]
> push/pull service
> - push : 무조건 온다(전송한다)
> - pull : 내가 요청하면 온다

- 수신자가 받을 수 있는 양만큼의 데이터를 전송해야 한다.
	- 처리할 수 있는 양 이상의 데이터가 오면 다 손실된다.
	- **전송 속도를 줄여달라고(받을 수 있는 양만큼만 보내달라고) 송신자에게 요청**해야 한다.
	- 이게 flow control


### Two Categories of Links
- 위 설명에 따르면 소비자(consumer)는 두 사건 : 버퍼가 가득 찼을 때와 빈 곳이 생겼을 때 생산자(producer)와 소통해야 한다.
- 두 참여자(당사자)가 하나의 슬롯(slot)만 있는 버퍼를 사용한다면 통신이 더 쉬워질 수 있다.
- 각 데이터 링크 계층이 하나의 메모리 슬롯을 사용하여 프레임을 보관한다고 가정하자.
- 수신 데이터 링크 계층의 이 단일 슬롯이 비어 있으면 네트워크 계층에 다음 프레임을 보내라고 알림을 전송한다.


### Data Link Layer Protocol
- 전통적으로 데이터 링크 계층에서는 흐름 및 오류 제어를 처리하기 위해 네 가지 프로토콜이 정의되어 있다.
	- Simple, Stop-and-Wait, Go-Back-N, Selective-Repeat
- 마지막 두 프로토콜은 여전히 데이터 링크 계층에서 사용되고 있지만, 처음 두 프로토콜은 사라졌다.


#### Simple Protocol
- 첫 번째 프로토콜은 **흐름 및 오류 제어가 둘 다 없는** Simple Protocol이다.
- 수신자는 수신하는 모든 프레임을 즉시 처리할 수 있다고 가정하자.
	- 즉, 수신기는 들어오는 프레임에 과부하가 걸리지 않는다.
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240505041654.png|500]]


#### Flow Diagram
- Flow control이 필요 없다.
	 ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240602215456.png|400]]
	- 그냥 전송

#### Stop-and-Wait Protocol
- 두 번째 프로토콜은 **흐름과 오류 제어를 모두 사용**하는 **Stop-and-Wait 프로토콜**이다.
- 여기서는 이 프로토콜의 primitive version(원시 버전)을 보인다.
- 이 프로토콜에서는 송신자가 **한 번에 한 프레임씩 전송**하고 다음 프레임을 **전송하기 전에 확인을 기다린다**.
- 손상된 프레임을 감지하려면 각 데이터 프레임에 redundancy bit를 추가해야 한다.


##### Flow Diagram
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240505041734.png|500]]

- 송신자는 메세지(frame) 전송 후 **timer**를 돌린다.
- 수신자는 frame을 수신한 뒤, 에러가 없으면 **ACK(ACKnowledgement)를 송신자에게 보낸다.**
- 송신자는 timer안에 **ACK가 오면** 문제가 없다고 생각하고 **timer를 리셋**한다.
- 만약 timer가 끝날 때까지 **ACK가 안오면 재전송을 실행**한다.

> [!problem]
> 만약 수신자가 데이터를 잘 받았는데, 이후 보낸 ACK packet이 전송 중 lost되거나 corrupted되어 송신자가 같은 메세지를 재전송하면 **duplicate**된 frame을 버려야 한다.  
> 	 근데 simple protocol은 이걸 알아낼 수 있는 방법이 없음. 그냥 중복 된다.  
> → Frame을 식별하는 번호가 필요하다. (더 복잡한 프로토콜이 등장.)

> [!solution]
> - seq, ACK에 번호 붙이는 방식 이용


#### Go-Back-N Protocol
- 전송의 효율성을 높이기 위해(파이프를 채우기 위해) 송신자가 **ACK를 기다리는 동안 여러 packet이 전송**돼야 한다.
- 즉, 송신자가 ACK를 기다리는 동안 채널을 바쁘게 유지하기 위해 하나 이상의 패킷을 미보류 상태로 둬야한다.
- 이 섹션에서는 이 목표를 달성할 수 있는 프로토콜을 소개한다.
- 첫 번째 프로토콜을 **Go-Back-N(GBN)** 이다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240505043012.png|500]]

- packet, ACK에 **seqNo, ackNo**를 붙여서 **frame과 ACK를 식별**하게 한다. 
- **Send window** 
	- 전송 측에 윈도우를 둔다.
	- 데이터 양 조절. 너무 많이 전송하지 않도록 한다.
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240505043209.png|450]]
	- $S_{size}$ : **Send window size**
		- **ACK 없이(ACK를 받지 않고) 보낼 수 있는 패킷 개수**
		- 위 사진에서는 ACK 없이 7개를 보낼 수 있다는 것.

> [!note]
> - seqNo가 $2^m$일 때, $S_{size}$ = $2^m - 1$이어야 한다.


- Sliding the send window(**sliding window** 방식 사용)
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240505043410.png|400]]

- Receiver window for Go-Back-N protocol
	- $R_{size}$ = 1
	- Go-Back-N 프로토콜은 Receive window의 크기가 1인 것.
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240505043519.png|400]]

##### Flow Diagram
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240505043558.png|500]]

- ACK는 **그 다음 받을 것을 전송**
	- "0번 잘 받았어"가 아닌 "1번을 줘"를 의미
- 위 사진에서 2번 ACK가 lost됐지만, 2번 ACK가 사다져도 3번 ACK가 온다면 2번까지는 잘 갔다는 의미
	- 이후 번호의 ACK가 오면 2번 ACK는 의미가 없다.
	- **누적 ACK**를 사용

> [!my_question]
> 만약 데이터가 전송 중에 손실되면?(Ex: 실제로 2번 packet이 손실되면?)  
> → Receiver window의 크기가 1이기 때문에 기대하고 있던 2번이 오지 않으면 다음 데이터를 받을 수 없다.


##### Example
- 다음은 패킷이 손실(lost) 되었을 떄 어떤 일이 발생하는 지 보인다.

> [!example]
> - 패킷 0, 1, 2, 3이 전송된다.
> - 패킷 1이 손실 된다.
> - 수신자는 패킷 2와 3을 수신하지만 순서대로 수신되지 않았기 때문에 버린다. (패킷 1이 기대됨.)
> - 수신자는 패킷 2와 3을 수신하면 패킷 1을 수신할 것을 기대한다는 것을 나타내는 ACK1을 전송한다.
> - 그러나 이러한 ACK는 송신자에게 유용하지 않은데, 그 이유는 akcNo가 $S_f$보다 크지 않고 $S_f$와 같으므로(이미 전송한 패킷의 Num을 요청한 것) 송신자는 이 ACK packet을 버린다. 
> - time-out이 발생하면 발신자는 패킷 1, 2, 3을 재전송하고 이 패킷은 ACKnowledge된다.


##### Flow Diagram2
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240505211745.png|500]]

- Packet discarded
	- receiver는 1번을 기다리고 있는데 2번이 온 것. 2번을 버리고 ACK 1을 보낸다.
	- +) 만약buffer가 여러 개면 2, 3번을 저장해놓고 1번만 다시 받으면 된다.
- ACK discarded
	- 1번에서 문제가 발생한 것.
- 기대한 ACK는 2, 3, 4 중에 하나인데, ACK 1번이 와서 time-out이 걸린다.

> [!problem]
> - **하나만 에러 나도 여러 개를 다시 재전송**해야
> 	- 2, 3번은 에러 없이 갔는데도 재전송을 또 해야한다.
> 	- 비효율적

> [!solution]
> - receiver에서 buffer가 하나만 있기 때문에
> - buffer 수를 늘려서 해결할 수 있다.
> - 이렇게 buffer를 여러 개 두는 게 Selective Repeat

- 타이머가 길면
	- 에러 검출이 느리게 되어 낭비하는 시간이 길어진다.
- 타이머가 짧으면
	- 에러가 없어도 있다고 생각하게 될 수 있다.


#### Selective-Repeat Protocol
- Go-Back-N 프로토콜은 수신자의 프로세스를 간소화한다. 수신자는 하나의 변수만 추적하며, 순서가 맞지 않는 패킷은 버퍼에 넣지 않고 단순히 삭제한다.
	- 그러나 이 프로토콜은 기본 네트워크 프로토콜이 많은 패킷을 손실하는 경우 비효율적이다.
	- 하나의 패킷이 손실되거나 손상될 때마다 송신자는 몇몇 이미 보내진 패킷이 정상적으로 수신되었지만 순서가 맞지 않아도 모든 이미 보내진 패킷을 재전송한다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240505222409.png|500]]

- receiver쪽이 window처럼 버퍼를 더 가지게 된다.

##### Flow Diagram
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240505222552.png|500]]

- 기대하는 packet 번호가 아닌 **자기가 받은 번호를 ACK** 보낸다.

> [!note]
> - $R_{size}$ = $2^{m-1}$로 설정해야



## Media Access Control(MAC)
[참고](https://ideadummy.tistory.com/114#Reservation-1)

- **Broadcast link**
	- 데이터를 두 디바이스가 같이 보내면 **충돌이 발생**한다.
	- 누가 데이터를 보낼건지, 어떻게 하면 겹치지 않는지.

- RANDOM ACCESS
	- controller가 없다.
- CONTROLLED ACCESS
	- controller 하나 → 다른 것들을 control하게 하는 것.
- CHANNELIZATION

### Objectives
- 첫 번째 섹션에서는 random-access 프로토콜에 대해 설명한다. 
	- 네 개의 프로토콜 ALOHA, CSMA, CSMA/CD, CSMA/CA가 이 섹션에서 설명된다.
	- 이러한 프로토콜은 주로 LAN과 WAN에서 사용된다.

- 두 번째 섹션에서는 controlled-access 프로토콜에 대해 설명한다.
	- 세 개의 프로토콜 reservation, polling, token-passing이 이 섹션에서 설명된다.
	- 이러한 프로토콜 중 몇몇은 LAN에서 사용되지만 다른 프로토콜은 역사적인 가치를 가진다.

- 세 번째 섹션에서는 channelization 프로토콜에 대해 설명한다. 
	- 세 개의 프로토콜 FDMA, TDMA, CMDA이 이 섹션에서 설명된다.
	- 이러한 프로토콜은 셀룰러 전화에 사용된다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506161741.png|500]]


### Random Access
- random-access 또는 contention에서는 어떤 스테이션(station)도 다른 스테이션보다 우월하지 않으며, 어떤 스테이션도 다른 스테이션에 대한 제어권이 할당되지 않는다.
- 각 인스턴스에서 전송할 데이터가 있는 스테이션은 프로토콜에 정의된 절차(proceduer)를 사용하여 전송 여부를 결정한다.
- 이 결정(decision)은 **중간 매체의 상태(idle or busy)** 에 달려있다.


#### ALOHA
- 최초의 random access method인 ALOHA는 1970년 초 하와이 대학교에서 개발되었다.
- ALOHA는 radio(무선) LAN용으로 설계되었지만, 어떤 공유 매체(shares medium)에서든 사용할 수 있다.
- 이 방식(arrangement)에 잠재적인 충돌이 있다는 것은 명백하다.
- 매체(medium)은 스테이션들 사이에서 공유된다. 한 스테이션이 데이터를 전송하면 다른 스테이션도 동시에 전송을 시도할 수 있다.
- 두 스테이션의 데이터가 충돌하여 왜곡될 수 있다.

##### Frame in the ALOHA Protocol
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506162832.png|500]]

- **충돌(Collision) → 재전송 → 또 충돌**이 날 수 있다.


##### Procedure for pure ALOHA protocol
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506163114.png|500]]

- Wait($2 * T_p$) : Timer
	- ACK 수신을 대기하는 timer
- Choose R
	- 각각 전송 시간이 달라질 수 있도록 **random 값을 추가**한다.
- $K > K_{max}$
	- 어느 정도 반복했는데도 안되면 포기.


##### Frames in a slotted ALOHA netword
- **Slotted ALOHA**
	- 보내는 시간의 **slot을 나눠두어** 충돌 가능성을 줄인다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506163422.png|500]]


#### CSMA : Carrier Sense Multiple Access
> [!summary]
> 남이 전송 하고 있는지를 먼저 보고 전송 하고 있으면 남이 전송을 안 할 때까지 기다리고 전송 안하고 있으면 내가 전송하는 방식

- 충돌 가능성을 최소화하여 성능을 향상시키기 위해 CSMA 방식이 개발되었다.
- 스테이션이 **매체를 사용하기전에 매체를 감지**하면 충돌 가능성을 줄일 수 있다.
- Carrier Sense Multiple Access(CSMA)는 각 스테이션이 전송하기 전에 먼저 매체를 listen(또는 매체의 상태를 확인)해야 한다.
- 즉, CSMA는 "sense before transmit" 또는 "listen before talk"라는 원칙에 기반한다.

##### Space/time model of a collision in CSMA
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506164546.png|500]]

- B의 신호는 $t_1$에 시작
- C까지 B의 신호가 도달하기 전 $t_2$에서 C가 medium을 체크하면 medium을 사용하지 않는다고 판단하고 충돌이 발생할 수 있다.



##### Vulnerable time in CSMA
- 위의 예시와 같이 CSMA에서 **취약 시간(Vulnerable time)** 이 생긴다.
- Vulnerable time = Propagation time
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506164844.png|500]]

> [!summary]
> propagation time 즉, 다른 station이 medium을 검사해서 알아낼 수 있을 정도로 전파되는 시간 중에 다른 station이 medium을 검사하면 medium을 사용하지 않는 것처럼 보이므로 propagation이 CSMA에서의 취약 시간이 된다.


##### Behavior of three persistence methods
- 채널 획득 방식 : carrier sence를 어떻게 할거냐?
- 1-persistent
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506165207.png|300]]
	- **계속 carrier를 sensing**하고 있다가 사용 중인 station이 없으면 **바로 보낸다.**
	- 여러 station이 대기 하면 충돌날 가능성이 크다.
	- 한 station만 대기하고 있으면 성능이 제일 좋다.
		- 대기하고 있다가 medium이 비는 없이 바로 전송할 수 있으므로

> [!hint]
> - p-persitent 방식에서 확률 p가 1인 것.



- Nonpersistent
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506165325.png|300]]
	- sensing하고 **랜덤한 시간 동안 wait**하다가 이후 다시 sensing한다.
	- 모든 station이 wait하다가 medium이 비어 있는 시간을 낭비할 수 있다.

- p-persistent
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506165524.png|450]]
	- **확률**을 가지고 기다리든지 보내든지 한다.
	- 알고리즘을 복잡하게 만들어서 최대한 동시에 보내지 않도록 한다.
	- 모든 station이 wait하다가 medium이 비어 있는 시간을 낭비할 수 있다.

##### Flow diagram for three persistence methods

- 1-persistent
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506165724.png|200]]

- Nonpersistent
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506165742.png|300]]

- p-persistent
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506165802.png|400]]


#### CSMA/CD
- CSMA 방식은 **충돌 후 procedure(절차)를 지정하지 않는다.**
- Carrier Sense Multiple Access with **Collision Detection**(CSMA/CD)는 **충돌을 처리**하기 위해 알고리즘을 보강한다.
	- **충돌이 나면 어떻게 할건지**를 추가로 정의함.
- 이 방법에서는 스테이션이 프레임을 전송한 후 매체를 모니터링하여 전송이 성공했는지 확인한다. 전송이 성공하면 스테이션이 완료된 것이다. 그러나 **충돌이 발생하면 프레임이 다시 전송**된다.

##### Collision of the first bits in CSMA/CD
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506170246.png|500]]


##### Collision and abortion in CSMA/CD

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506170600.png|500]]

- 충돌이 발생하면 감지하고 자신의 데이터를 더 이상 보내지 않음(**중단**)
- 이후 채널을 보면서 기다렸다가 재전송 한다.
- 이더넷(ethernet)이 이 방식을 사용한다.

- 충돌나면 jamming signal 보내서 충돌 난 거 알림.
- 그리고 exponential back-off로 대기  


##### Flow diagram for the CSMA/CD
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506170646.png|500]]

> [!note]
> - hidden state problem → CTS, RTS


### Controlled Access
- Controlled Access에서는 스테이션이 서로 협의하여 어느 스테이션이 전송할 권한이 있는지 찾는다
- 한 스테이션은 다른 스테이션의 승인(authorization)을 받지 않으면 전송할 수 없다.
	- 데이터를 보낼 수 있는지 **다른 station한테 물어보는 것.**
- 세 가지 제어 액세스 방법에 대해 설명한다.


> [!my_question]
> - primary가 어떤 기준으로 뽑히는 건지
> - 그러면 매번 바뀌나요? 아니면 하나 지정인가요?
> - 네트워크 그룹(LAN) 당 하나인가요?

#### Reservation
- reservation 방식에서는 스테이션이 데이터를 전송하기 전에 예약을 해야한다.
- 시간은 interval(구간)으로 나뉜다.
- 각 interval에서 예약 프레임은 해당 interval에 전송되는 데이터보다 우선(먼저 전송)된다.

##### Reservation Access Control
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506171604.png|500]]

- 오른쪽부터 왼쪽으로 읽으면 이해가 쉽다.
- **reservation frame**에서 **보낼 데이터가 있는 station의 수를 1로 변경**한다.
- 이후 1~5를 순서대로 읽으며 값이 1이면 해당 station의 데이터를 받아 **순서대로 time interval에 맞게 전송**한다.



#### Polling
- Polling은 한 장치가 primary station으로 지정되고 다른 장치가 보조 스테이션(Secondary station)으로 지정되는 topology에서 작동한다.
- 최종 목적지가 보조 장치인 경우에도 **모든 데이터 교환은 기본 장치를 통해 이루어져야 한다.**
- primary 장치가 링크를 제어하고 보조 장치는 primary 장치의 지시를 따른다.
- 주어진 시간에 채널을 사용할 수 있는 디바이스를 결정하는 것은 primary device에게 달려있다.
- **데이터 보낼 station을 물어본다.**

##### Select and poll functions in polling-access method
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506181101.png|500]]

- primary station은 secondary station에 크게 두 가지를 지시한다.
	- select
	- poll

##### Select
- primary station이 특정 secondary station을 골라서(select) **데이터를 보낼 것**이라고 하는 과정을 보인다.
- Primary station의 지시(instruction)에 대해 Secondary station은 **데이터를 받을 수 있는 상태면 ACK, 받을 수 있는 상태가 아니면 NAK**를 보낸다.


##### Poll
- poll도 select와 마찬가지로 데이터를 **보낼 수 있는 상황이면 ACK, 아니면 NAK**를 보낸다.
- 그리고 primary도 데이터를 잘 받으면 ACK를 전송한다.
- primary가 **데이터를 받는 것.**


#### Token Passing
- **token-passing 방식**에서, 네트워크의 스테이션은 **logical ring**으로 구성된다. 
	- 논리적으로 링의 형태를 가진다는 말은 네트워크를 bus나 star topology로 구성했어도, token은 원(ring)의 형태로 공평하게 주어진다는 말이다.
- 즉, 각 스테이션에서는 predecessor와 successor가 있다. 
- predecessor는 논리적으로 링에서의 이전 스테이션이고 sucessor는 링에서 뒤쪽에 있는 스테이션이다.


##### Logical ring and physical topology in token-passing access method
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506182302.png|450]]

- ring형에서 숫자를 정해놓고 데이터 전송. 
- **token을 받은 사람만 전송**할 수 있다.
	- 수건 돌리기 같은 방식
	- controller 필요.


### Channelization
- (channel partition이라고도 불리는) Channlization는 링크의 사용 가능한 대역폭을 시간, 주파수, 혹은 코드를 통해 여러 스테이션 간에 공유하는 multi access 방식이다. 
- 이 섹션에서는 세 가지 프로토콜 : FDMA, TDMA, CDMA에 대해 설명한다.

#### FDMA
- Frequency-Division Multiple Access(FDMA)에서는 **사용 가능한 대역폭이 주파수 대역으로 나누어진다.**
- 각 스테이션에는 데이터를 전송할 수 있는 대역이 할당된다. 즉, **각 대역은 특정한 스테이션을 위해 reserve**되어 있으며 항상 해당 스테이션에 속한다.
	- 채널의 주파수를 나눠서 각각 구분하여 할당해준다.
- 또한 각 스테이션은 bandpass filter를 사용하여 송신기 주파수(transmitter frequencies)를 제한한다.
- (1세대 아날로그 방식)

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506183600.png|500]]


#### TDMA
- Time-Division Multiple Access(TDMA)에서는 스테이션들이 **자신의 시간에 채널의 대역폭을 공유**한다.
	- **시간으로 channel을 나눈다.**
- 각 스테이션에는 데이터를 전송할 수 있는 time slot이 할당된다.
- 각 스테이션은 **할당된 time slot에 데이터를 전송**한다.
- (2세대 time 방식)

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506183928.png|500]]


#### CDMA
- **Code-Division Multiple Access(CDMA)** 는 수십 년 전에 고안된 개념이다. 최근 전자 기술의 발전으로 마침내 구현이 가능해졌다.
	- (퀄컴에서 특허내고 etri에서 구현)
- CDMA는 하나의 채널만이 링크의 전체 대역폭을 차지한다는 점에서 FDMA와 다르다.
- **모든 스테이션이 동시에 데이터를 전송할 수 있고** 시분할이 없다는 점에서 TDMA와 다르다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506184257.png|500]]


##### Chip Sequence
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506184315.png|300]]


##### Data Representation in CDMA
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506184342.png|300]]


##### Sharing Code in CDMA
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240506184440.png|500]]



> [!note]
> - 직교 벡터는 dot product가 0임을 이용
> - chip이 서로 모두 직교함. → 1, -1을 1, 0으로 바꿈
> - station마다 코드할당
> 	- data → code로 인코딩
> - 받는 쪽은 다 더함. 받는쪽은 station별 코드로 내적하고 코드 비트(ex-4 bit)로 나눈다.

