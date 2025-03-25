
## Introduction to Application Layer
### Objective
- 응용 계층(Application layer)을 소개한다.
	- 응용 계층에서 제공하는 서비스에 대해 설명한다.
	- 인터넷의 호스트가 서비스를 교환할 수 있는 두 가지 패러다임을 설명한다.
		- client-server 패러다임
		- peer-to-peer 패러다임


### Introduction
- 응용 계층은 사용자에게 서비스를 제공한다.
- 통신(Communication)은 논리적 연결을 사용하여 제공되며, 이는 두 응용 계층이 메시지를 주고받을 수 있는 가상의 direct connection이 있다고 가정한다는 것을 의미한다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604165911.png|400]]


### Providing Services
- 인터넷 이전에 시작된 모든 통신 네트워크는 네트워크 사용자에게 서비스를 제공하도록 설계되었다.
- 그러나 이러한 네트워크의 대부분은 원래 하나의 특정 서비스를 제공하도록 설계되었다.
	- 예를 들어, 전화(telephone) 네트워크는 원래 전 세계 사람들이 서로 통화할 수 있도록 음성 서비스를 제공하도록 설계되었다.
	- 그러나 이 네트워크는 나중에 사용자가 양쪽 끝에 하드웨어를 추가하여 facsimile(fax)와 같은 다른 서비스에도 사용되었다.
- 하위 계층에 있는 서비스를 제외하고는 모두 응용 계층에서 제공해야


### Application-Layer Paradigms
- 인터넷을 사용하려면 전 세계 어딘가의 컴퓨터에서 실행되는 프로그램과 전 세계 다른 곳의 다른 컴퓨터에서 실행되는 **두 개의 응용 프로그램이 서로 상호 작용**해야 한다는 점을 분명히 알아야한다.
- 두 프로그램은 인터넷 인프라(Internet infrastructure)를 통해 서로에게 메시지를 보내야 한다.
- 그러나 이러한 프로그램 간의 관계에 대해서 설명한 적은 없다.
- **client-server 패러다임**과 **peer-to-peer 패러다임**이라는 두 가지 패러다임이 개발 되었고, 여기서는 이 두 가지 패러다임에 대해 간략히 소개한다.


#### Example of a Client-Server Paradigm
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604171307.png|400]]

- **서버는 정보를 holding하고 요청**을 기다린다.

> [!problem]
> - client-server는 **중앙 집중형**. 서버가 죽으면 아무것도 못한다.
> 	- 분산형으로 해결할 수 있지만 데이터의 consistence를 맞춰줘야 한다는 문제가 생긴다.
> 	- 데이터의 consistence : 모든 서버의 데이터를 똑같이 맞춰 줘야 한다는 것.

> [!solution]
> - scale-up(수직 확장) : 비싸다
> - scale-out(수평 확장) : 싼 서버를 여러 개 두는 방식
> - auto-scaling : 늘렸다 줄였다 하는 것
> - scale-out 등을 통한 load-balancing 등


#### Example of a Peer-to-Peer Paradigm
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604171651.png|400]]

- **Peer-to-Peer**
	- 내가 서버도, 클라이언트도 될 수 있다.

> [!problem]
> - 문제 : 어느 데이터가 어디에 있는지 알아내야
> 	- 서버가 데이터에 모여있는 게 아니기 때문에


## Standard Client Server Protocols
### Objective
- 첫 번째 섹션에서는 **World Wide Web(WWW, or Web)** 에 대해 소개한다.
- 그 다음 WWW과 관련하여 가장 일반적으로 사용되는 client-server 응용 프로그램인 **HTTP(HyperText Transfer Protocol)** 에 대해 설명한다.


### World Wide Web
- 웹(web)의 개념은 1989년 유럽입자물리연구소(CERN)의 Tim Berners-Lee가 유럽 각지에 있는 여러 연구자들이 서로의 연구에 액세스할 수 있도록 하기 위해 처음 제안한 것이다.
- 상업용 웹은 1990년대 초에 시작되었다.


