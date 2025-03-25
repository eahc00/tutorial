
## Unicast Routing
- 주소를 보고 주소에 대해 어느 쪽으로 가야할지를 결정

### Objective
- 첫 번째 섹션에서는 unicast routing의 개념을 소개하고 그 이면에 있는 일반적인 아이디어를 설명한다.
	- 그런 다음 least-cost routing(최소 비용 라우팅)과 least-cost trees(최소 비용 트리)에 대해서 설명한다.

- 두 번째 섹션에서는 인터넷에서 사용되는 일반적인 라우팅 알고리즘에 대해 설명한다.
	- 이 섹션에서는 먼저 Distance-Vector routing에 대해 설명한다.
	- 그런 다음 link-state routing에 대해 설명한다.
	- 마지막으로 path-vector routing에 대해 설명한다.

- 세 번째 섹션에서는 먼저 Distance-Vector routing 알고리즘을 구현하는 프로토콜인 RIP에 대해 설명한다.
	- 그런 다음 link-state routing 알고리즘을 구현하는 프로토콜인 OSPF에 대해 설명한다.
	- 마지막으로 path-vector routing 알고리즘을 구현하는 프로토콜인 BGP에 대해 설명한다.


### Introduction
- 많은 수의 라우터와 수많은 호스트가 있는 인터넷에서 유니캐스트 라우팅은 **계층적 라우팅(hierarchical routing : 서로 다른 라우팅 알고리즘을 사용하여 여러 단계로 라우팅)** 을 사용해야만 수행할 수 있다.
- 이 섹션에서는 먼저 인터넷에서 유니캐스트 라우팅의 일반적인 개념에 대해 설명한다.
- 라우팅 개념과 알고리즘을 이해한 후에는 이를 인터넷에 적용하는 방법을 설명한다.


### General Idea
- 유니캐스트 라우팅에서 패킷은 **포워딩 테이블**을 사용하여 source에서 destination까지 **한 hop씩(hop-by-hop, 한 번에 하나씩 넘어감) 라우팅** 된다.
- source host는 로컬 네트워크의 기본 라우터(default router)로 패킷을 전달하므로 포워딩 테이블이 필요하지 않다.
- destination host 또한 로컬 네트워크의 기본 라우터에서 패킷을 수신하기 때문에 포워딩 테이블이 필요하지 않다.
- 즉, **인터넷에서 네트워크를 연결하는 라우터에만 포워딩 테이블이 필요**하다.

> [!my_question]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240605221409.png|400]]
> - router간에 통신에만 포워딩 테이블이 사용된다?
> - router와 host간 포워딩에서는 포워딩 테이블이 필요 없다?




### Least-Cost Routing
- **가장 비용이 적은 경로**
- 인터넷을 weighted graph로 모델링할 때 source 라우터에서 destination 라우터까지의 최적 경로를 설명하는 방법 중 하나는 둘 사이의 비용이 가장 적게 드는 경로를 찾는 것이다.
- 즉, source 라우터는 가능한 모든 경로 중에서 경로의 총 비용이 가장 적게 드는 방식으로 destination 라우터로 가는 경로를 선택한다.


#### An internet and its graphical representation
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521125816.png|500]]

- The **weighted graph**
	- 2차원 배열이나 linked list로 표현


#### Least-cost trees for nodes in the internet
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521125923.png|500]]


### Routing Algorithms
- 과거에는 여러 가지 라우팅 알고리즘이 설계되었다. 
- 이러한 방법의 차이점은 최소 비용을 해석하는 방식과 각 노드에 대해 **최소 비용 트리(least-cost tree)를 생성**하는 방식에 있다.
- 이 섹션에서는 일반적인 알고리즘에 대해 설명하며, 이후 인터넷의 라우팅 프로토콜이 이러한 알고리즘 중 하나를 구현하는 방법을 보여준다.


