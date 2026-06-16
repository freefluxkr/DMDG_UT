import 'package:flutter/material.dart';
import 'main_game.dart';

void main() {
  runApp(const AIOfficeTownApp());
}

class AIOfficeTownApp extends StatelessWidget {
  const AIOfficeTownApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Office Town',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      // 시작 화면을 MainGame으로 설정
      home: const MainGame(),
    );
  }
}