#### Example
- 다른 텍스트 파일에 대한 참조와 큰 이미지에 대한 참조가 각각 하나씩 포함된 과학 문서를 검색해야 한다고 가정하자.
- main document(file A)와 이미지(file B)는 같은 사이트에 있는 두 개의 별도 파일에 저장되어 있고, 참조된 텍스트 파일은 다른 사이트(file C)에 저장되어 있다.
- **세 개의 서로 다른 파일을 다루고 있으므로 전체 문서를 보려면 세 번의 처리(transaction)이 필요**하다.
	- **이미지 같은 거를 각자 요청**한다.
- HTML, XML 등을 주로 주고 받고 브라우저를 통해 우리가 보는 형태로 나타난다.

> [!tip]
> - 최초의 브라우저 : 모자익

#### Browser
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604185547.png|500]]


#### Example
- URL \http://www.mhhe.com/compsci/forouzan/은 맥그로힐 회사의 컴퓨터 중 하나와 관련된 웹 페이지를 정의한다.
	- (www 세 글자는 호스트 이름의 일부이며 상용 호스트에 추가된다.)
- 경로는 compsci/forouzan/이며, compsci(computer science) 디렉토리 아래에 있는 Forouzan의 웹페이지를 정의한다.


### HyperText Transfer Protocol
- **HyperText Transfer Protocol(HTTP)** 는 웹에서 웹 페이지를 검색하기 위해 client-server 프로그램을 작성하는 방법을 정의하는 데 사용된다.
- **HTTP 클라이언트가 요청을 보내면 HTTP 서버가 응답을 반환**한다.
	- 서버는 **포트 번호 80**을 사용하고 **클라이언트는 임시 포트 번호**를 사용한다.
- HTTP는 앞서 설명한 대로 연결 지향적이고 신뢰성 있는 프로토콜인 **TCP의 서비스를 사용**한다.
	- TCP는 흐름 및 오류 제어를 가진다.

> [!tip]
> - HTTP3는 UDP 사용 : QUIC
> - [참고](https://youtu.be/Zyv1Sj43ykw?si=WtKpvD30dvOqN3Dk)


#### Example : non-persistent connection
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604191050.png|400]]

- 클라이언트는 이미지에 대한 링크가 하나 포함된 파일에 액세스 해야 한다.
- 텍스트 파일과 이미지는 동일한 서버에 있다. 여기에는 두 개의 연결이 필요하다.
- 각 연결에 대해 TCP는 연결을 설정하기 위해 최소 세 개의 handshake 메시지가 필요하지만 요청은 세 번째 메시지를 전송할 수 있다.
- 연결이 설정되면 object를 전송할 수 있다. object를 받은 후 연결을 종료하려면 세 개의 handshake 메시지가 더 필요하다.


#### Non-Persistent Connection
- **한 연결에 하나의 요청**만 주고 받는 것.
- HTTP 1.0

> [!summary]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605225357.png|400]]
> - 연결 설정 → 데이터 통신 → 연결 해제
> - 이거를 데이터 하나 주고 받을 때마다 함.
> - 속도가 ㅈㄴ 느림.


#### Example : persisitent connection
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604194210.png|450]]

- **한 번 연결하면 데이터 통신을 계속**



#### Persistent Connection
- HTTP 1.1
	- HTTP 1.1에서 부터는 persistent connection 사용.
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605225448.png|400]]

> [!warning]
> - HTTP 1.1에서는 파이프라이닝 방식 또한 사용한다.
> 	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605225732.png|400]]
> 	- 요청을 여러 개를 한 번에 보내는 것.
> - head of blocking 문제가 발생할 수 있다.
> 	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605230002.png|400]]
> 	- 파이프라이닝에서 REQUEST 1번을 처리하는 데에 시간이 엄청 오래걸리면 REQUEST 2, 3번은 시간이 오래 걸리지 않음에도 client는 응답을 받지 못하고 대기해야한다. 

> [!etc]
> - multiplexed stream으로 따로따로 나눠서 전송하여 HOB 문제 해결 → HTTP 2.0
> - UDP 사용 : QUIC → HTTP 3.0


