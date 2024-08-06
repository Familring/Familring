import 'package:flutter/material.dart';

class MyPageScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('홈'),
        backgroundColor: Colors.orange,
      ),
      body: Center(
        child: Text(
          '마이페이지',
          style: TextStyle(fontSize: 24),
        ),
      ),
    );
  }
}