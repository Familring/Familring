import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class PhotoAlbumScreen extends StatefulWidget {
  @override
  _PhotoAlbumScreenState createState() => _PhotoAlbumScreenState();
}

class _PhotoAlbumScreenState extends State<PhotoAlbumScreen> {
  List _albums = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchAlbums();
  }

  // 앨범 데이터를 서버에서 가져오는 함수
  void _fetchAlbums() async {
    final response = await http.get(Uri.parse('http://127.0.0.1:8000/api/albums/'));
    if (response.statusCode == 200) {
      setState(() {
        _albums = json.decode(response.body);
        _isLoading = false;
      });
    } else {
      throw Exception('Failed to load albums');
    }
  }

  // 앨범 추가 기능
  void _addAlbum(String albumName) async {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/api/add-album/'),
      body: json.encode({'album_name': albumName}),
      headers: {"Content-Type": "application/json"},
    );

    if (response.statusCode == 201) {
      setState(() {
        _fetchAlbums();
      });
    } else {
      throw Exception('Failed to add album');
    }
  }

  // 앨범 추가 다이얼로그
  void _showAddAlbumDialog() {
    final TextEditingController albumController = TextEditingController();

    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('앨범 추가'),
          content: TextField(
            controller: albumController,
            decoration: InputDecoration(hintText: '앨범 이름을 입력하세요'),
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: Text('취소'),
            ),
            TextButton(
              onPressed: () {
                _addAlbum(albumController.text);
                Navigator.of(context).pop();
              },
              child: Text('추가'),
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
        title: Text('사진첩'),
        backgroundColor: Colors.orange,
      ),
      body: _isLoading
          ? Center(child: CircularProgressIndicator())
          : _albums.isEmpty
          ? Center(child: Text('앨범이 없습니다.'))
          : ListView.builder(
        itemCount: _albums.length,
        itemBuilder: (context, index) {
          return ListTile(
            leading: Icon(Icons.photo_album),
            title: Text(_albums[index]['album_name']),
            onTap: () {
              // 앨범 클릭 시 사진 목록 화면으로 이동
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => AlbumDetailScreen(albumId: _albums[index]['id']),
                ),
              );
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _showAddAlbumDialog,
        child: Icon(Icons.add),
        backgroundColor: Colors.orange,
      ),
    );
  }
}

class AlbumDetailScreen extends StatelessWidget {
  final int albumId;

  AlbumDetailScreen({required this.albumId});

  @override
  Widget build(BuildContext context) {
    // 앨범 상세 화면 구현
    return Scaffold(
      appBar: AppBar(
        title: Text('앨범 상세'),
        backgroundColor: Colors.orange,
      ),
      body: Center(
        child: Text('앨범 ID: $albumId'),
      ),
    );
  }
}