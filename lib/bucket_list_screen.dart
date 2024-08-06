import 'package:flutter/material.dart';

class BucketListScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('버킷리스트'),
        backgroundColor: Colors.orange,
      ),
      body: Center(
        child: Text(
          '버킷리스트 화면',
          style: TextStyle(fontSize: 24),
        ),
      ),
    );
  }
}
