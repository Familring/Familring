import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SignupScreen extends StatelessWidget {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _confirmPasswordController = TextEditingController();

  void _signup(BuildContext context) async {
    String username = _usernameController.text;
    String password = _passwordController.text;
    String confirmPassword = _confirmPasswordController.text;

    if (password != confirmPassword) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('비밀번호가 일치하지 않습니다.')),
      );
      return;
    }

    try {
      var url = Uri.parse('http://10.0.2.2:8000/api/register/');// 각자의 에뮬레이터 or web의 주소에 맞게 URL을 변경할 것
      var response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'}, // 서버에 JSON형식의 데이터로 보낼 것임을 선언
        body: jsonEncode({ //jsonEncode() 함수는 Dart의 Map을 JSON 형식의 문자열로 변환
          'username': username,
          'password': password,
        }),
      );

      print('Response status: ${response.statusCode}');
      print('Response body: ${response.body}');

      if (response.statusCode == 201) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('회원가입이 완료되었습니다.')),
        );
        Navigator.pushNamedAndRemoveUntil(context, '/login', (route) => false);
      } else {
        var responseData = jsonDecode(response.body);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('회원가입에 실패했습니다: ${responseData['error']}')),
        );
      }
    } catch (error) {
      print('Error: $error');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('회원가입 중 오류가 발생했습니다. 다시 시도해주세요.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('회원 가입'),
        backgroundColor: Colors.orange,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: _usernameController,
              decoration: InputDecoration(
                labelText: '아이디',
              ),
            ),
            TextField(
              controller: _passwordController,
              decoration: InputDecoration(
                labelText: '비밀번호',
              ),
              obscureText: true,
            ),
            TextField(
              controller: _confirmPasswordController,
              decoration: InputDecoration(
                labelText: '비밀번호 확인',
              ),
              obscureText: true,
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                _signup(context);
              },
              child: Text('회원 가입하기'),
              style: ElevatedButton.styleFrom(backgroundColor: Colors.orange),
            ),
          ],
        ),
      ),
    );
  }
}

