import Calendar from '@event-calendar/core';
import TimeGrid from '@event-calendar/time-grid';
// Import CSS if your build tool supports it
import '@event-calendar/core/index.css';


let ec = new EventCalendar(document.getElementById('ec'), {
    view: 'dayGridMonth',
    date: '2025-03-01',  // 2025-03-01が表示された状態で表示される
    dayCellFormat: function(date) {
      return date.getDate().toString().padStart(2, '0');
    },
    events: [
      {start: "2024-04-01", end: "2024-04-03", title: "イベント1", textColor: "#000000", color: "#FFFF00"},
      {start: "2024-04-05", end: "2024-04-05", title: "イベント2", textColor: "#0D61A9", color: "#FE6B64"},
    ],
    headerToolbar: {
      start: 'prev', center: 'title', end: 'today timeGridWeek next'
    },
    dateClick: function (info) {
      alert('dateClick されたよ');
      console.log(info);
    },
    eventClick: function (info) {
      alert('eventClick されたよ');
      console.log(info);
    }
  });
  
  
  ec.setOption('date',  '2024-04-01');
  //ec.setOption('date',  new Date('2023-01-01'));  // Date型でもOK


