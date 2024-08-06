import 'package:flutter/material.dart';
import 'photo_album_screen.dart';
import 'question_list_screen.dart';
import 'home_screen.dart';
import 'calender_component_screen.dart';
import 'mypage_screen.dart';

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
      home: MyHomePage(),
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
    MyPageScreen(),
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
            label: '',
          ),
          BottomNavigationBarItem(
            icon: ImageIcon(
              AssetImage('images/question_list_icon.png'),
              size: 35,
            ),
            label: '',
          ),
          BottomNavigationBarItem(
            icon: ImageIcon(
              AssetImage('images/home_icon.png'),
              size: 35,
            ),
            label: '',
          ),
          BottomNavigationBarItem(
            icon: ImageIcon(
              AssetImage('images/calender_icon.png'),
              size: 35,
            ),
            label: '',
          ),
          BottomNavigationBarItem(
            icon: ImageIcon(
              AssetImage('images/mypage_icon.png'),
              size: 35,
            ),
            label: '',
          ),
        ],
        currentIndex: _selectedIndex,
        selectedItemColor: Color.fromARGB(255, 101, 101, 101),
        unselectedItemColor: Color.fromARGB(255, 218, 218, 218),
        onTap: _onItemTapped,
        selectedFontSize: 0, // 선택된 아이콘의 폰트 크기를 0으로 설정
        unselectedFontSize: 0, // 선택되지 않은 아이콘의 폰트 크기를 0으로 설정
        showSelectedLabels: false, // 선택된 아이콘의 레이블 숨김
        showUnselectedLabels: false, // 선택되지 않은 아이콘의 레이블 숨김
      ),
    );
  }
}

