import 'package:flutter/material.dart';
import 'answer_question_screen.dart';

class QuestionListScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Familring List'),
        backgroundColor: Colors.orange,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: ListView(
          children: [
            ListTile(
              title: Text(
                '#03 가장 최근에 읽은 책은?',
                style: TextStyle(color: Colors.orange),
              ),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => AnswerQuestionScreen(question: '가장 최근에 읽은 책은?'),
                  ),
                );
              },
            ),
            ListTile(
              title: Text(
                '#02 가장 좋아하는 과일은?',
                style: TextStyle(color: Colors.orange),
              ),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => AnswerQuestionScreen(question: '가장 좋아하는 과일은?'),
                  ),
                );
              },
            ),
            ListTile(
              title: Text(
                '#01 가장 여행 가고 싶은 나라는?',
                style: TextStyle(color: Colors.orange),
              ),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => AnswerQuestionScreen(question: '가장 여행 가고 싶은 나라는?'),
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
