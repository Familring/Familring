import 'package:flutter/material.dart';
import 'question_notification.dart'; // QuestionNotification 파일 임포트

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  void initState() {
    super.initState();
    // 1초 뒤에 QuestionNotification으로 화면 전환
    Future.delayed(Duration(seconds: 1), () {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => QuestionNotification()),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('홈'),
        backgroundColor: Colors.orange,
      ),
      body: Center(
        child: Text(
          '환영합니당',
          style: TextStyle(fontSize: 24),
        ),
      ),
    );
  }
}