### Format of Request and Response message
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604194644.png|500]]


#### Example
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604194807.png|500]]

> [!seealso]
> - [쿠키](https://mysterious-dev.tistory.com/11)


## Crptography And Network Security
### Objective
- 첫 번째 섹션
	- 기밀성과, 무결성, 가용성 같은 보안 목표에 대해 설명한다. 
		- **기밀성(confidentiality)** : 당사자만 데이터를 볼 수 있어야
		- **무결성(integrity)** : 데이터가 바뀌면 안된다.
		- **가용성(availability)** : 내가 쓰고 싶을 때 쓸 수 있도록
	- 스누핑(snooping) 및 트래픽 분석(traffic analysis)과 같은 공격으로 인해 기밀성이 어떻게 위협 받는지 설명한다.
	- 그런 다음 modification(수정), masquerading, replaying 및 repudiation과 같은 공격으로 인해 무결성이 어떻게 위협받는지 설명한다.
	- 이 섹션에서 가용성을 위협하는 한 가지 공격인 denial of service(DOS)에 대해 언급한다.

- 두 번째 섹션에서는 기밀성(confidentiality)에 대해 설명한다.
	- 먼저 대칭키 암호(symmetric-key ciphers)에 대해 설명하고 치환(substitution) 암호와 전치 암호(transposition)와 같은 전통적인 대칭 키 암호에 대해 설명한다.
	- 그런 다음 현대 대칭키 암호로 이동하여 현대 블록 및 스트림 암호에 대해 설명한다.
	- 또 이 섹션에서는 DOS가 가용성에 대한 공격임을 보인다.

- 세 번째 섹션에서는 보안의 다른 측면인 메시지 무결성(message integrity), 메시지 인증(message authentication), 전자 서명(digital signature)에 대해 설명한다. 
	- 이러한 측면은 오늘날 기밀서을 보완하는 보안 시스템의 일부이다.
	- 이 섹션에서는 대칭 키 및 비대칭 키 암호에 대한 키 배포를 포함한 키 관리에 대해서도 설명한다.


### Introduction
- 우리는 정보화 시대에 살고 있다. 정보는 다른 자산과 마찬가지로 가치를 지닌 자산이다.
- 자산으로서 정보는 공격으로부터 보호되어야 한다.
- 정보를 안전하게 보호하려면 무단 액세스로부터 정보를 숨기고(**기밀성** : confidentiality), 무단 변경으로부터 보호하며(**무결성** : integrity), 필요할 때 권한이 있는 주체가 사용할 수 있어야 한다(**가용성** : availabilty).


### Attacks
- 보안의 세 가지 목표인 기밀성, 무결성, 가용성은 보안 공격으로 인해 위협을 받을 수 있다.
- 문헌에서는 공격을 분류하는 데 다양한 접근 방식을 사용하지만, 우리는 보안 목표와 관련된 세 가지 그룹으로 분류한다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604202305.png|400]]

> [!definition]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604214329.png|500]]



### Confidentiality
- **기밀성은 암호를 사용하여 달성**할 수 있다.
- 암호는 크게 대칭키와 비대칭키의 두 가지 범주로 나눌 수 있다.
- 평문 → 암호화 → 암호문 → 복호화 → 평문


### Symmetric Key Cipher
- **대칭 키 암호**는 **암호화와 복호화 모두에 동일한 키를 사용**하며, 이 키를 양방향 통신에 사용할 수 있으므로 대칭 키 암호라고 부른다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604203015.png|500]]

#### Example

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604204404.png|500]]

- additive cipher
- key = 15

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604204445.png|500]]

> [!example]
> - 위 예시에서 key = 15를 이용하여 hello → WTAAD로 암호화
> - 복호화하는 쪽에서도 key = 15를 이용하여 WTAAD → hello로 복호화한다.


### Transposition Cipher
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604204706.png|500]]

- 위치를 바꾸는 방식으로 암호화.
- Key는 바꾼 위치의 mapping table이다.