#### Distance-Vector Routing
- **Distance-Vector(DV)** Routing은 Introduction에서 설정한 목표를 사용하여 최적의 경로를 찾는다.
- DV 라우팅에서 각 노드가 가장 먼저 생성하는 것은 바로 옆 노드에 대한 기초적인 정보를 통한 자기만의 least-cost tree이다.
- 불완전한 트리는 **가까운 이웃 사이에서 교환**되어 트리를 점점 더 완전하게 만들고 전체 인터넷을 나타낸다.
- DV 라우팅에서 라우터는 전체 인터넷에 대해 알고 있는 정보를 (불완전한 지식일 수 있지만) 모든 이웃 라우터에게 지속적으로 전달한다고 할 수 있다.


##### Graphical idea behind Bellman-Ford equation
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521131652.png|400]]


> [!info]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521132635.png|400]]
> - [벨만포드](https://ttl-blog.tistory.com/1043)
> - [다익스트라](https://great-park.tistory.com/133)


##### The distance vector corresponding to a tree
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521132721.png|400]]

- 트리로부터 만들어진 **DV 테이블을 보고 비용을 산출**한다.


##### The first distance vector for an internet
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521132857.png|400]]

> [!example]
> - A는 B와 D(이웃)에게 정보를 받아서 update
> - → 이걸 더 이상 업데이트 할 필요가 없을 때까지(업데이트가 되지 않을 때까지) 반복


##### Updating distance vectors
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521133029.png|450]]

- Key idea
	- 시간에 따라, 각각의 노드는 **자체 DV 추정치를 이웃 노드에 전송**한다.
	- x가 이웃으로부터 새로운 DV 추정치를 받으면 B-F 방정식을 사용하여 자신의 DV를 업데이트한다.
$$D_x(y) \leftarrow min_v\{c(x,v) +  D_v(y)\} \space for \space each \space node \space y \in N$$


##### Distance vector algorithms
- iterative, asynchronous 
	- 각 local iteration은 다음에 의해 발생된다.
		- 로컬 링크 비용(cost) 변경
		- 이웃으로부터의 DV 업데이트 메시지
	- distributed
		- 각 노드는 자신의 DV가 변경될 때만 이웃 노드에게 알린다.
		- 이웃 노드는 필요한 경우 그들의 이웃 노드에게 알린다.

> [!abstract]
> - wait for(로컬 링크 cost가 변경 혹은 이웃으로 부터의 메시지를 기다린다.)
> - 추정치 재계산(recompute)
> - 만약 destination DV가 변경된 경우 이웃 노드에게 알린다.


##### Two-node instability
> [!problem]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521141831.png|500]]

> [!example]
> - a. X에 A는 1만큼, B는 A를 통해 2만큼에 갈 수 있다
> - b. A와 X와의 연결이 끊어지면 A에서 X로의 비용은 16이 되고 끊어진 링크가 된다. B는 여전히 A를 통해 2만큼에 갈 수 있다는 정보를 가지고 있다.
> - c. A는 B에게서 새로운 정보를 받고 B를 통해 3만큼에 갈 수 있다고 update된다.
> - d. B는 다시 A에게 새로운 정보를 받고 4로 update된다. → 서로 잘못된 정보(entry)를 계속 주고받는 문제 발생
> - e. 둘 다 무한대의 거리를 가지게 된다.


##### Solution
- Infinite to Count Problem(무한 계산 문제)
	- **상대방에게 받은 정보는 다시 상대방에게 주면 안된다.**
- **Split Horizon**(분할 지평선)
	- 이 기법의 각 노드는 모든 인터페이스를 통해 테이블을 넘기지 않고 각 인터페이스에 걸쳐 테이블의 일부를 전달한다.
	- 노드 B가 X로 이동하는 가장 좋은 방법이 노드 A를 통하는 것이라는 정보를 갖고 있다면, 노드 B는 이 정보를 노드 A가 이미 제공했기 때문에(A는 이미 알고 있음) 노드 A에게 알릴 필요가 없다.

