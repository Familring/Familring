import 'package:flutter/material.dart';

class DeleteAccountScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('회원 탈퇴'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            // 회원 탈퇴 로직을 여기에 구현
            showDialog(
              context: context,
              builder: (context) => AlertDialog(
                title: Text('회원 탈퇴'),
                content: Text('정말로 회원 탈퇴를 하시겠습니까?'),
                actions: [
                  TextButton(
                    onPressed: () {
                      Navigator.of(context).pop(); // 탈퇴 취소
                    },
                    child: Text('취소'),
                  ),
                  TextButton(
                    onPressed: () {
                      // 실제 탈퇴 로직
                      Navigator.of(context).pop();
                    },
                    child: Text('확인'),
                  ),
                ],
              ),
            );
          },
          child: Text('회원 탈퇴'),
        ),
      ),
    );
  }
}