### Modern Block Cipher
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604204906.png|500]]

- bit 하나씩이 아닌 **block 단위로 암호화**한다.


#### Components of Modern Block Cipher
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604204946.png|500]]

- Transposition : 위치를 바꾼다.
	- Straight permutation
	- Compression permutation
	- Expansion permutation
- Substituition
- Exclusive-OR
- Shift
- Swap
- Split
- Combine


### Data Encryption Standard(DES)
- 1971년, IBM은 128비트 키를 사용하여 64비트 블록에서 작동하는 LUCIFER라는 알고리즘을 개발했다.
- IBM 연구원이었던 Walter Tuchman은 LUCIFER를 개선하여 키 사이즈를 칩에 맞도록 56비트로 줄였다.
- 1977년, IBM의 Tuchman 프로젝트의 결과가 미국 국가 표준 연구소(NIST)의 **데이터 암호화 표준**으로 채택되었다.


#### General Structure of DES
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604210523.png|450]]


#### DES Function
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604210635.png|400]]


#### Key Generator
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604211050.png|500]]


### Ultimate
- **DES가 insecure함**(안전하지 않음)이 입증됐다.
	- 1997년 인터넷에서 해독하는 데에 몇 달이 걸림
	- 1998년 전용 H/W(EFF)에서 며칠이 걸림
	- 1999년 위의 두 가지를 합쳐 22시간 만에 풀림.
- 트리플 DES
	- 말 그대로 트리플 DES
	- 트리플 DES 키의 길이는 192비트이다. 3개의 64비트 DES 키로 간주할 수 있다.
	- DES는 crack되고, 트리플 DES는 느리다.
- 1997 : **AES 발표**, 알고리즘 요청
	- 1998년 8월 : 15개의 후보 알고리즘
	- 1999년 8월 : 최종 후보 5개
	- 2000년 10월 : Rijndael 선정
		- 두 명의 벨기에인 : Joan Daemon, Vincent Rijmen
	- 2001년 5월 : 의견 수렴기간 종료
	- 2001년 여름 : 최종 확정, '06년까지 인증 완료


### AES(Advanced Encryption Standard)
- DES와 유사 : (모드가 다른) 블록 암호, 128-bit 블록이라는 점에서 같다.
- 128-bit, 192-bit, 혹은 256-bit 키가 이용된다.
- 순열의 혼합, "S-box"
- 다항식을 사용한 **modular(나머지) 연산**에 기반한 S-box
	- 비선형(Non-linear)
	- 분석하기에 쉽고, 공격 실패를 증명한다.


### Asymmetric Key Cipher
- 이 섹션에서는 **비대칭 키 암호**에 대해 설명을 시작한다.
- 대칭 키 암호와 비대칭 키 암호는 병행에서 존재하며, 커뮤니티에 계속 서비스를 제공할 것이다.
- 사실 대칭키 암호와 비대칭키 암호는 서로를 보완하는 관계이며, 한 쪽의 장점이 다른 쪽의 단점을 보완할 수 있다고 믿는다.


#### Locking and Unlocking
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604212653.png|500]]

- 이전 방식에서는 키를 수신자, 송신자 둘 다 공유했다.
	- 이 둘이 키를 나눠갖는데 만약 키가 감청당하면?
- 이 방식에서는 **키를 두 개** : **public**(이건 공개됨), **private** 가진다.
- **수신자의 public키로 암호화**한다. public키는 **상대(수신자)의 private key로만 풀린다**.


#### General Idea of a Asymmetric-key Cipher
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604212836.png|500]]


#### RSA
- 1977년 MIT의 Rivest, Shamr, Adelman이 개발
- 가장 잘 알려져 있고 널리 사용되는 **공개 키 체계(public-key scheme)**
- 소수를 modulo한 정수에 대한 유한(Galois) 필드에서의 지수화 기반
- 큰 정수를 사용한다.(예 : 1024비트)
	- 지수는 $O((log\space n)^3)$ 연산(복잡도)이 든다.(쉬움)
