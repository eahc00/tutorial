![[chapter1_new.pdf]]
1주차 수업 자료와 이어짐.
  
- Networks Types
    네트워크의 size, geographical coverage(지리적 범위), ownership(소유권)등을 기준으로 구분할 수 있다.
    
- What’s the Internet
    ![[Untitled 35.png|Untitled 35.png|300]]
    - 수백만의 연결된 computing devies
        - **hosts = end systems**(네트워크의 가장 바깥쪽에 존재 : 데이터를 주고 받음.)
        - running network apps(네트워크 앱들을 돌리고 있다는 것)
    - Communication links(통신 링크)
        - 광섬유(fiber), 구리(copper), 라디오(radio), 위성(satellite)
        - 전송 속도(transmission rate) : bandwidth(대역폭)
            **대역폭** : 일정한 시간 내에 데이터 연결을 통과할 수 있는 정보량의 척도 (ex - bit/s)
    - Packet switches
        : packets(chuck of data;데이터 덩어리..?) 전달(forward)
        - router와 switch
            router : 네트워크를 이어주는 장치

### LAN(Local Area Networks)
- LAN은 일반적으로 개인 소유이며 단일 사무실, 건물 또는 캠퍼스에 있는 일부 호스트들을 연결한다.
- 조직의 필요에 따라 LAN은 간단하게는 집에 있는 두 대의 PC와 프린터부터 오디오, 비디오 디바이스를 포함하는 회사 전체로 확장될 수도 있다.
- LAN의 각각의 사용자는 **유일하게 LAN 내의 사용자를 정의하는 identifier, address**(네트워크 내에 주소.. 이더넷 MAC주소)를 가진다. 호스트가 다른 호스트에게 보내는 packet에는 source 호스트와 수신 호스트의 주소를 모두 포함한다.
    계층과 각각을 구분할 수 있는 여러 주소를 가진다.
- **LAN은 호스트와 연결**돼있다.
    - Bus형
        ![[Untitled 1 20.png|Untitled 1 20.png]]
        
    - HUB형
        ![[Untitled 2 17.png|Untitled 2 17.png|400]]

 
### WAN(Wide Area Networks)
- WAN도 통신이 가능한 디바이스의 연결이다.
- **LAN과 WAN의 차이**
    - LAN은 일반적으로 **크기가 제한**된다.; WAN은 도시, 주, 국가, 심지어 전 세계에 걸쳐 **더 넓은 지리적 범위**를 가진다.
    - **LAN은 호스트들을 연결**한다.; **WAN은 switch, router, modem과 같은 연결 디바이스를 연결**한다.
        - → **WAN은 Mesh방식이 사용**됨. 왜? 비용보다 신뢰성, 보안이 중요.
    - LAN은 일반적으로 그것을 사용하는 조직이 개인적으로 소유한다.; WAN은 일반적으로 통신 회사에서 생성, 운영하고 이를 사용하는 조직에서 임대한다.
	
- WAN의 연결 방식
    - **A Point-to-Point WAN**
        ![[Untitled 3 16.png|Untitled 3 16.png | 500]]
        통신기기(ex-router, switch)를 1:1로 연결하는 방식
        
    - **A Switched WAN**
        ![[Untitled 4 14.png|Untitled 4 14.png|500]]
        **네트워크끼리 서로 연결시킬 수 있는 형태**. 모든 걸 1:1로 연결하는 것보다 복잡성이 준다. 다른 네트워크를 통해 모두 연결 될 수 있다.
        
    - An internetwork made of two LANs and one WAN
        ![[Untitled 5 10.png|Untitled 5 10.png | 500]]
        두 LAN만을 위한 network(1:1) → 비싸다(Private network)
        그럼 기존의 network를 이용하여 연결하면? → 보안이 낮지만 비용이 싸다. (Public network)
        그럼 public을 private처럼 쓰는 법? → VPN(virtual private network)
        
    - A heterogeneous network made of WANs and LANs
        ![[Untitled 6 10.png|Untitled 6 10.png|500]]
        switched WAN으로 연결해서 확장성이 좋음.

