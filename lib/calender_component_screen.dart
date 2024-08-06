import 'package:flutter/material.dart';

class CalendarComponentScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('홈'),
        backgroundColor: Colors.orange,
      ),
      body: Center(
        child: Text(
          '캘린더와 버킷리스트',
          style: TextStyle(fontSize: 24),
        ),
      ),
    );
  }
}