- 큰 숫자를 (소인수)분해 하는 데 드는 비용을 통한 보안
- 분해에는 $O(e^{log \space n \space log \space log \space n})$ 연산이 든다.(어려움)
	- e의 n승으로 높아진다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604213604.png|500]]

- **modulo 연산을 사용**한다.


### Other Aspects of Security
- 지금까지 공부한 암호화 시스템은 기밀성을 제공한다.
- 그러나 현대의 통신에서는 무결성, 메시지 및 엔티티 인증(entity authentication), nonrepudiation(부인 방지), key management 등 보안의 다른 측면도 고려해야 한다. 
- 이 섹션에서는 이러한 문제에 대해 간략하게 설명한다.


### Message Integrity
- **데이터가 바뀌지 않았음**을 증명
- 비밀 유지가 필요하지 않더라도 무결성을 유지해야 하는 경우가 있는데, 바로 메시지가 변하지 않아야 하는 경우이다.

> [!example]
> - 예를 들어, 앨리스가 사망 시 유산을 분배하기 위해 유언장을 작성할 수 있다.
> - 이 유언장은 암호화할 필요가 없다.
> - 앨리스가 사망한 후에는 누구나 유언장을 검토할 수 있지만 유언장의 무결성은 보존되어야 한다.
> - 앨리스는 유언장의 내용이 변경되는 것을 원하지 않는다.


#### Message and Digest
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604214750.png|500]]

- 메세지가 변하지 않았다는 걸 보장한다.
- 암호화 해시 함수 : Cryptographic Hash Function 사용 → 이렇게 나온 값이 digest
	- client와 server가 같은 해시 함수를 가진다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240610023857.png|580]]

> [!info]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240606114102.png|400]]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240606114116.png|400]]


#### Message Authentication
- **메시지의 송신자**를 찾고 싶다.
- digest는 메시지가 변경되지 않았는지 메시지의 무결성을 확인하는 데 사용할 수 있다.
- 메시지의 무결성과 데이터 원본 인증(origin authentication), 즉 다른 사람이 아닌 앨리스가 메시지의 발신자라는 것을 보장하려면 이 과정에서 앨리스와 밥이 공유하는 (제 3자가 갖고 있지 않은) 비밀을 포함시켜야 하며, 메시지 인증 코드(**MAC**, message authentication code)를 만들어야 한다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604215136.png|500]]


#### Digital Signature
- 메시지 무결성 및 메시지 인증을 제공하는 또 다른 방법(또한 곧 살펴볼 더 많은 보안 서비스)은 **전자서명(digital signature)** 이다. 
- MAC은 비밀 키(secret key)를 사용하여 digest를 보호하고, **전자 서명은 private-public key쌍을 사용**한다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604215328.png|500]]

- 앨리스의 private key로 암호화한 데이터를 보내고 밥이 앨리스의 public key로 이걸 풀 수 있으면 이건 alice가 보낸 것이라는 뜻.


#### Using a Trusted Center for non-repudiation
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240604215454.png|500]]

- 앨리스와 밥 사이에 **Trusted center**를 두어 앨리스가 보냈다는 것을 증명한다.
- 앨리스가 자기가 보낸 데이터가 아니라고 부인하는 것을 방지하기 위함. **부인 방지(non-repudiation)**


## Internet Security
### Outline
- 첫 번째 섹션에서는 네트워크 계층의 보안인 IPSec에 대해 설명한다.
	- 이 섹션에서는 전송 모드(transport mode)와 터널 모드(tunnel mode)의 두 가지 IPSec 모드에 대해 설명한다.
	- 그 다음 프로토콜의 두 가지 버전 : AS와 ESP에 대해 설명한다.

- 두 번째 섹션에서는 전송 계층의 보안 프로토콜 중 하나인 SSL에 대해 설명한다(다른 프로토콜인 TLS도 유사하다).
	- 서비스, 알고리즘, 매개변수 생성 등 SSL 아키텍처에 대해 설명한다.
	- 그런 다음 SSL을 구성하는 네 가지 프로토콜에 대해 설명한다.
		- Handshake, ChangeCipherSpec, Alert, Record