> [!info]
> ![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240607194705.png|500]]


#### Link State Routing
- least-cost tree 및 포워딩 테이블 생성에 대한 논의에 바로 이어지는 라우팅 알고리즘은 **Link-State(LS) 라우팅**이다.
- 이 방법은 link-state라는 용어를 사용하여 인터넷에서 네트워크를 나타내는 link(edge)의 특성을 정의한다.
- 이 알고리즘에서는 에지와 관련된 비용이 링크의 상태를 정의한다.
- lower cost 링크가 higher cost 링크보다 선호되며, 링크의 cost가 무한대인 경우 링크가 존재하지 않거나 끊어진 것을 의미한다.


##### Example of a link-state database
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521143255.png|500]]

- **다익스트라(Dijkstra) 알고리즘**을 사용한다.


##### LSPs created and sent out by each node to build LSDB
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521144152.png|450]]

- 서로 이 테이블들을 서로 다 교환
	- → 모든 정보를 담은 하나의 큰 테이블을 만듦(이전 페이지 : **Link state database**)


##### A Link-State Routing Algorithm
- **Dijkstra's algorithm**
	- link cost가 모든 링크에 알려진 네트워크 토폴로지.
		- **link state broadcast**를 이용하여 달성된다.
		- 모든 노드가 동일한 정보를 보유한다.
	- 한 노드(source)에서 다른 모든 노드까지 최소 비용 경로를 계산한다.
		- 해당 노드에 대한 포워딩 테이블을 제공한다.
	- 반복(Iterative) : k번 반복 이후, k개의 목적지까지 최소 비용 경로를 알 수 있다.

- notation
	- c(x,  y) : node x로부터 y까지의 link cost : 이웃까지의 방향이 없으면 $\infty$
	- D(v) : source로부터 destination v까지의 경로의 비용의 현재 값. 
	- p(v) : source로부터 v까지의 경로를 따르는 이전 노드
	- N' : 최고 비용 경로가 확실하게 알려진 노드 집합.

- Dijsktra's algorithm

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521145340.png|450]]


##### Dijkstra's algorithm : example
- link-state : **모든 토폴로지의 정보**를 받아서 경로를 찾아냄.
- DV(distance vector) : **이웃 정보**만 받음.
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521145543.png|300]]

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521145556.png|300]]

- 이전 노드를 추적하여 최단 경로 트리를 구성할 수 있다.
- 동일한 cost가 존재할 수 있다. (임의로 끊을 수 있음)

![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521150235.png|400]]

- u에서의 forwarding table은 이웃 경로에 대해 나타나짐.


#### Path-Vector Routing
- link state routing과 distance vector routing은 모두 최소 비용(least-cost)목표를 기반으로 한다.
- 하지만 least-cost 목표가 우선순위가 아닌 경우도 있다.
- 예를 들어, 인터넷에서 송신자가 자신의 패킷이 통과하지 못하게 하려는 라우터가 있다고 가정하자.
- 즉, LS 또는 DV 라우팅이 적용하는 최소 비용 목표는 발신자가 패킷의 경로에 특정 정책을 적용하는 것을 허용하지 않는다.
- 이러한 요구에 대응하기 위해 **경로 벡터(PV, Path Vector) 라우팅**이라는 세 번째 라우팅 알고리즘이 고안되었다.
	- **특정 정책을 적용.**


##### Path vectors made at booting time
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521152033.png|400]]
- DV는 비용을 저장&전달한다.
- PV는 내가 지나가는 Path에 대한 정보를 넘겨준다.
- 경로를 보고 내가 업데이트 할지말지를 결정
	- **정책**에 따라서 갈 수도, 안 갈 수도 있다.


##### Updating path vectors
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521152155.png|450]]

- minimum이 아닌 **best**로 계산한다.


