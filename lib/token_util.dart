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

// 글씨 크기 저장
Future<void> saveFontSize(double fontSize) async {
  SharedPreferences prefs = await SharedPreferences.getInstance();
  await prefs.setDouble('font_size', fontSize);
}

// 저장된 글씨 크기 불러오기
Future<double> getSavedFontSize() async {
  SharedPreferences prefs = await SharedPreferences.getInstance();
  return prefs.getDouble('font_size') ?? 16.0;  // 기본값 16.0
}
