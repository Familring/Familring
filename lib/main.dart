import 'package:flutter/material.dart';
import 'welcome_screen.dart';
import 'login_screen.dart';
import 'signup_screen.dart';
import 'question_list_screen.dart';
import 'answer_question_screen.dart';
import 'home_screen.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Familring App',
      theme: ThemeData(
        primarySwatch: Colors.orange,
      ),
      home: WelcomeScreen(),
      routes: {
        '/login': (context) => LoginScreen(),
        '/signup': (context) => SignupScreen(),
        '/questions': (context) => QuestionListScreen(),
        '/answer': (context) => AnswerQuestionScreen(question: '',),
        '/home': (context) => HomeScreen(),  // 홈 화면 추가
      },
    );
  }
}
