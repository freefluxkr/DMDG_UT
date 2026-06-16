import 'dart:ui' as ui;
import 'dart:async';
import 'dart:math' as math;
import 'package:flutter/material.dart' hide Image;
import 'package:bonfire/bonfire.dart';
import 'package:flame/effects.dart';
import '../services/api_client.dart';
import '../main_game.dart';

class AgentComponent extends SimplePlayer with BlockMovementCollision, TapGesture {
  double currentHP = 100.0;
  String? currentEmote;
  double emoteTimer = 0;
  final String agentName;
  
  bool _isZombie = false;
  bool _isFled = false;
  
  double _perceiveTimer = 0;
  static const double PERCEIVE_INTERVAL = 30.0; // 30초마다 인지 (무료 API Rate Limit 방지)

  final String imageName;

  AgentComponent(Vector2 position, this.agentName, this.imageName)
      : super(
          position: position,
          size: Vector2(96, 128), // 임시 크기 (onLoad에서 원본 비율에 맞게 재조정됨)
          animation: SimpleDirectionAnimation(
            idleRight: _getPortraitAnimation(imageName),
            runRight: _getPortraitAnimation(imageName),
          ),
        );

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    final sprite = await Sprite.load(imageName);
    final originalSize = sprite.originalSize;
    // 높이를 128로 고정하고, 원본 비율에 맞춰 너비를 자동 조절합니다.
    final targetHeight = 128.0;
    final scale = targetHeight / originalSize.y;
    this.size = Vector2(originalSize.x * scale, targetHeight);
  }

  static Future<SpriteAnimation> _getPortraitAnimation(String imgName) async {
    final sprite = await Sprite.load(imgName);
    return SpriteAnimation.spriteList([sprite], stepTime: 0.1);
  }

  void showEmote(String emoji) {
    currentEmote = emoji;
    emoteTimer = 3.0; // 3초간 표시
  }

  void recoverHP(double amount) {
    currentHP += amount;
    if (currentHP > 100) currentHP = 100;
    if (currentHP > 20) {
      _isZombie = false;
      _isFled = false;
    }
    debugPrint("HP recovered! Current HP: $currentHP");
  }

  void moveTo(Vector2 target) {
    final random = math.Random();
    // 여러 에이전트가 완벽하게 겹치지 않도록 반경 넓게 랜덤 오프셋 추가
    final offsetX = (random.nextDouble() - 0.5) * 150;
    final offsetY = (random.nextDouble() - 0.5) * 150;
    
    final finalTarget = Vector2(target.x + offsetX, target.y + offsetY);
    double dur = _isZombie ? 15.0 : 4.0;
    add(MoveEffect.to(finalTarget, EffectController(duration: dur)));
  }

  void goToBreakRoom(Vector2 targetPos) {
    // 탕비실로 이동한다는 말풍선 표시
    showEmote('☕ 휴식!');
    
    // 좀비 모드면 아주 느리게 이동
    double dur = _isZombie ? 15.0 : 5.0;
    add(MoveEffect.to(targetPos, EffectController(duration: dur)));
  }

  @override
  void update(double dt) {
    super.update(dt);
    
    // --- 야근 모드 체력 감소 및 좀비화 ---
    if (MainGame.isNightModeGlobal) {
      currentHP -= dt * 1.0; // 1초에 1씩 깎임
      if (currentHP < 0) currentHP = 0;
      
      if (currentHP <= 20 && !_isZombie) {
        _isZombie = true;
        showEmote('🧟‍♂️ 살려줘..');
      }
      
      if (currentHP <= 0 && !_isFled) {
        _isFled = true;
        final random = math.Random();
        goToBreakRoom(Vector2(800 + (random.nextDouble()-0.5)*160, 250 + (random.nextDouble()-0.5)*160));
      }
    }
    // ------------------------------------

    // 이모티콘 타이머
    if (emoteTimer > 0) {
      emoteTimer -= dt;
      if (emoteTimer <= 0) {
        currentEmote = null;
      }
    }

    // 인지(Perceive) 타이머
    _perceiveTimer += dt;
    if (_perceiveTimer >= PERCEIVE_INTERVAL) {
      _perceiveTimer = 0;
      _requestPerceive();
    }
  }

  Future<void> _requestPerceive() async {
    // 임시로 주변 사람 리스트는 비워둠 (추후 구현)
    final response = await ApiClient.perceive(agentName, position.x, position.y, []);
    
    if (response != null) {
      // 응답에서 대사(emote)가 있으면 띄움
      if (response['emote'] != null && response['emote'].toString().isNotEmpty) {
        showEmote(response['emote']);
      }
      
      // 타겟 좌표가 다르면 이동
      final double targetX = response['target_x'];
      final double targetY = response['target_y'];
      
      if ((targetX - position.x).abs() > 5 || (targetY - position.y).abs() > 5) {
        double dur = _isZombie ? 15.0 : 4.0;
        add(MoveEffect.to(Vector2(targetX, targetY), EffectController(duration: dur)));
      }
    }
  }

  @override
  void render(Canvas canvas) {
    // 원래의 전신 캐릭터(Sprite) 렌더링
    super.render(canvas);

    // 이모티콘 (대사) 렌더링
    if (currentEmote != null) {
      TextSpan span = TextSpan(
        style: const TextStyle(
          fontSize: 14, 
          color: Colors.black, 
          fontWeight: FontWeight.bold,
          fontFamily: 'Roboto', // 한글 깨짐 방지용 기본 폰트 설정
        ),
        text: currentEmote,
      );
      TextPainter tp = TextPainter(
        text: span,
        textAlign: TextAlign.center,
        textDirection: ui.TextDirection.ltr,
      );
      tp.layout(maxWidth: 150); // 너무 길어지면 줄바꿈

      // 말풍선 배경 그리기
      final bubbleRect = Rect.fromLTWH(
        (size.x - tp.width) / 2 - 8,
        -tp.height - 15,
        tp.width + 16,
        tp.height + 10
      );
      final bgPaint = Paint()..color = Colors.white.withOpacity(0.9);
      final borderPaint = Paint()
        ..color = Colors.black
        ..style = PaintingStyle.stroke
        ..strokeWidth = 2.0;

      // 둥근 사각형으로 말풍선 렌더링
      canvas.drawRRect(RRect.fromRectAndRadius(bubbleRect, const Radius.circular(8)), bgPaint);
      canvas.drawRRect(RRect.fromRectAndRadius(bubbleRect, const Radius.circular(8)), borderPaint);

      // 텍스트 렌더링
      tp.paint(canvas, Offset((size.x - tp.width) / 2, -tp.height - 10));
    }

    // 상태에 따른 HP 바 색상 결정
    Color barColor = Colors.green;
    if (currentHP <= 20) {
      barColor = Colors.red;
    } else if (currentHP <= 50) {
      barColor = Colors.orange;
    }
    final paint = Paint()..color = barColor;
    canvas.drawRect(Rect.fromLTWH(0, size.y + 5, size.x * (currentHP / 100), 5), paint); 

    // 에이전트 이름 표시 (얼굴 아래) - 가독성을 위해 검은색 테두리(그림자) 추가
    const textStyle = TextStyle(
      color: Colors.white, 
      fontSize: 10, 
      fontWeight: FontWeight.bold,
      shadows: [
        ui.Shadow(offset: ui.Offset(-1, -1), color: Colors.black),
        ui.Shadow(offset: ui.Offset(1, -1), color: Colors.black),
        ui.Shadow(offset: ui.Offset(1, 1), color: Colors.black),
        ui.Shadow(offset: ui.Offset(-1, 1), color: Colors.black),
      ],
    );
    final textSpan = TextSpan(text: agentName, style: textStyle);
    final textPainter = TextPainter(text: textSpan, textDirection: ui.TextDirection.ltr);
    textPainter.layout();
    textPainter.paint(canvas, Offset((size.x - textPainter.width) / 2, size.y + 12));
  }

  @override
  void onTap() {
    // 따스한 손길 (쓰다듬기) 로직: 터치 시 ✨ 이모티콘 표출 및 의욕(HP) 상승
    showEmote('✨');
    recoverHP(20);
    debugPrint("에이전트를 쓰다듬었습니다! 의욕이 상승합니다. ✨");
  }
}
