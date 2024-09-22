import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class BucketListScreen extends StatefulWidget {
  @override
  _BucketListScreenState createState() => _BucketListScreenState();
}

class _BucketListScreenState extends State<BucketListScreen> {
  List<dynamic> _bucketList = [];

  @override
  void initState() {
    super.initState();
    _fetchBucketList();
  }

  // 버킷리스트 가져오기
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

  // 버킷리스트 추가 API 호출
  void _addBucketItem(String item) async {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/api/bucket/add/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'bucket_title': item,
        'bucket_content': '',
        'is_completed': false,
      }),
    );
    if (response.statusCode == 201) {
      _fetchBucketList();
    } else {
      throw Exception('Failed to add bucket list');
    }
  }

  // 버킷리스트 완료 API 호출
  void _completeBucketItem(int bucketId) async {
    final response = await http.put(
      Uri.parse('http://127.0.0.1:8000/api/bucket/complete/$bucketId/'),
    );
    if (response.statusCode == 200) {
      _fetchBucketList(); // 성공적으로 완료된 후, 목록을 다시 로드
    } else {
      throw Exception('Failed to complete bucket list');
    }
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('버킷리스트'),
      ),
      body: ListView.builder(
        itemCount: _bucketList.length,
        itemBuilder: (context, index) {
          return Card(
            child: ListTile(
              leading: Icon(Icons.emoji_objects),
              title: Text(_bucketList[index]['bucket_title']),
              trailing: Checkbox(
                value: _bucketList[index]['is_completed'],
                onChanged: (bool? value) {
                  if (value == true) {
                    _completeBucketItem(_bucketList[index]['id']);
                  }
                },
              ),
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _showAddBucketDialog,
        backgroundColor: Colors.orange,
        child: Icon(Icons.add),
      ),
    );
  }
}