- 세 번째 섹션에서는 침입자의 악의적인 의도로부터 기업을 보호할 수 있는 기술인 방화벽(firewall)에 대해 설명한다.
	- 패킷 필터 방화벽(packet-filter filrewall)과 프록시 방화벽의 두 가지 버전에 대해 설명한다.
	- 첫 번째는 네트워크 계층에서만 보안(protection) 기능을 제공하고 두 번째는 응용 계층에서 보안 기능을 제공할 수 있다.


### Network Layer Security
- 이 Chapter는 **네트워크 계층의 보안**에 대한 논의로 시작한다.
- 네트워크 계층에서는 두 호스트, 두 라우터 혹은 호스트와 라우터 간에 보안이 적용된다.
- 네트워크 계층 보안의 목적은 네트워크 계층의 서비스를 직접 사용하는 애플리케이션을 보호하는 것이다.

> [!info]
> - [IPSec](https://aws.amazon.com/ko/what-is/ipsec/)
> - [IPSec](https://www.cloudflare.com/ko-kr/learning/network-layer/what-is-ipsec/)
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240606115906.png|200]]

#### Transport Model
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605001052.png|500]]

- **IPSec 방식**으로 암호화한다.
- payload를 암호화하고 헤더를 붙여서 전송.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240606115043.png|600]]


#### Tunnel Mode
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605001127.png|500]]

- 기존 Header와 payload를 모두 암호화하고 새로운 헤더를 붙여서 전송

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240606115114.png|600]]

### Two Security Protocols
- IPSec은 IP 수준에서 패킷에 대한 인증 및 암호화를 제공하기 위해 **Authentication Header(AH, 인증 헤더)** 프로토콜과 **Encapsulating Security Payload(ESP)** 프로토콜이라는 두 가지 프로토콜을 정의한다.


#### Authentication Header Protocol
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605001533.png|500]]

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240606115159.png|600]]

#### Encapsulating Header Protocol
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605001614.png|500]]

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240606115319.png|600]]

### Virtual Private Networks(VPN)
- IPSec의 Application 중 하나는 **virtual private networks(VPN, 가상 사설망)** 이다.
- VPN은 조직 내부 및 조직 간 통신을 위해 global internet을 사용하는 대규모 조직에서 인기를 얻고 있는 기술이다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605001815.png|500]]

- R1과 R2 사이의 **tunnel처럼**(둘만 통신하는 것처럼).

> [!additional explanation]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240606115449.png|600]]


### Transport Layer Protocol
- 전송 계층의 보안은 연결 지향 프로토콜인 TCP의 서비스를 사용하는 응용 계층에 보안을 제공한다.
- 현재 전송 계층에서 보안을 제공하는 데는 **Secure Socket Layer(SSL, 보안 소켓 계층)** 프로토콜과 **Transport Layer Security(전송 계층 보안)** 프로토콜이라는 두 가지 프로토콜이 주로 사용되고 있다.


#### SSL architecture
- SSL은 응용 계층에서 생성된 데이터에 **보안 및 압축 서비스를 제공**하도록 설계 되었다.
- 일반적으로 SSL은 모든 응용 계층 프로토콜에서 데이터를 수신할 수 있지만 **대체로 프로토콜은 HTTP**이다.
- application에서 수신한 데이터는 **압축(optional), 서명(signed) 및 암호화**된다.
- 그런 다음 데이터는 TCP와 같은 신뢰할 수 있는 전송 계층 프로토콜로 전달된다.
- Netscape는 1994년에 SSL을 개발했다. version 2, version 3는 1995년에 출시됐다.
- 이 섹션에서는 SSLv3에 대해 설명한다.


##### Four Protocols
- SSL은 두 계층으로 구성된 네 가지 프로토콜을 정의한다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605003319.png|400]]

> [!additional explanation]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240610022845.png|450]]


#### SSL Protocol
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605003406.png|500]]

