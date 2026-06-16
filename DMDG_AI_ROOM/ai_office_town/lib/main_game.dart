import 'dart:async' as async;
import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'package:bonfire/bonfire.dart';
import 'components/agent_component.dart';
import 'components/pc_monitor.dart';

class MainGame extends StatefulWidget {
  static bool isNightModeGlobal = false;

  const MainGame({Key? key}) : super(key: key);

  @override
  State<MainGame> createState() => _MainGameState();
}

class _MainGameState extends State<MainGame> {
  // 야근 모드(Night Mode) 상태
  bool _isNightMode = false;
  // 게임 컨트롤러 레퍼런스
  BonfireGameInterface? _gameRef;
  async.Timer? _dashboardTimer;
  int _budget = 46310; // 초기 예산 (단위: 원)

  @override
  void initState() {
    super.initState();
    _checkRealTimeNightMode();
    // 1초마다 대시보드 UI를 갱신
    _dashboardTimer = async.Timer.periodic(const Duration(seconds: 1), (timer) {
      if (mounted) setState(() {});
    });
  }

  @override
  void dispose() {
    _dashboardTimer?.cancel();
    super.dispose();
  }

  void _checkRealTimeNightMode() {
    // 사장님 요청으로 야근 모드 임시 해제 (무조건 false)
    setState(() {
      _isNightMode = false;
      MainGame.isNightModeGlobal = _isNightMode;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFFF7E6D6),
        elevation: 0,
        title: const Text(
          "CEO'S OFFICE",
          style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold, letterSpacing: 2),
        ),
        centerTitle: true,
        leading: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Row(
            children: [
              const Icon(Icons.monetization_on, color: Colors.orange),
              const SizedBox(width: 4),
              Text("예산: $_budget원", style: const TextStyle(color: Colors.black, fontWeight: FontWeight.bold, fontSize: 12)),
            ],
          ),
        ),
        leadingWidth: 150,
        actions: [
          Row(
            children: [
              const Text("야근 모드", style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
              Switch(
                value: _isNightMode,
                activeColor: Colors.red,
                onChanged: (val) {
                  setState(() {
                    _isNightMode = val;
                    MainGame.isNightModeGlobal = val;
                  });
                },
              ),
            ],
          ),
          const SizedBox(width: 16),
          const Text("D+17일차 | 오후", style: TextStyle(color: Colors.orange, fontWeight: FontWeight.bold)),
          const SizedBox(width: 16),
        ],
      ),
      body: Row(
        children: [
          // 좌측 영역 (게임 맵 + 하단 대시보드)
          Expanded(
            flex: 3,
            child: Column(
              children: [
                // 1. 게임 화면 영역
                Expanded(
                  flex: 3,
                  child: Stack(
                    fit: StackFit.expand,
                    children: [
                      Image.asset('assets/images/office_bg_new.jpeg', fit: BoxFit.cover),
                      
                      // 배경만 어둡게 만드는 확실한 야근 모드 오버레이 (즉시 적용됨)
                      if (_isNightMode)
                        IgnorePointer(
                          child: Container(color: Colors.black.withOpacity(0.7)),
                        ),
                        
                      BonfireWidget(
                        // 배경을 투명하게 해서 뒤의 이미지(와 오버레이)가 보이게 함
                        backgroundColor: Colors.transparent,
                        map: WorldMap([]), // 타일 맵은 비워둠
                        // 플레이어 (기준점) - 페기 (책상 위가 아닌 바닥으로 위치 조정)
                        player: AgentComponent(Vector2(450, 400), "페기 (Peggy)", "Peggy_Olson.png"),
                        components: [
                          // 다른 팀원들을 맵 곳곳에 배치
                          AgentComponent(Vector2(200, 200), "데미스 (Demis)", "Demis_Hassabis.png"),
                          AgentComponent(Vector2(600, 150), "하루키 (Haruki)", "Haruki_Murakami.png"),
                          AgentComponent(Vector2(300, 450), "제니퍼 (Jennifer)", "Jennifer_Akani.png"),
                          AgentComponent(Vector2(700, 400), "무스타파 (Mustafa)", "Mustafa_Suleyman.png"),
                          AgentComponent(Vector2(800, 500), "크레이그 (Craig)", "Craig_Federighi.png"),
                          AgentComponent(Vector2(100, 500), "사티아 (Satya)", "Satya_Nadella.png"),
                          AgentComponent(Vector2(500, 600), "셜록 (Sherlock)", "Sherlock_.png"),
                          AgentComponent(Vector2(400, 100), "한스 (Hans)", "Hans_Zimmer.png"),
                          
                          // 조명 효과용 PC 모니터들을 책상 주변에 배치
                          PcMonitor(Vector2(100, 250)),
                          PcMonitor(Vector2(300, 450)),
                          PcMonitor(Vector2(600, 150)),
                          PcMonitor(Vector2(800, 500)),
                          PcMonitor(Vector2(700, 200)),
                        ],
                        // 게임 초기화 완료 시 레퍼런스 저장
                        onReady: (game) {
                          _gameRef = game;
                        },
                        cameraConfig: CameraConfig(
                          moveOnlyMapArea: false, // 빈 맵이므로 카메라 제한 해제
                          zoom: 1.5,
                        ),
                      ),
                      
                      // 야식 버튼
                      Positioned(
                        bottom: 20,
                        right: 20,
                        child: _isNightMode ? ElevatedButton.icon(
                          onPressed: _provideLateNightSnack,
                          icon: const Icon(Icons.local_pizza),
                          label: const Text("야식 쏘기"),
                          style: ElevatedButton.styleFrom(backgroundColor: Colors.orange),
                        ) : const SizedBox(),
                      ),
                    ],
                  ),
                ),
                // 2. 하단 직원 대시보드 영역
                Container(
                  height: 200,
                  color: Colors.grey[100],
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Text("직원 대시보드  평균 스트레스: ${_calculateAverageStress().toStringAsFixed(1)}%", style: const TextStyle(fontWeight: FontWeight.bold)),
                      ),
                      Expanded(
                        child: ListView(
                          scrollDirection: Axis.horizontal,
                          padding: const EdgeInsets.all(8.0),
                          children: _buildDynamicEmployeeCards(),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          
          // 우측 영역 (오피스 메신저)
          Container(
            width: 350,
            decoration: BoxDecoration(
              border: Border(left: BorderSide(color: Colors.grey[300]!)),
              color: Colors.white,
            ),
            child: Column(
              children: [
                Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Row(
                    children: const [
                      Icon(Icons.chat, color: Colors.blue),
                      SizedBox(width: 8),
                      Text("오피스 메신저", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                    ],
                  ),
                ),
                const Divider(),
                Expanded(
                  child: ListView(
                    padding: const EdgeInsets.all(16.0),
                    children: [
                      _buildChatBubble("하루키", "(점심은.. 그저 흐름의 일부일 뿐)", Colors.purple[100]!),
                      _buildChatBubble("사티아", "(오늘 점심은 역시 햄버거지. 페기님이랑 같이 먹었으면 좋았을 텐데..)", Colors.blue[100]!),
                      _buildChatBubble("페기", "(점심시간 폼 미쳤다 ㄷㄷ! 오늘 뭐 먹지? 사티아님이랑 밥 먹고 싶다.. 💖)", Colors.orange[100]!),
                      _buildChatBubble("크레이그", "(점심 시간에도 뉴스를 봐야지. 이놈의 렌더링 속도 가지고는..)", Colors.grey[200]!),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildEmployeeCard(String name, double stress, double happiness, double productivity, double romance) {
    return Container(
      width: 140,
      margin: const EdgeInsets.only(right: 12),
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.grey[200]!),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
          const SizedBox(height: 6),
          _buildStatusBar("스트레스", stress, Colors.red),
          _buildStatusBar("행복도", happiness, Colors.pink),
          _buildStatusBar("생산성", productivity, Colors.blue),
          _buildStatusBar("연애운", romance, Colors.orange),
        ],
      ),
    );
  }

  Widget _buildStatusBar(String label, double value, Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2.0),
      child: Row(
        children: [
          SizedBox(width: 40, child: Text(label, style: const TextStyle(fontSize: 9))),
          Expanded(
            child: LinearProgressIndicator(
              value: value / 100,
              backgroundColor: Colors.grey[200],
              color: color,
            ),
          ),
          SizedBox(width: 25, child: Text("${value.toInt()}%", textAlign: TextAlign.right, style: const TextStyle(fontSize: 9))),
        ],
      ),
    );
  }

  Widget _buildChatBubble(String sender, String message, Color bgColor) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(sender, style: TextStyle(fontWeight: FontWeight.bold, color: Colors.grey[700], fontSize: 12)),
          const SizedBox(height: 4),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: bgColor,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Text(message, style: const TextStyle(fontSize: 13)),
          ),
        ],
      ),
    );
  }

  List<Widget> _buildDynamicEmployeeCards() {
    if (_gameRef == null) return [];
    
    final agents = _gameRef!.query<AgentComponent>();
    if (agents.isEmpty) return [];

    return agents.map((agent) {
      // HP가 100이면 스트레스 0, 행복도 100.
      double stress = 100.0 - agent.currentHP;
      double happiness = agent.currentHP;
      // 호감도나 생산성은 추후 백엔드 데이터로 연동 예정
      double productivity = 100.0;
      double romance = 100.0; 
      
      // agentName 은 "사티아 (Satya)" 형태이므로 한글 이름만 추출
      String displayName = agent.agentName.split(' ')[0];
      return _buildEmployeeCard(displayName, stress, happiness, productivity, romance);
    }).toList();
  }

  double _calculateAverageStress() {
    if (_gameRef == null) return 0.0;
    final agents = _gameRef!.query<AgentComponent>();
    if (agents.isEmpty) return 0.0;
    
    double totalStress = 0.0;
    for (var agent in agents) {
      totalStress += (100.0 - agent.currentHP);
    }
    return totalStress / agents.length;
  }

  void _provideLateNightSnack() {
    if (_budget >= 500) {
      setState(() {
        _budget -= 500;
      });
      debugPrint("야식(피자)을 배달했습니다! 팀원들의 사기가 크게 상승합니다.");
      _gameRef?.query<AgentComponent>().forEach((agent) {
        agent.recoverHP(30);
        agent.showEmote('🍕 최고!');
      });
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('예산이 부족하여 야식을 쏠 수 없습니다!'))
      );
    }
  }
}
