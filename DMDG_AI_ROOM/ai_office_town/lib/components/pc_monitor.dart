import 'package:flutter/material.dart';
import 'package:bonfire/bonfire.dart';

class PcMonitor extends GameDecoration with Lighting {
  PcMonitor(Vector2 position)
      : super(
          position: position,
          size: Vector2.zero(), // 이미지가 보이지 않게 크기를 0으로 설정
        ) {
    setupLighting(
      LightingConfig(
        radius: 150, // 책상 주변을 충분히 밝히도록 반경 대폭 확대
        blurBorder: 100,
        color: Colors.lightBlueAccent.withOpacity(0.3),
      ),
    );
  }
}
