import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:familring/utils/token_util.dart';  // 토큰 유틸리티 함수 임포트
import 'dart:convert';
import 'font_size_settings_screen.dart'; // 폰트 크기 설정 페이지 import
import 'family_management_screen.dart';  // 가족 관리 페이지 import

class MyPageScreen extends StatefulWidget {
  @override
  _MyPageScreenState createState() => _MyPageScreenState();
}

class _MyPageScreenState extends State<MyPageScreen> {
  String nickname = ''; // 초기 닉네임 (기본값)

  @override
  void initState() {
    super.initState();
    _loadProfileData(); // 닉네임 초기 데이터 로드
  }

  Future<void> _loadProfileData() async {
    String? token = await getToken();
    if (token == null) {
      print('No token found!');
      return;
    }

    final headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $token',
    };

    final response = await http.get(
      Uri.parse('http://127.0.0.1:8000/api/profile/'),
      headers: headers,
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(utf8.decode(response.bodyBytes));
      setState(() {
        nickname = data['nickname']; // 닉네임 업데이트
      });
    } else {
      print('Failed to load profile data');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('마이페이지'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            SizedBox(height: 20),
            CircleAvatar(
              radius: 50,
              backgroundImage: AssetImage('images/mypage.png'), // 프로필 이미지
            ),
            SizedBox(height: 10),
            Text(
              '$nickname 님', // 닉네임 표시
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 30),
            ListTile(
              title: Text('내 프로필 편집'),
              trailing: Icon(Icons.arrow_forward_ios),
              onTap: () async {
                final updatedNickname = await Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => EditProfileScreen(nickname: nickname)), // nickname 전달
                );

                if (updatedNickname != null) {
                  setState(() {
                    nickname = updatedNickname; // 닉네임 업데이트
                  });
                }
              },
            ),
            ListTile(
              title: Text('글씨 크기 변경'),
              trailing: Icon(Icons.arrow_forward_ios),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => FontSizeSettingsScreen()),
                );
              },
            ),
            ListTile(
              title: Text('가족 추가하기'),  // 가족 추가하기 메뉴
              trailing: Icon(Icons.arrow_forward_ios),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => FamilyManagementScreen()), // 가족 관리 페이지로 이동
                );
              },
            ),
            // 나머지 항목들...
          ],
        ),
      ),
    );
  }
}

class EditProfileScreen extends StatefulWidget {
  final String nickname;

  EditProfileScreen({required this.nickname}); // nickname을 생성자에 추가

  @override
  _EditProfileScreenState createState() => _EditProfileScreenState();
}

class _EditProfileScreenState extends State<EditProfileScreen> {
  late TextEditingController _nicknameController;

  @override
  void initState() {
    super.initState();
    _nicknameController = TextEditingController(text: widget.nickname);
  }

  Future<void> _updateProfile() async {
    String? token = await getToken();
    if (token == null) {
      print('No token found');
      return;
    }

    final headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $token',
    };

    final body = jsonEncode({'nickname': _nicknameController.text});

    try {
      final response = await http.put(
        Uri.parse('http://127.0.0.1:8000/api/profile/update/'),
        headers: headers,
        body: body,
      );

      if (response.statusCode == 200) {
        Navigator.pop(context, _nicknameController.text); // 수정된 닉네임 전달
      } else {
        print('Failed to update profile: ${response.statusCode}');
      }
    } catch (e) {
      print('Error updating profile: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('프로필 수정'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _nicknameController,
              decoration: InputDecoration(labelText: '닉네임'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _updateProfile,
              child: Text('저장'),
            ),
          ],
        ),
      ),
    );
  }
}
