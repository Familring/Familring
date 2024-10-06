import 'package:flutter/material.dart';

class FamilyManagementScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('가족 구성 관리'),
      ),
      body: Center(
        child: Text('여기서 가족 구성원을 추가하거나 삭제할 수 있는 기능을 구현합니다.'),
      ),
    );
  }
}
