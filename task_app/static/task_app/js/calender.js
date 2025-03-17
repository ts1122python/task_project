const resources = [
  { id: 1, title: 'Room 1' }, { id: 2, title: 'Room 2' }, { id: 3, title: 'Room 3'}
];

function createDate(hours, minutes) {
  const now = new Date();
  now.setHours(hours);
  now.setMinutes(minutes);
  now.setSeconds(0);
  return now;
}

const events = [{
  id: 1,
  resourceIds: [1],
  start: createDate(9, 0),
  end: createDate(10, 30),
  title: 'Editable Event',
  editable: true,
}, {
  id: 2,
  resourceIds: [2],
  start: createDate(11, 0),
  end: createDate(13, 30),
  title: 'Uneditable Event',
  // editable: false, // not work
  startEditable: false,
  durationEditable: false,
  backgroundColor: 'red',
}];

function getOverlappingEvents(event) {
  // select event has event.resource.id
  // eventDrop event has event.resourceIds
  const rId = event.resource ? event.resource.id : event.resourceIds[0];
  return ec.getEvents().filter(e => 
    e.resourceIds[0] == rId && e.start < event.end && event.start < e.end);
}

function hasOverlappingEvents(event) {
  return getOverlappingEvents(event).length > 0;
}

function hasOtherOverlappingEvents(event) {
  return getOverlappingEvents(event).filter(e => e.id != event.id).length > 0
}

const ec = new EventCalendar(document.getElementById('ec'), {
  resources,
  events,
  view: 'resourceTimeGridDay',
  allDaySlot: false,
  slotMinTime: '08:00:00',
  slotMaxTime: '19:00:00',
  nowIndicator: true,
  selectable: true,
  select: function(event) {
    if (hasOverlappingEvents(event)) {
      ec.unselect();
      return;
    }
    showModal(event);
  },
  eventDrop: function ({ event, revert }) {
    if (hasOtherOverlappingEvents(event)) revert();
  },
  eventResize: function ({ event, revert }) {
    if (hasOtherOverlappingEvents(event)) revert();
  },
  datesSet: function ({ start }) {
    toggleDateButtonsFor7Days(start);
  },
  eventClick: function ({ event }) {
    showModal(event);
  },
});

function toggleDateButtonsFor7Days(start) {
  const next = document.querySelector('.ec-next');
  const prev = document.querySelector('.ec-prev');
  const now = dayjs();
  const targetDate = dayjs(start);
  prev.disabled = targetDate.isBefore(now);
  next.disabled = targetDate.isAfter(now.add(6, 'day'));  
}

function addEvent(event) {
  if (event.id) {
    ec.updateEvent(event);
    return;
  }
  event.id = new Date().getTime();
  event.resourceIds = [ event.resource.id ];
  ec.addEvent(event);
  ec.unselect();
}

const dialog = document.querySelector('dialog');

function showModal(event) {
  function getResourceTitle(event) {
    const resourceId = event.resource ? event.resource.id : event.resourceIds[0];
    const resource = resources.find(r => r.id == resourceId);
    return resource ? resource.title : '';
  }
  document.getElementById('room-name').innerText = getResourceTitle(event);
  const startDate = dayjs(event.start);
  document.getElementById('date').innerText = startDate.format('YYYY/MM/DD');
  document.getElementById('start').value = startDate.format('HH:mm');
  document.getElementById('end').value = dayjs(event.end).format('HH:mm');
  document.getElementById('comment').value = event.title || '';
  dialog.event = event;
  dialog.showModal();
}

document.getElementById('form').onsubmit = function(e) {
  e.preventDefault();
  const event = dialog.event;

  const startTime = document.getElementById('start').value.split(':');
  event.start.setHours(Number(startTime[0]));
  event.start.setMinutes(Number(startTime[1]));

  const endTime = document.getElementById('end').value.split(':');
  event.end.setHours(Number(endTime[0]));
  event.end.setMinutes(Number(endTime[1]));

  const comment = document.getElementById('comment').value;
  event.title = comment;
  addEvent(event);
  dialog.close();
}

document.getElementById('cancel').onclick = function() {
  dialog.close();
};



