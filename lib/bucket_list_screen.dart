import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class BucketListScreen extends StatefulWidget {
  @override
  _BucketListScreenState createState() => _BucketListScreenState();
}

class _BucketListScreenState extends State<BucketListScreen> {
  List<String> _bucketList = [];
  List<bool> _isChecked = [];
  int _completedCount = 0;

  void _addBucketItem(String item) {
    setState(() {
      _bucketList.add(item);
      _isChecked.add(false);
    });
  }

  void _showAddBucketDialog() {
    String newBucketItem = '';
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('버킷리스트 추가'),
          content: TextField(
            onChanged: (value) {
              newBucketItem = value;
            },
            decoration: InputDecoration(hintText: "새로운 버킷리스트 항목"),
          ),
          actions: <Widget>[
            TextButton(
              child: Text('취소'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
            TextButton(
              child: Text('확인'),
              onPressed: () {
                _addBucketItem(newBucketItem);
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  void _fetchBucketList() async {
    final response = await http.get(Uri.parse('http://127.0.0.1:8000/api/bucket/'));
    if (response.statusCode == 200) {
      setState(() {
        _bucketList = json.decode(response.body);
      });
    } else {
      throw Exception('Failed to load bucket list');
    }
  }

  void _showCompletionDialog(int index) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('버킷리스트 완료'),
          content: Text('해당 버킷리스트를 이루셨나요?'),
          actions: <Widget>[
            TextButton(
              child: Text('취소'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
            TextButton(
              child: Text('확인'),
              onPressed: () {
                setState(() {
                  _isChecked[index] = true;
                  _completedCount++;
                });
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    int remainingCount = _bucketList.length - _completedCount;
    return Scaffold(
      appBar: AppBar(
        title: Text('버킷리스트'),
        backgroundColor: Colors.white,
      ),
      backgroundColor: Colors.white, // 배경 색상을 하얀색으로 변경
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(height: 20),
            Text(
              '하고 싶은 것들이\n${remainingCount}개 남았어요!',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 10),
            Text(
              '지금까지 $_completedCount개를 이뤘어요',
              style: TextStyle(fontSize: 16, color: Colors.grey),
            ),
            SizedBox(height: 20),
            Expanded(
              child: ListView.builder(
                itemCount: _bucketList.length,
                itemBuilder: (context, index) {
                  return Card(
                    child: ListTile(
                      leading: Icon(Icons.emoji_objects),
                      title: Text(_bucketList[index]),
                      trailing: Checkbox(
                        value: _isChecked[index],
                        onChanged: (bool? value) {
                          if (value == true) {
                            _showCompletionDialog(index);
                          }
                        },
                      ),
                      onTap: () {
                        if (!_isChecked[index]) {
                          _showCompletionDialog(index);
                        }
                      },
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: Padding(
        padding: const EdgeInsets.all(20.0), // FloatingActionButton의 패딩
        child: FloatingActionButton(
          onPressed: _showAddBucketDialog,
          backgroundColor: Colors.orange,
          child: Icon(Icons.add),
        ),
      ),
    );
  }
}

class Event {
  final String title;

  Event(this.title);

  @override
  String toString() => title;
}