### Switching
인터넷은 스위치가 두 개 이상의 링크를 서로 연결하는 스위치형 네트워크이다. 스위치는 필요할 때 한 네트워크에서 (원하는) 다른 네트워크로 데이터를 전달해야 한다.
가장 일반적인 두 가지 유형의 스위치 네트워크는 circuit-switched network와 packet-switched network이다.
- **A circuit-switched network**
    ![[Untitled 7 9.png|Untitled 7 9.png]]
    - 전화 : 연결(자원)이 할당되면 다른 사람이 쓸 수 없다. 자원이 둘 사이의 통신으로 **reserve**된다. → **경쟁을 하지 않음.**
        **자기 영역이 할당** 돼 있다. ex) 4개가 하나를 쓰면 1/4만을 쓰는 것.
    - → **비용이 많이 든다**. 안 쓰고 있는 게 많아질 수 있다.
    - Jitter의 차이가 생기지 않는다.
	
- **A Packet-switched network**
    ![[Untitled 8 9.png|Untitled 8 9.png]]
    - reserve를 하지 않는 방식 → 데이터가 많으면 **경쟁해야 한다**.
        ex) 4개가 하나를 쓰면 혼자 모든 걸 쓸 수도 있는 것.
    - **경제성이 좋다.**
    - Jitter의 차이가 생긴다.(많이 쓰면 길이지고 아니면 짧아지고…)
        → Jitter 문제를 추가적인 방법을 고안해서 해결한다.



### Internet
internet : 서로 통신할 수 있는 두 개 이상의 네트워크.
Internet(고유명사) : 사용하는 프로토콜이 TCP/IP인 네트워크. 수천 개의 상호 연결된 네트워크로 구성되어 있다.
![[Untitled 9 8.png|Untitled 9 8.png|500]]
- 오늘 날의 인터넷(Internet).
    - 위와 같이 계층적인 구조로 되어있다. 우리는 Customer network로 접속하여 backbone으로 들어간다.
    - 모든 사용자가 인터넷의 일부가 될 수 있는 인터네트워크이다. 하지만 사용자는 ISP(Internet Service Provider)에 물리적으로 연결되어 있어야 한다.
    - 물리적 연결은 일반적으로 지점 간 WAN을 통해 이루어진다.


### Internet History
- Early Internet
    - 1960년 이전에는 telegraph와 telephone network(circuit switch) 몇몇의 통신 네트워크가 있었음.
    - **constant rate**(정속 통신) : 두 사용자 간에 연결이 이루어진 후 인코딩 된 메세지 또는 음성(전화)를 교환할 수 있다는 의미
    - **bursty data**: 다양한 시간에 다양한 속도로 수신되는 데이터 : 이걸 처리하기 위해 **패킷 교환 네트워크**가 필요
	
- Birth of the Internet
    - 1972년 한 네트워크의 호스트가 다른 네트워크의 호스트와 통신할 수 있도록 하는 프로젝트 진행.
    - 한 네트워크에서 다른 네트워크로 데이터를 전송하는 중개 하드웨어 역할을 하는 게이트웨이라는 장치를 고안.
    - end-to-end 전송을 위한 프로토콜 개요를 설명하는 논문 발표(1973)
    - UNIX 운영체제에 TCP/IP를 포함하도록 함.
        → 인프라, 애플리케이션 모두에서 급속한 성장


### Standard
표준이 있는 게 좋을 것.(표준화된 통신)
Standard한 규칙 → document(docs)
- Internet Standards
    - 공식화된 규정
![[Untitled 10 7.png|Untitled 10 7.png]]
표준화 문서가 이렇게 만들어진다.
Standard draft → 검증 : 상호작용이 되는가?