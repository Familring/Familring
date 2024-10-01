import 'package:shared_preferences/shared_preferences.dart';

// 토큰 저장
Future<void> saveToken(String token) async {
  SharedPreferences prefs = await SharedPreferences.getInstance();
  await prefs.setString('auth_token', token);
}

// 저장된 토큰 불러오기
Future<String?> getToken() async {
  SharedPreferences prefs = await SharedPreferences.getInstance();
  return prefs.getString('auth_token');
}

// 토큰 삭제 (로그아웃 시)
Future<void> deleteToken() async {
  SharedPreferences prefs = await SharedPreferences.getInstance();
  await prefs.remove('auth_token');
}
