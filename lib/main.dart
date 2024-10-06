import 'package:flutter/material.dart';
import 'package:familring/bucket_list_screen.dart';
import 'package:familring/calender_main_screen.dart';
import 'package:familring/login_screen.dart';
import 'package:familring/signup_screen.dart';
import 'package:familring/welcome_screen.dart';
import 'package:familring/font_size_settings_screen.dart'; // 글씨 크기 변경 페이지 import
import 'photo_album_screen.dart';
import 'question_list_screen.dart';
import 'home_screen.dart';
import 'calender_component_screen.dart';
import 'mypage_screen.dart' as mypage; // 별칭 사용하여 중복 방지
import 'edit_profile_screen.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Navigation Bar',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      debugShowCheckedModeBanner: false,
      home: WelcomeScreen(),
      routes: {
        '/login': (context) => LoginScreen(),
        '/signup': (context) => SignupScreen(),
        '/home': (context) => MyHomePage(),
        '/calender': (context) => CalendarMainScreen(),
        '/bucketlist': (context) => BucketListScreen(),
        '/today_question': (context) => QuestionListScreen(),
        // 여기에 nickname 값을 전달해야 합니다.
        '/edit_profile': (context) => EditProfileScreen(nickname: '현재닉네임'), // 실제 로그인한 사용자의 닉네임으로 대체
        '/font_size_settings': (context) => FontSizeSettingsScreen(),
      },
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _selectedIndex = 2;

  static List<Widget> _widgetOptions = <Widget>[
    PhotoAlbumScreen(),
    QuestionListScreen(),
    HomeScreen(),
    CalendarComponentScreen(),
    mypage.MyPageScreen(),  // 별칭 사용하여 MyPageScreen 호출
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: _widgetOptions.elementAt(_selectedIndex),
      ),
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        items: <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: ImageIcon(
              AssetImage('images/photo_album_icon.png'),
              size: 40,
            ),
            label: '가족앨범',
          ),
          BottomNavigationBarItem(
            icon: ImageIcon(
              AssetImage('images/question_list_icon.png'),
              size: 35,
            ),
            label: '데일리로그',
          ),
          BottomNavigationBarItem(
            icon: ImageIcon(
              AssetImage('images/home_icon.png'),
              size: 35,
            ),
            label: '홈',
          ),
          BottomNavigationBarItem(
            icon: ImageIcon(
              AssetImage('images/calender_icon.png'),
              size: 35,
            ),
            label: '캘린더',
          ),
          BottomNavigationBarItem(
            icon: ImageIcon(
              AssetImage('images/mypage_icon.png'),
              size: 35,
            ),
            label: '내정보',
          ),
        ],
        currentIndex: _selectedIndex,
        selectedItemColor: Color.fromARGB(255, 101, 101, 101),
        unselectedItemColor: Color.fromARGB(255, 218, 218, 218),
        onTap: _onItemTapped,
        selectedFontSize: 12,
        unselectedFontSize: 12,
        showSelectedLabels: true,
        showUnselectedLabels: true,
      ),
    );
  }
}