### Unicast Routing Protocols
- 소개 이후 인터넷에서 사용되는 세 가지 일반적인 프로토콜에 대해 설명한다.
- 거리 벡터 알고리즘을 기반으로 하는 **라우팅 정보 프로토콜(RIP, Routing Inforamtion Protocol)**, 링크 상태 알고리즘을 기반으로 하는 **최단 경로 우선 개방형 프로토콜(OSPF, Open Shortest Path First)**, 경로 벡터 알고리즘을 기반으로 하는 **보더 게이트웨이 프로토콜(Boader Gateway Protocol)** 에 대해 설명한다.


#### Hop counts in RIP
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521153942.png|500]]

- **hop 수** : 비용을 가지고 weigth를 준다.


##### Forwarding tables
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521154410.png|450]]

- 서로 교환해서 update하면 된다.(거리 벡터 DV 알고리즘 기반)

> [!my_question]
> - Destination network는 CIDR로 표기되는 IP address인가요?
> 	- 그럴 수도 있다.




##### RIP message format
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521154833.png|400]]


##### Example of an autonomous system using RIP

- 초기 상태
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521154951.png|470]]

- update
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521155144.png|500]]

- update
	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521155219.png|500]]


#### Open Shortest Path First
- Open Shortest Path First(OSPF)도 RIP와 같이 도메인 내 라우팅 프로토콜이지만, 이 장의 앞부분에서 설명한 링크 상태 라우팅 프로토콜을 기반으로 한다.
- OSPF는 개방향 프로토콜이므로 사양이 공개 문서로 되어 있다.

- RIP는 비용을 hop으로(몇 개의 라우터를 지나는지로) 책정
- OSPF는 **비용을 임의로 책정 가능**(시간 등).

##### Metric in OSPF
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521160317.png|500]]


##### Forwarding tables in OSPF
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521160451.png|500]]

- 비용 기준만 다를 뿐 update 방법은 같다.


##### OSPF message formats
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521160611.png||500]]


#### Boader Gateway Protocol
- **Boader Gateway Protocol version 4(BGP4)** 는 오늘날 인터넷에서 사용되는 유일한 도메인 간 라우팅 프로토콜이다.
- BGP4는 앞서 설명한 **경로 벡터 알고리즘(비용보다 정책을 우선)** 을 기반으로 하지만 인터넷에서 **네트워크의 도달 가능성에 대한 정보**를 제공하도록 맞춤화되어 있다.

> [!my_question]
> - 도메인 간 라우팅 프로토콜이 뭔 말인가요? 도메인의 범위가 뭘 말하는 건가요?
> 	![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240608160116.png|400]]


##### A sample internet with four ASs
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521161038.png|550]]

- link-state, DV를 소규모 네트워크(LAN)에서는 사용할 수 있다.
	- **밖으로 보낼 때는 정책 우선 → Path**
- 왜? 내 네트워크는 내 관리니까 빠른 게 중요
	- 밖에서는 보안 등 정책이 더 중요


##### eBGP Operation
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521161231.png|500]]

- 이러한 정보들을 교환하면서 **Best를 찾으면 된다.**


##### Combination of eBGP and iBGP sessions in out internet
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521161432.png|500]]


##### Finalized BGP path tables
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521161533.png|500]]


##### Forwarding tables after injuction from BGP
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521161644.png|500]]

- 여기서 R1과 같은 라우터는 내부, 외부 통신을 위한 알고리즘을 두 개씩 돌려야
	- 내부로는 DV, LS 기반의 RIP, OSPF 등을 돌릴 수 있고 외부로는 PV기반의 BGP를 돌림.


![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521162005.png|500]]


##### Flow diagram for route selection
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521162030.png|500]]

- 마지막에 다른 네트워크와 연결돼있는 라우터는 이런 복잡한 알고리즘이 요구된다.


##### BGP Messages
![[CNU/3-1/컴퓨터 네트워크/images/Pasted image 20240521162112.png|500]]



