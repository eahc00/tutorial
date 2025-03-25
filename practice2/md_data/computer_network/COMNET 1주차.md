![[chapter1_new.pdf]]
- 데이터 통신
- 네트워크
- Internet : TCP/IP (internet과 다름)


## Data Communications ; 정보 공유
> [!definition]
> Data Communication은 **전송 매체를 통해 두 디바이스 간의 정보를 교환하는 것**.
- Data Communication System의 유효성(효율성)
    - **Delivery** : 시스템은 반드시 **올바른 목적지로 데이터를 전송**해야
        내가 원하는 사람에게 정확히 가야 → 목적지를 정확히 알 수 있는 **식별자(identifier) 필요**.
        ex) ip address, 전화번호 → 내 위치 정보를 담고 있음.
        
    - **Accuracy** : 시스템은 데이터를 **정확히 전달**해야.
        데이터가 정확히 전달 돼야(A 발신 → A 수신). 따라서 수신하는 데이터가 발신한 데이터와 같은지 확인하는 시스템이 필요.
        
    - **Timeliness**: 데이터가 **시기적절**하게 도착해야.
        ex) 라이브 방송, real-time system(실시간 시스템) → 빨라야한다.
        
    - **Jitter**
        **Jitter는 도착 시간의 variation**(변동? 분산?)을 나타낸다. packet의 고르지 않은 delay.
        ex) 이를 위해 buffer를 사용할 수 있음.

- data Communication의 **5가지 요소**
    - Sender(송신자)
    - Receiver(수신자)
    - Message(메시지)
    - Transmission medium(전송 매개, 전송 매체)
    - Protocol
        ex) http, tcp 등
        조약(Rule)을 포함.
        

- Data Flows
    - **Simplex**(**단방향**)
        한 디바이스는 발신만, 한 디바이스는 수신만 하는 dataflow
        ex) 본체와 모니터.
        
    - **Half-duplex**
        **양방향**이지만 **한 순간에는 한 명만 전송가능**.
        ex) 무전기. 동시에 얘기할 수 없다.
        
    - **Full-duplex**
        **모든 시간 양방향**으로 데이터가 흐른다.

### Network
> [!definition]
> **통신이 가능한 디바이스들이 연결 되어있는 집합**이 네트워크.

네트워크를 다른 네트워크와 연결해주는 디바이스; router, switch
(→ 정보를 가장 빠르게 전달하는 graph - shortest path 등의 알고리즘이 포함되는 것.)
  
- Network 기준(criterion)
    - **Performance**(성능)
        **response time, throughput(처리율 : 내가 특정 시간에 보낼 수 있는 양), delay** 등 여러 방법으로 측정된다.
        algorithm에 의해서도 성능이 좌지우지 됨.
        
    - **Reliability**(신뢰성)
        실패(에러, 고장) 빈도, 또한 이러한 실패에서 recover(회복)하는 시간.
	    얼마나 빠르게 복구할 수 있나?
        
    - **Security**(보안)
        승인되지 않은 접근으로부터 데이터를 지키는 등.
        
### Physical Structure 물리적 구조
- **Point-to-Point**
    전용선 : 두 개의 기기만 나누어 씀
    장점 : 성능이 좋다. 보안도 좋다. 둘만 쓰니까.
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240421164019.png|500]]

- **Multipoint**
    여러 명이 나누어 씀.
    성능, 보안이 덜 좋지만 경제성이 좋다.
    ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240421164036.png|500]]
    
---
- **mesh topology**
    하나가 다른 것과 모두 연결 돼 있음.
    장점 : 각각 전용선을 쓰는 것과 같음. 성능이 좋다. 어떤 선이 끊어져도 다른 것과는 상관 없어서 영향이 최소화. 보안도 강화된다.
    단점 : 새로 하나가 더 붙으면 이미 있는 기기만큼의 선을 연결 → 비용이 많이 든다.
    ⇒ **성능 측면에서는 좋지만 비용 측면에서 좋지 않다.**
	    ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240421164137.png|300]]
    
- **A star topology** : **Hub사용**
    허브사용. 이것 또한 전용선처럼 사용돼서 성능도 좋고 한 선이 고장나도 다른 것에 영향 가지 않음. 하나가 새로 연결 돼도 허브 포트에 선 하나만 더 연결하면 된다.
    단점 : 허브가 고장 나면 아무것도 못함. **single of failure 문제**를 가진다.
	    ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240421164205.png|400]]
    
- **A bus topology**
    케이블에 여러 기기가 달림. 비용이 많이 들지는 않음.(비용성이 좋음) 중간이 끊어지면 뒤쪽 부분에 접근이 불가능. **보안이 좋지 않음**.(point-to-point 방식이 아님 : 전용선이 아니라는 뜻)
    ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240421164224.png|450]]
    
- **A ring topology**
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240421164242.png|450]]
    한 링크가 끊어져도 반대 반향으로 접근할 수 있음.(**양방향 link**). bus보다 reliability(신뢰성)은 좋지만 보안은 좋지 않음. 경제성은 좋음.
    
> [!tip]
> ring topology는 link가 길어서 신호가 감쇠. -> 증폭기 사용
> 

  
그럼 여기서 어떤 방법이 제일 좋냐?
→ 상황에 따라서. 내가 구축하고자 하는 네트워크의 requirement에 맞게 구축.