- 기본적으로 암호화 제공
	- 중간에 있는 애들(ex : 라우터)이 데이터를 볼 수 없다.

##### SSL/TLS
- 데이터를 암호화하는 통신 프로토콜
	- 데이터를 암호화하여 제3자가 데이터를 볼 수 없게 보호한다.(기밀성)
	- 데이터 변조 여부를 검증한다.(무결성)
	- 상호 인증을 지원한다.(통신 상대 인증)


![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240610023608.png]]

> [!additional explanation]
> - [참고](https://youtu.be/KpyzbEFYE_E?si=NnsutmBRskDWh3lL)
> - HTTPS의 동작과정
> 	- SSL/TLS handshaking
> 	- server는 CA(Certificate Authority 인증기관, ㅈㄴ 믿을 수 있다.)에게 공개키를 공개해야
> 		- server는 자신의 공개키가 있고 그 공개키가 올바른 공개키인지 CA에 등록해야 한다.
> 		- 서버는 인증 기관에 서버 인증서를 발급 받는다.
> 		- 인증서는 서버 공개키와 서버 정보를 인증 기관의 개인키로 암호화한 것.
> 	- 브라우저는 server에 접속 → 서버는 자신의 인증서(공개키)를 준다.
> 		- 브라우저는 CA에게 제대로 된 공개키인지 물어본다.
> 		- CA에게 CA의 공개키를 받고 그걸로 인증서를 복호화 →서버 정보와 공개키를 얻을 수 있다.
> 	- 브라우저가 이번 연결에서 사용할 세션키를 만든다.
> 	- 내가 만든 세션키를 서버의 공개키로 암호화하여 전송
> 		- 서버 말고는 내 세션키 아무도 못 봄
> 	- 서버가 받고 개인키로 그걸 푼다.
> 	- 양쪽 다 세션키 공유 됐으니까 그걸로 통신.

> [!etc]
> - HSTS(HTTP Strict Transport Security) 
> 	- HTTP헤더에 HSTS라는 헤더를 설정해서 자동으로 HTTPS로 리다이렉트
> 


### Firewalls 방화벽
- 이전의 모든 보안 조치로는 제 3자가 시스템에 유해한 메시지를 보내는 것을 막을 수 없다.
- 시스템에 대한 **액세스를 제어**하려면 방화벽이 필요하다.
- 방화벽은 조직의 내부 네트워크와 나머지 인터넷 사이에 설치되는 장치(일반적으로 라우터 또는 컴퓨터)이다.
- 방화벽은 일부 패킷은 전달하고 다른 패킷은 필터링(not forward)하도록 설계되었다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605003729.png|450]]

- 나한테 들어오거나 나가는 트래픽(데이터)을 제어. 
	- 대체로 **라우터**에 있다.


#### Packet-Filter Firewalls
- 방화벽은 **패킷 필터**로 사용될 수 있다.
- 방화벽은 네트워크 계층 및 전송 계층 **헤더의 정보** : source 및 destination의 **IP주소, port 번호, 프로토콜 유형(TCP인지 UDP인지)를 기반**으로 패킷을 전달하거나 차단할 수 있다.
- 패킷 필터 방화벽은 필터링 테이블을 사용하여 어떤 패킷을 버려야 하는지(not forwarded) 결정하는 라우터이다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605004120.png|450]]

> [!problem]
> - IP와 포트번호만 보고 패킷을 차단하는데, IP는 VPN을 통해 바꾸면 된다.
> - 즉, IP주소는 의미가 없고 실제 데이터를 봐야 한다.


#### Proxy firewall
- 패킷 필터 방화벽은 네트워크 계층에서 사용할 수 있는 네트워크 계층 및 전송 계층 헤더(IP 및 TCP/UDP)에서 **사용 가능한 정보를 기반**으로 한다.
- 그러나 때로는 **메시지 자체**에서(응용 계층에서) 사용 가능한 정보를 기반으로 메시지를 필터링해야 하는 경우도 있다.

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605004503.png|500]]

