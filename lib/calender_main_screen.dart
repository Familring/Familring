import 'package:flutter/material.dart';
import 'package:table_calendar/table_calendar.dart';

class CalendarMainScreen extends StatefulWidget {
  @override
  _CalendarMainScreenState createState() => _CalendarMainScreenState();
}

class _CalendarMainScreenState extends State<CalendarMainScreen> {
  late Map<DateTime, List<Event>> _events;
  late List<Event> _selectedEvents;
  late DateTime _focusedDay;
  late DateTime _selectedDay;

  @override
  void initState() {
    super.initState();
    _events = {
      DateTime.utc(2024, 7, 16): [Event('아빠 생신')],
      DateTime.utc(2024, 7, 22): [Event('가족 여행 시작')],
      DateTime.utc(2024, 7, 25): [Event('가족 여행 종료')],
    };
    _selectedEvents = [];
    _focusedDay = DateTime.now();
    _selectedDay = DateTime.now();
    _selectedEvents = _getEventsForDay(_selectedDay);
  }

  List<Event> _getEventsForDay(DateTime day) {
    return _events[day] ?? [];
  }

  void _onDaySelected(DateTime selectedDay, DateTime focusedDay) {
    if (!isSameDay(_selectedDay, selectedDay)) {
      setState(() {
        _selectedDay = selectedDay;
        _focusedDay = focusedDay;
        _selectedEvents = _getEventsForDay(selectedDay);
      });
    }
  }

  void _addEvent(DateTime date, String title) {
    if (_events[date] != null) {
      _events[date]!.add(Event(title));
    } else {
      _events[date] = [Event(title)];
    }
    setState(() {
      _selectedEvents = _getEventsForDay(_selectedDay);
    });
  }

  void _showAddEventDialog() {
    DateTime selectedDate = _selectedDay;
    String eventTitle = '';
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return StatefulBuilder(
          builder: (context, setState) {
            return AlertDialog(
              title: Text('일정 추가'),
              content: Column(
                mainAxisSize: MainAxisSize.min,
                children: <Widget>[
                  ListTile(
                    leading: Icon(Icons.calendar_today),
                    title: Text("${selectedDate.toLocal()}".split(' ')[0]),
                    onTap: () async {
                      DateTime? picked = await showDatePicker(
                        context: context,
                        initialDate: selectedDate,
                        firstDate: DateTime(2020),
                        lastDate: DateTime(2030),
                      );
                      if (picked != null && picked != selectedDate) {
                        setState(() {
                          selectedDate = picked;
                        });
                      }
                    },
                  ),
                  TextField(
                    onChanged: (value) {
                      eventTitle = value;
                    },
                    decoration: InputDecoration(hintText: "일정 내용을 입력하세요"),
                  ),
                ],
              ),
              actions: <Widget>[
                TextButton(
                  child: Text('취소'),
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                ),
                TextButton(
                  child: Text('추가'),
                  onPressed: () {
                    if (eventTitle.isNotEmpty) {
                      Navigator.of(context).pop(); // 다이얼로그 닫기
                      setState(() {
                        _addEvent(selectedDate, eventTitle);
                        _selectedDay = selectedDate; // 캘린더의 선택된 날짜를 업데이트
                        _focusedDay = selectedDate;
                        _selectedEvents = _getEventsForDay(_selectedDay);
                      });
                    }
                  },
                ),
              ],
            );
          },
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('캘린더'),
        backgroundColor: Colors.white,
        elevation: 0,
      ),
      body: Container(
        color: Colors.white,
        child: Column(
          children: [
            SizedBox(height: 40), // AppBar와 캘린더 사이의 간격
            Container(
              color: Colors.white,
              padding: EdgeInsets.all(16.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    '7월',
                    style: TextStyle(fontSize: 32, color: Colors.orange),
                  ),
                ],
              ),
            ),
            TableCalendar(
              focusedDay: _focusedDay,
              firstDay: DateTime.utc(2020, 1, 1),
              lastDay: DateTime.utc(2030, 12, 31),
              selectedDayPredicate: (day) => isSameDay(_selectedDay, day),
              onDaySelected: _onDaySelected,
              eventLoader: _getEventsForDay,
              calendarStyle: CalendarStyle(
                todayTextStyle: TextStyle(color: Colors.black),
                todayDecoration: BoxDecoration(
                  color: Colors.orangeAccent,
                  shape: BoxShape.circle,
                ),
                selectedDecoration: BoxDecoration(
                  color: Colors.orange,
                  shape: BoxShape.circle,
                ),
                markerDecoration: BoxDecoration(
                  color: Colors.green,
                  shape: BoxShape.circle,
                ),
                outsideDaysVisible: false,
                weekendTextStyle: TextStyle(color: Colors.red),
                holidayTextStyle: TextStyle(color: Colors.red),
                cellMargin: EdgeInsets.symmetric(vertical: 12.0), // 셀 마진을 조정하여 행 높이를 늘림
              ),
              headerStyle: HeaderStyle(
                formatButtonVisible: false,
                titleCentered: true,
                titleTextStyle: TextStyle(fontSize: 20, color: Colors.orange),
                leftChevronIcon: Icon(Icons.chevron_left, color: Colors.orange),
                rightChevronIcon: Icon(Icons.chevron_right, color: Colors.orange),
              ),
              daysOfWeekStyle: DaysOfWeekStyle(
                weekendStyle: TextStyle(color: Colors.red),
              ),
              calendarBuilders: CalendarBuilders(
                dowBuilder: (context, day) {
                  if (day.weekday == DateTime.sunday) {
                    return Center(
                      child: Text(
                        '일',
                        style: TextStyle(color: Colors.red),
                      ),
                    );
                  } else if (day.weekday == DateTime.saturday) {
                    return Center(
                      child: Text(
                        '토',
                        style: TextStyle(color: Colors.blue),
                      ),
                    );
                  } else {
                    return Center(
                      child: Text(
                        ['월', '화', '수', '목', '금'][day.weekday - 1],
                        style: TextStyle(color: Colors.black),
                      ),
                    );
                  }
                },
                markerBuilder: (context, date, events) {
                  if (events.isNotEmpty) {
                    return Positioned(
                      right: 1,
                      bottom: 1,
                      child: Container(
                        decoration: BoxDecoration(
                          color: Colors.blue,
                          borderRadius: BorderRadius.circular(12.0),
                        ),
                        width: 16,
                        height: 16,
                        child: Center(
                          child: Text(
                            '${events.length}',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 12.0,
                            ),
                          ),
                        ),
                      ),
                    );
                  }
                  return SizedBox();
                },
              ),
            ),
            Expanded(
              child: ListView.builder(
                itemCount: _selectedEvents.length,
                itemBuilder: (context, index) {
                  return ListTile(
                    title: Text(_selectedEvents[index].title),
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
          onPressed: _showAddEventDialog,
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
